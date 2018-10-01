const path = require('path');
const { stat, getCwd } = require('./helpers');


const DEFAULT_CONFIG = {
  ignore: [],
  files: ['*']
}

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
  return stat(fileName).then(() => fileName).catch(() => false);
};

module.exports = () => {
  const configPromise = configPaths.reduce((acc, { fileName, load }) => {
    const file = path.resolve(getCwd(), fileName);
    return acc.then((config) => !!config ? acc : checkFile(file).then((fileName) => {
      return fileName ? load(file) : false;
    }));
  }, Promise.resolve(false));

  return configPromise.then((config) => [].concat(config).map((config) => {
    return Object.assign({}, DEFAULT_CONFIG, config);
  }));
}

