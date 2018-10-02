const glob = require("glob");
const promisify = require("promisify-node");
const path = require('path');
const fs = require('fs');
const os = require('os');
const childProcess = require('child_process');


const cwd = process.cwd();


module.exports = {
  stat: promisify(fs.stat),
  copyFile: promisify(fs.copyFile),
  rmDir: promisify(fs.rmdir),
  mkDir: promisify(fs.mkdir),
  mkTempDir: promisify(fs.mkdtemp),
  findFiles: promisify(glob),
  getCwd: () => cwd,
}
