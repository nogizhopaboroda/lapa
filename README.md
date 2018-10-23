# lapa
(Almost) universal AWS Lambda packager.
It generates zip archive ready for uploading on AWS with no pain using just a simple config file.

Supports `node` and `python` out of the box, can be customised for other environments.


## Configuration

### Config file

A config file is either plain json file (`packer.config.json`) or js module (`packer.config.js`) that exports configuration object.


example `packer.config.json`:
```js
{
  "environment": "python",
  "files": ["*.py", "*.ini"],
  "ignore": ["lib/*", "bin/*"],
  "dependencies": ["requests"],
  "zipName": "./dist/my-lambda.zip"
}
```

example `packer.config.js`:
```js
//packer.config.js

//js configs are treated as regular js modules,
//so you can use variables, require another modules and so on
const common = {
  "environment": "node",
  "files": "*",
  "ignore": ["node_modules/*"]
}

module.exports = [
  {
    ...common,
    "dependencyFile": "package.json",
    "zipName": "./dist/my-lambda.zip"
  },
  {
    ...common,
    "dependencyFile": "edge.package.json",
    "zipName": "./dist/my-edge-lambda.zip"
  },
]
```

### Configuration object

```js
{ //can be an array (for multiple builds)
  "environment": <String|Object>,

  //optional fields
  "files": <String|Array>,
  "ignore": <String|Array>,
  "dependencyFile": <String>,
  "dependencies": <String|Array>,
  "zipName": <String>,
  "mapDirectories": <Object>
}
```

#### Required fields

`environment`:

environment to use when install dependencies. So far only `node` and `python` are supperted.

*Can also be an object of dependencies installation instructions. In such case:*

```js
{
  "environment": {
    "installDependencies": "some-bundler install {dependencies}",
    "installDependencyFile": [
      "some-bundler install {dependencyFile}"
    ],
  }
}
```
where

`{dependencies}` - space-separated dependencies from config object

`{dependencyFile}` - dependency file from config object

#### Optional fields

`files` (Default: `[*]`):

file/directory masks to include to archive

`ignore` (Default: `[]`):

file/directory masks to ignore

`dependencyFile`:

file to use as a dependency file

`dependencies` (Default: `[]`):

list of dependencies

`zipName` (Default: `lambda.zip`):

output archive name

`mapDirectories`:

Change file directory in resulting archive. Example:

```js
{
  //  src/a.js -> a.js
  //  b.js     -> b.js
  "mapDirectories": {
    "src": "./"
  }
}
```

### Generate a basic configuration file

You can create config file in interactive mode

```sh
lapa --init
```

App will ask you several questions and try to guess you environment based on most common files type


## Installation

#### manual

```sh
curl https://raw.githubusercontent.com/nogizhopaboroda/lapa/master/packer.py -o /usr/local/bin/lapa && chmod +x /usr/local/bin/lapa
```

#### with npm

```sh
npm i -g https://github.com/nogizhopaboroda/lapa
```

#### as a local node dependency
```sh
npm i --save-dev https://github.com/nogizhopaboroda/lapa
```

then in package.json:

```js
{
  ...
  "scripts": {
    "pack": "lapa"
  }
  ...
}
```

#### Usage directly from github

```sh
python <(curl https://raw.githubusercontent.com/nogizhopaboroda/lapa/master/packer.py) [arguments]
```


## Examples

- [simple python project](./example/python/simple/)
- [simple node project](./example/node/simple/)
- [node project with 2 configs (lambda + edge)](./example/node/simple/)
- [simple python project with requirements.txt](./example/python/with_requirements_txt/)

## Troubleshooting

##### Pip can't install dependencies in specific directory

It's known issue if your `pip` is installed via brew. As a workaround just copy [this setup.cfg file](./example/python/simple/setup.cfg) in your project on root level as [in this example](./example/python/simple/)
