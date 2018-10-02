# import os
# import glob

# for filename in glob.glob('lib/**', recursive=True):
    # print(filename)






# import os, fnmatch

# def find_files(directory, pattern='*'):
    # if not os.path.exists(directory):
        # raise ValueError("Directory not found {}".format(directory))

    # matches = []
    # for root, dirnames, filenames in os.walk(directory):
        # for filename in filenames:
            # full_path = os.path.join(root, filename)
            # if fnmatch.filter([full_path], pattern):
                # matches.append(os.path.join(root, filename))
    # return matches

# print(find_files('.', './lib/**'))





# import fnmatch
# import os

# matches = []
# for root, dirnames, filenames in os.walk('./'):
    # for filename in fnmatch.filter(filenames, './lib/**'):
        # matches.append(os.path.join(root, filename))




# import fnmatch
# fnmatch.filter(['./foo.js', 'lib/hh.js'], 'lib/*')




import fnmatch
import os

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
  "zipName": './example_lambda.zip', #optional take package.json name or directory name
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

print(list(set(files_to_add) - set(files_to_ignore)))
