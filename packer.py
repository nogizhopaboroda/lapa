# TODO: handle upper level files in config, e.g. { files: ['../*.py'] }


import fnmatch
import os
import json
import tempfile



try:
    input = raw_input
except NameError:
    pass


# run shell commands
# import subprocess

# p = subprocess.Popen('ls -la', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/var/folders/jg/c8j3dyfx3h3bfnk_z538x24m5xj24d/T/1iLhKb')
# for line in p.stdout.readlines():
    # print line,
# retval = p.wait()


#read node config
# node -p "JSON.stringify(require('`pwd`/packer.config.js'))"




cwd = os.getcwd()

this_dir = os.path.join(cwd, '')


# helpers
def cast_list(val):
    return [val] if type(val) is not list else val


#config functions

def load_json(file_name):
    with open(file_name) as json_file:
        return json.load(json_file)

config_paths = [
  # {
    # 'fileName': 'packer.config.js',
    # 'load': load_json
  # },
  {
    'fileName': 'packer.config.json',
    'load': load_json
  },
  # {
    # 'fileName': 'packer.config.yml',
    # # load: (fileName) => {/* load yml */}
  # }
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


def process_config(config):
    files = []
    for root, dirnames, filenames in os.walk(this_dir):
        dirname = os.path.join(root, '').replace(this_dir, '')
        for filename in filenames:
            files.append(os.path.join(dirname, filename))

    files_to_add = []
    for pattern in config['files']:
        files_to_add.extend(fnmatch.filter(files, pattern))

    files_to_ignore = []
    for pattern in config['ignore']:
        files_to_ignore.extend(fnmatch.filter(files, pattern))

    files_to_copy = list(set(files_to_add) - set(files_to_ignore))

    for x in files_to_copy:
        print(x)



configs = enhance_config(load_config())

for index, config in enumerate(configs):
    print('processing config #{}'.format(index))
    process_config(config)
