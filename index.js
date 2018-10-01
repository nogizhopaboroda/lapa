const glob = require("glob");
const promisify = require("promisify-node");
const path = require('path');
const fs = require('fs');
const os = require('os');
const childProcess = require('child_process');


const stat = promisify(fs.stat);
const rmDir = promisify(fs.rmdir);
const mkDir = promisify(fs.mkdir);
const mkTempDir = promisify(fs.mkdtemp);
const findFiles = promisify(glob);


const cwd = process.cwd();


const configPaths = [
  {
    fileName: 'packer.config.js',
    load: require
  },
  {
    fileName: 'packer.config.json',
    load: require
  },
  {
    fileName: 'packer.config.yml',
    load: (fileName) => {/* load yml */}
  }
];

const checkFile = (fileName) => {
  return stat(path.resolve(cwd, fileName)).then(
    () => fileName
  ).catch(
    () => false
  );
};

const loadConfig = () => {
  return configPaths.reduce((acc, { fileName, load }) => {
    return acc.then((config) => !!config ? acc : checkFile(fileName).then((fileName) => {
      return fileName ? load(path.resolve(cwd, fileName)) : false;
    }));
  }, Promise.resolve(false));
}

const DEFAULT_CONFIG = {
  tempDir: `${os.tmpdir()}${path.sep}`,
  exclude: []
}


const processConfig = (config, index) => { //maybe rename it
  return Promise.resolve(config)
    .then((config) => Object.assign({}, DEFAULT_CONFIG, config))
    .then((config) => {
      return mkTempDir(config.tempDir).then(() => config);
    })
    .then((config) => {
      return findFiles(`*(${config.files.join('|')})`, { matchBase: true, ignore: config.ignore }).then((files) => {
        console.log(234, files);
      });
    })
    .then(() => 'processed config #' + index)
}

Promise.resolve(true)
  .then(loadConfig)
  .then((config) => [].concat(config))
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

