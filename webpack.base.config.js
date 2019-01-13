const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
    entry: './frontend/js/index.js',
    output: {
        path: path.resolve(__dirname, './static/bundles/'),
        filename: '[name]-[hash].js'
    },
    module: {
        rules: [
            { test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader' }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(['static/bundles'], { watch: true }),
        new BundleTracker({ filename: './webpack-stats.json' }),
    ]
};
