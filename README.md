# lapa
universal lambda packager


## Configuration

```js
{
  "environment": <String>,

  //optional fields
  "files": <String|Array>,
  "ignore": <String|Array>,
  "dependencyFile": <String>,
  "dependencies": <String|Array>,
  "zipName": <String>,
  "mapDirectories": <Object>,
  "tempDir": <String>
}
```

`environment`: environment to use when install dependencies

`files`: file/directory masks to include to archive

`ignore`: file/directory masks to ignore

`dependencyFile`: file to use as a dependency file

`dependencies`: list of dependencies

`zipName`: output archive name

`mapDirectories`: remap directories in resulting archive

`tempDir`: temporary directory to use for building project

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

#### Usage directly from github

```sh
python <(curl https://raw.githubusercontent.com/nogizhopaboroda/lapa/master/packer.py) [arguments]
```

## Examples

## Troubleshooting

## Issues
