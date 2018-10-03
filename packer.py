# TODO: handle upper level files in config, e.g. { files: ['../*.py'] }


import fnmatch
import os
import json
import tempfile
import subprocess
import shutil



try:
    input = raw_input
except NameError:
    pass


cwd = os.getcwd()

this_dir = os.path.join(cwd, '')


# helpers
def cast_list(val):
    return [val] if type(val) is not list else val

def exec_command(command, cwd = None, silent = True):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
    return p.communicate()


def load_json(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)

def load_js(file_name):
    res = exec_command('node -p "JSON.stringify(require(\'./{}\'))"'.format(file_name))
    return json.loads(res[0])


def find_files(file_patterns, ignore_patterns):
    files = []
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


def copy_files(files, target):
    for file_name in cast_list(files):
        dest = os.path.join(target, file_name)
        ensure_directories(dest)
        shutil.copy(file_name, dest)



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

def load_config():
    for item in config_paths:
        file_name = item['fileName']
        if os.path.isfile(file_name):
            return item['load'](file_name)

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
        'install_dependencies': 'pip install --prefix=./ {dependencies}',
        'install_dependency_file': [
            'cp {dependency_file} requirements.txt',
            'pip install --prefix=./ -r requirements.txt'
        ],
    },
    'node': {
        'install_dependencies': 'npm install {dependencies}',
        'install_dependency_file': [
            'cp {dependency_file} package.json',
            'npm install'
        ],
    },
}

def install_dependencies(config):
    environment = config['environment']
    commands = []
    if 'dependencyFile' in config:
        commands = cast_list(environmentConfigs[environment]['install_dependency_file'])
    elif 'dependencies' in config:
        commands = cast_list(environmentConfigs[environment]['install_dependencies'])

    for command in commands:
        values = {
            'dependencies': ' '.join(config['dependencies']),
            'dependency_file': config.get('dependencyFile', '')
        }
        res = exec_command(command.format(**values), cwd = config['tempDir'])
        print(res[0])


def archive_directory(path, output_file):
    shutil.make_archive(
      output_file.replace('.zip', ''), 'zip', root_dir=path, base_dir='.'
    )


# build flow
def process_config(config):
    copy_files(find_files(config['files'], config['ignore']), config['tempDir'])
    install_dependencies(config)
    archive_directory(config['tempDir'], config['zipName'])


#programm
if __name__ == '__main__':

    configs = enhance_config(load_config())

    for index, config in enumerate(configs):
        print('processing config #{}'.format(index))
        print(config)
        process_config(config)
