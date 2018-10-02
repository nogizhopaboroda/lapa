import fnmatch
import os



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


# create temp directory
# import tempfile
# foo = tempfile.mkdtemp()
# print(foo)


#read node config
# node -p "JSON.stringify(require('`pwd`/packer.config.js'))"




cwd = os.getcwd()

this_dir = os.path.join(cwd, '')



config = [{
  "files": ['*.py'],
  # //dependenciesFile: 'package.json|requirements.txt',
  "dependencies": ['requests'], #optional, replacing dependenciesFile
  # //excludeDependencies: [], //optional, replacing dependenciesFile
  "ignore": ['secrets_backup.py', 'lib/**', 'deps/**', 'bin/**'],
  # //include: [],
  "environment": 'python',
  # //dist: '<filder>',
  "zipName": 'example_lambda.zip', #optional take package.json name or directory name
}]


files = []
for root, dirnames, filenames in os.walk(this_dir):
    dirname = os.path.join(root, '').replace(this_dir, '')
    for filename in filenames:
        files.append(os.path.join(dirname, filename))

files_to_add = []
for pattern in config[0]['files']:
    files_to_add.extend(fnmatch.filter(files, pattern))

files_to_ignore = []
for pattern in config[0]['ignore']:
    files_to_ignore.extend(fnmatch.filter(files, pattern))

files_to_copy = list(set(files_to_add) - set(files_to_ignore))

for x in files_to_copy:
    print(x)
