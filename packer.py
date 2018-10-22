#!/usr/bin/env python

import fnmatch
import os
import json
import tempfile
import subprocess
import shutil
import re
import logging
import argparse
import pdb


# TODO: handle upper level files in config, e.g. { searchDirectories: ['../../lib'] }

logger = logging.getLogger('packer')


try:
    input = raw_input
except NameError:
    pass


cwd = os.getcwd()


# helpers
def cast_list(val):
    return [val] if type(val) is not list else val

def exec_command(command, cwd = None, sync = True):
    logger.debug('Executing command: {}'.format(command))
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    if sync is True:
        return p.communicate()

    stdout = ''
    while(True):
        retcode = p.poll()
        line = p.stdout.readline()
        stdout += line
        logger.info(line)
        if(retcode is not None):
            break
    return (stdout, None)

def bold(string):
    return '\033[1m{}\033[0m'.format(string)


def load_json(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)

def load_js(file_name):
    res = exec_command('node -p "JSON.stringify(require(\'{}\'))"'.format(file_name))
    return json.loads(res[0])


def find_files(file_patterns, ignore_patterns, cwd = os.getcwd()):
    files = []
    this_dir = os.path.join(cwd, '')
    for root, dirnames, filenames in os.walk(this_dir):
        dirname = os.path.join(root, '').replace(this_dir, '')
        for filename in filenames:
            files.append(os.path.join(dirname, filename))

    files_to_add = []
    for pattern in file_patterns:
        files_to_add.extend(fnmatch.filter(files, pattern))

    files_to_ignore = []
    for pattern in ignore_patterns:
        files_to_ignore.extend(fnmatch.filter(files, pattern))

    return list(set(files_to_add) - set(files_to_ignore))

def ensure_directories(file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    return file_name


def copy_files(files, target, cwd = os.getcwd(), map_dirs = {}):
    for file_name in cast_list(files):
        file_name_new = file_name
        for source_dir, target_dir in map_dirs.items():
            source_dir_regex = r'^{}'.format(os.path.join(source_dir, ''))
            if re.match(source_dir_regex, file_name):
                file_name_new = os.path.normpath(re.sub(source_dir_regex, os.path.join(target_dir, ''), file_name))
        dest = os.path.join(target, file_name_new)
        ensure_directories(dest)
        source = os.path.join(cwd, file_name)
        logger.debug('{} -> {}'.format(source, dest))
        shutil.copy(source, dest)



# load/process config
config_paths = [
  {
    'fileName': 'packer.config.json',
    'load': load_json
  },
  {
    'fileName': 'packer.config.js',
    'load': load_js
  },
]

DEFAULT_CONFIG = {
    'files': ['*'],
    'ignore': [],
    'dependencies': [],
    'zipName': 'lambda.zip'
}

def load_config(cwd=cwd):
    for item in config_paths:
        file_name = item['fileName']
        file_path = os.path.join(cwd, file_name)
        if os.path.isfile(file_path):
            logger.info('Using config: {}'.format(file_path))
            return item['load'](file_path)

    logger.info('Could not find packer config. Using default')
    return {}

def enhance_config(config):
    configs = cast_list(config)
    enhanced_configs = []

    for item in configs:
        enhanced_config = {}
        enhanced_config.update(DEFAULT_CONFIG)
        enhanced_config.update(item)

        enhanced_config.update({
            'files': cast_list(enhanced_config['files']),
            'ignore': cast_list(enhanced_config['ignore']),
            'dependencies': cast_list(enhanced_config['dependencies']),
            'tempDir': tempfile.mkdtemp() if 'tempDir' not in enhanced_config else enhanced_config['tempDir']
        })

        enhanced_configs.append(enhanced_config)

    return enhanced_configs





# install stuff

environmentConfigs = {
    'python': {
        'mostCommonExtensions': ['py'],
        'defaultDependencyFile': 'requirements.txt',
        'installCommands': {
            'installDependencies': 'pip install --upgrade {dependencies} -t ./',
            'installDependencyFile': [
                'cp {dependencyFile} requirements.txt',
                'pip install -r requirements.txt -t ./'
            ],
        }
    },
    'node': {
        'mostCommonExtensions': ['js'],
        'defaultDependencyFile': 'package.json',
        'installCommands': {
            'installDependencies': 'npm install {dependencies}',
            'installDependencyFile': [
                'cp {dependencyFile} package.json',
                'npm install --production'
            ],
        }
    },
}

def install_dependencies(config):
    environment = config['environment']
    environment_config = environment if type(environment) is dict else environmentConfigs[environment]['installCommands']
    commands = []
    if 'dependencyFile' in config:
        commands = cast_list(environment_config['installDependencyFile'])
    elif len(config['dependencies']) > 0:
        commands = cast_list(environment_config['installDependencies'])

    for command in commands:
        values = {
            'dependencies': ' '.join(config['dependencies']),
            'dependencyFile': config.get('dependencyFile', '')
        }
        formatted_command = command.format(**values)
        res = exec_command(formatted_command, cwd = config['tempDir'], sync = False)


def archive_directory(path, output_file):
    shutil.make_archive(
      output_file.replace('.zip', ''), 'zip', root_dir=path, base_dir='.'
    )


# build flow
def process_config(config):
    files = find_files(config['files'], config['ignore'])
    logger.info('Found {} files to copy'.format(len(files)))
    logger.info('Copying files to temp dir: {}'.format(config['tempDir']))
    copy_files(files, config['tempDir'], map_dirs = config.get('mapDirectories', {}))
    logger.info('Installing dependencies:'.format(config['tempDir']))
    install_dependencies(config)
    archive_directory(config['tempDir'], config['zipName'])
    logger.info('Built output archive to: {}'.format(config['zipName']))


def better_input(question, default_value = None):
    prepared_default = '({})'.format(bold(default_value)) if default_value is not None else ''
    val = input('{}: {} '.format(question, prepared_default))
    if val == '' and default_value != '':
        return default_value
    return val


# programm
if __name__ == '__main__':

    parser=argparse.ArgumentParser()

    parser.add_argument('--init', action="store_true", help='Interactively create a packer config file')
    parser.add_argument('-V', '--verbose', action="store_true", help='Increase output verbosity')

    args = parser.parse_args()

    if args.init is True:
        print('This utility will create a packeger configuration file')

        available_environments = environmentConfigs.keys()

        extensions = [x.split('.')[-1] for x in find_files(['*.*'], [])]
        most_common_extension = max(set(extensions), key=extensions.count) if extensions else None
        environment_prediction = None
        for environment_name, config in environmentConfigs.items():
            if most_common_extension in config['mostCommonExtensions']:
                environment_prediction = environment_name
                break
        while True:
            environment = better_input(
                    'environment [{}]'.format(' / '.join(available_environments)),
                    environment_prediction
            )
            if environment in available_environments:
                break
            print('please select one of the available environments')

        zip_name = better_input('zip name', DEFAULT_CONFIG['zipName'])

        config = DEFAULT_CONFIG.copy()
        config.update(DEFAULT_CONFIG)
        config.update({
            'environment': environment,
            'zipName': zip_name
        })

        file_name = os.path.join(cwd, 'packer.config.json')
        with open(file_name, 'w') as f:
            f.write(json.dumps(config, indent = 2))
            print('Saved config to {}'.format(file_name))

        exit()

    verbose = args.verbose

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s\n'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if verbose is True else logging.INFO)

    logger.debug('searching for packer config in {}'.format(cwd))
    user_config = load_config(cwd)
    logger.debug('packer config:\n{}'.format(json.dumps(user_config, indent = 4)))

    configs = enhance_config(user_config)

    for index, config in enumerate(configs):
        logger.info('processing config item #{}'.format(index + 1))
        process_config(config)

