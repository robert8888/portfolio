const BundleTracker = require("webpack-bundle-tracker");

const pages = {
    main: {
        entry: 'src/main.ts',
        chunks: ['chunk-vendors'],
    },
}
console.log("------------------------- node env in dept ------------------",  process.env.NODE_ENV)

module.exports = {
    pages: pages,
    filenameHashing: false,
    productionSourceMap: false,
    publicPath: process.env.NODE_ENV === 'production'
        ? ''
        : 'http://localhost:8080/',

    outputDir: '../../portfolio/static_compiled/vue/',
    runtimeCompiler: true,

    chainWebpack: config => {

        config.optimization
            .splitChunks({
                cacheGroups: {
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: "chunk-vendors",
                        chunks: "all",
                        priority: 1
                    },
                },
            });

        Object.keys(pages).forEach(page => {
            config.plugins.delete(`html-${page}`);
            config.plugins.delete(`preload-${page}`);
            config.plugins.delete(`prefetch-${page}`);
        })

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: '../components_src/webpack-stats.json'}]);

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