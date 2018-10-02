const glob = require("glob");
const promisify = require("promisify-node");
const path = require('path');
const fs = require('fs');
const os = require('os');
const childProcess = require('child_process');


function exec(cmd, opts) {
    opts || (opts = {});
    return new Promise((resolve, reject) => {
        const child = childProcess.exec(cmd, opts,
            (err, stdout, stderr) => err ? reject(err) : resolve({
                stdout: stdout,
                stderr: stderr
            }));

        if (opts.stdout) {
            child.stdout.pipe(opts.stdout);
        }
        if (opts.stderr) {
            child.stderr.pipe(opts.stderr);
        }
    });
}


const cwd = process.cwd();


module.exports = {
  stat: promisify(fs.stat),
  copyFile: promisify(fs.copyFile),
  rmDir: promisify(fs.rmdir),
  mkDir: promisify(fs.mkdir),
  mkTempDir: promisify(fs.mkdtemp),
  findFiles: promisify(glob),
  exec: exec,
  getCwd: () => cwd,
}
