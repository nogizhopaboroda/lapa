const COMMON_CONFIG = {
  "files": ["*.js", "*.json"],
  "ignore": ["node_modules/*"],
  "environment": "node",
  "mapDirectories": {
    "src": "./"
  }
}

module.exports = [{
  "dependencyFile": "package.json",
  "zipName": "./dist/lambda.zip"
}, {
  "dependencyFile": "edge.package.json",
  "zipName": "./dist/edge.zip"
}].map((extend) => Object.assign({}, COMMON_CONFIG, extend))

