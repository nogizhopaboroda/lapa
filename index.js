const path = require('path');
const os = require('os');

const loadConfig = require('./load-config');
const { findFiles, copyFile, mkTempDir, exec, getCwd } = require('./helpers');


const environmentConfigs = {
  python: {
    installDependencies(dependencies){
      return `pip install --prefix=./ ${dependencies.join(' ')}`;
    },
    installDependencyFile(file){
      return [
        `cp ${file} requirements.txt`,
        `pip install --prefix=./ -r requirements.txt`
      ];
    }
  },
  node: {
    installDependencies(dependencies){
      return `npm install ${dependencies.join(' ')}`;
    },
    installDependencyFile(file){
      return [
        `cp ${file} package.json`,
        `npm install`
      ];
    }
  }
}


const processConfig = (config, index) => { //maybe rename it
  return Promise.resolve(config)
    .then((config) => {
      return mkTempDir(`${os.tmpdir()}${path.sep}`).then((folderName) => {
        return Object.assign(config, {
          tempDir: folderName
        });
      });
    })
    .then((config) => {
      const filesPromise = findFiles(`*(${config.files.join('|')})`, { matchBase: true, ignore: config.ignore });
      const copyFilesPromise = filesPromise.then((files) => Promise.all(files.map((file) => copyFile(file, path.join(config.tempDir, file)))));
      return copyFilesPromise.then(() => config);
    })
    .then((config) => {
      const commands = [].concat(environmentConfigs[config.environment].installDependencies(config.dependencies));
      const commandsPromise = commands.reduce((acc, command) => {
        return acc.then(() => exec(command, { cwd: config.tempDir }));
      }, Promise.resolve());
      commandsPromise.then(console.log);
      console.log(config);
      return config;
    })
    .then(() => 'processed config #' + index)
}

Promise.resolve(true)
  .then(loadConfig)
  .then((configs) => Promise.all(configs.map(processConfig)))
  .then(console.log)

