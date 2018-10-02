const path = require('path');
const os = require('os');

const loadConfig = require('./load-config');
const { findFiles, copyFile, mkTempDir, getCwd } = require('./helpers');


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
      console.log(config);
      return config;
    })
    .then(() => 'processed config #' + index)
}

Promise.resolve(true)
  .then(loadConfig)
  .then((configs) => Promise.all(configs.map(processConfig)))
  .then(console.log)



//console.log(config);
////console.log(process.cwd());
////exec('pip --version', (err, stdout, stderr) => {
  ////if (err) {
    ////// node couldn't execute the command
    ////return;
  ////}

  ////// the *entire* stdout and stderr (buffered)
  ////console.log(`stdout: ${stdout}`);
  ////console.log(`stderr: ${stderr}`);
////});
////

