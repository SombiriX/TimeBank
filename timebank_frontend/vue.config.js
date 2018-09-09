const config = require('config')
const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const WriteFilePlugin = require('write-file-webpack-plugin')

module.exports = {
    configureWebpack: {
        // Merged into the final Webpack config
        plugins: [
            new BundleTracker({filename: "./webpack-stats.json"}),
            new WriteFilePlugin()
        ],
        entry: "./src/main.js",
        output: {
            filename: "bundle.js"
        },
    },
    devServer: {
        watchOptions: {
            poll: config.get("vagrantShared"),
            ignored: /node_modules/
        }
    },
    baseUrl: config.get("baseUrl")
}
