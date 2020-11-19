const path = require('path');

module.exports = (env, argv) =>({
    entry: './src/app.js',
    output: {
        path: path.join(__dirname, 'public'),
        filename: 'bundle.js',
    },
    module:{
        rules:[{
            test: /\.js$/,
            exclude: '/node_modules/',
            loader: 'babel-loader',
        }]
    },
    devtool: env === 'production' ? 'source-map':'eval-cheap-module-source-map',
    devServer: {
        port:8081,
        contentBase: path.join(__dirname, 'public'),
        historyApiFallback: true
    }
});