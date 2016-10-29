module.exports = {
    entry: './application/dashboard.ts',
    output: {
        path: './www',
        filename: 'app.bundle.js'
    },
    resolve: {
        extensions: ['', '.webpack.js', '.web.js', '.ts', '.js']
    },
    module: {
        loaders: [
            { test: /\.ts$/, loader: 'ts-loader' }
        ]
    }
};