const config = require('config')
const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const WriteFilePlugin = require('write-file-webpack-plugin')

const os = require('os')
const ifaces = os.networkInterfaces()

function getHostIp () {
  Object.keys(ifaces).forEach(function (ifname) {
    let alias = 0

    ifaces[ifname].forEach(function (iface) {
      if ('IPv4' !== iface.family || iface.internal !== false) {
        // skip over internal (i.e. 127.0.0.1) and non-ipv4 addresses
        return
      }

      if (alias >= 1) {
        // this single interface has multiple ipv4 addresses
        console.log('HOST: ' + ifname + ':' + alias, iface.address)
        return iface.address
      } else {
        // this interface has only one ipv4 adress
        console.log('HOST: ' + ifname, iface.address)
        return iface.address
      }
      ++alias
    })
  })
}

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
        host: getHostIp(),
        watchOptions: {
            poll: config.get("vagrantShared"),
            ignored: /node_modules/
        }
    },
    baseUrl: config.get("baseUrl")
}
