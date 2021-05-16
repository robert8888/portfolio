// const BundleTracker = require("webpack-bundle-tracker");
const BundleTracker = require("webpack4-bundle-tracker");

const pages = {
    main: {
        entry: 'src/main.ts',
        chunks: ['chunk-vendors', 'chunk-common'],
    },
    projects: {
        entry: 'src/projects.ts',
        chunks: ['chunk-vendors' , 'chunk-common']
    },
    project: {
        entry: 'src/project.ts',
        chunks: ['chunk-vendors', 'chunk-common']
    }
}

module.exports = {
    pages: pages,
    filenameHashing: false,
    productionSourceMap: false,
    publicPath: process.env.NODE_ENV === 'production'
        ? ''
        : 'http://localhost:8080/',

    outputDir: '../static_compiled/vue/',
    runtimeCompiler: true,
    css: {
        extract: { ignoreOrder: true },
    },
    chainWebpack: config => {

        config.optimization
            .splitChunks({
                cacheGroups: {
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: "chunk-vendors",
                        maxSize: 51200 * 4,
                        minSize: 51200 * 2,
                        chunks: "all",
                        priority: 1
                    },
                    common: {
                        name: 'chunk-common',
                        priority: -20,
                        chunks: 'initial',
                        minChunks: 2,
                        reuseExistingChunk: true,
                        enforce: true
                    }
                },
            });

        Object.keys(pages).forEach(page => {
            config.plugins.delete(`html-${page}`);
            config.plugins.delete(`preload-${page}`);
            config.plugins.delete(`prefetch-${page}`);
        })

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: '../vue_components_src/webpack-stats.json'}]);

        config.resolve.alias
            .set('__STATIC__', 'static')
            //.set('vue', '@vue/runtime-dom')

        config.devServer
            .public('http://localhost:8080')
            .host('localhost')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["*"]})

    }
};