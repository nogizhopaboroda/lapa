# TODO: handle upper level files in config, e.g. { files: ['../*.py'] }


import fnmatch
import os
import json
import tempfile
import subprocess



try:
    input = raw_input
except NameError:
    pass





#read node config
# node -p "JSON.stringify(require('`pwd`/packer.config.js'))"




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

# print('---')
# print(load_js('packer.config.js'))
# print(load_json('packer.config.json'))

# exit()

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

def load_config():
    for item in config_paths:
        file_name = item['fileName']
        if os.path.isfile(file_name):
            return item['load'](file_name)

    return {}



DEFAULT_CONFIG = {
    'files': ['*'],
    'ignore': [],
    'zipName': 'lambda.zip'
}

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
            'tempDir': tempfile.mkdtemp() if 'tempDir' not in enhanced_config else enhanced_config['tempDir']
        })

        enhanced_configs.append(enhanced_config)

    return enhanced_configs


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


def process_config(config):
    for x in find_files(config['files'], config['ignore']):
        print(x)



configs = enhance_config(load_config())

for index, config in enumerate(configs):
    print('processing config #{}'.format(index))
    process_config(config)
