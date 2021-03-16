const path = require("path");
const RemovePlugin = require('remove-files-webpack-plugin');
const frontSassEntries = require('./static_src/front/sass/webpack.entries.config');
const tsEntries = [
    //admin
    "admin/ts/admin-form-script.ts",
    //'admin/ts/sidebar.ts',
    'ckeditor/content_templates/editor-templates.ts',
    //front
    'front/ts/index.ts',
    'front/ts/window-height.ts'
]

const sassEntries = [
    //backend
    "admin/css/admin.scss",
    'admin/css/login.scss',
    'admin/css/ckeditor-content.scss',

    'ckeditor/ckeditor/skins/prestige/editor.scss',
    'ckeditor/ckeditor/skins/prestige/editor_gecko.scss',
    'ckeditor/ckeditor/skins/prestige/editor_ie.scss',
    'ckeditor/ckeditor/skins/prestige/editor_ie8.scss',
    'ckeditor/ckeditor/skins/prestige/editor_iequirks.scss',

    'ckeditor/galleriffic/css/galleriffic-2.scss',
    //front
    // 'front/css/index.scss',
    // 'front/css/projects.scss',
    // 'front/css/project.scss',

    ...frontSassEntries,
    // 'front/sass/pages/common.scss',
    // 'front/sass/pages/index.scss',
]

module.exports = [
    {
    mode: 'production',
    entry: transformEntries(tsEntries),
    output:{
        path: path.resolve(__dirname, 'static_compiled'),
        filename: "[name].js"
    },
    resolve: {
        extensions: ['.ts', '.js', '.json']
    },
    module: {
        rules: [
            {
                // Include ts, tsx, js, and jsx files.
                test: /\.(ts|js)x?$/,
                exclude: [/node_modules/],
                use: [{
                    loader: 'ts-loader',
                    options: {}
                }]
            },
            {
                test: /\.template.html$/,
                use: [{
                    loader: 'raw-loader',
                    options: {
                        esModule: false,
                    },
                }]
            }
        ],
    },
},
    {
    mode: 'production',
    entry: transformEntries(sassEntries),
    output:{
        path: path.resolve(__dirname, 'static_compiled'),
        assetModuleFilename: pathData =>
            pathData.filename.replace('static_src', '')
                .replace('.scss', '.css')
                .replace("sass", "css"),
        filename: "[name]-to-remove.js"
    },
    plugins:[
        new RemovePlugin({
            after: {
                test: [{
                    folder:  path.resolve(__dirname, 'static_compiled'),
                    recursive: true,
                    method: absoluteItemPath => /-to-remove.js$/.test(absoluteItemPath)
                }],
            }
        }),
    ],
    resolve: {
        alias: {
            "@": path.resolve(__dirname),
            "@common": path.resolve(__dirname, "static_src", "common_css"),
            "@front": path.resolve(__dirname, "static_src", "front", "css"),
            "@sass": path.resolve(__dirname, "static_src", "front", "sass"),
        }
    },
    module: {
        rules: [{
            test: /\.s[ac]ss?$/,
            type: 'asset/resource',
            use: [
              "extract-loader",
            {
                loader: 'css-loader',
                options: {
                    url: (assetPath, filePath) => (/.svg/.test(assetPath) && /front/.test(filePath)),
                    modules: false,
                    import: false,
                }
            },
            {
                loader: "postcss-loader",
                options: {
                    postcssOptions: {
                        plugins: [
                            [
                                "postcss-preset-env",
                                require('autoprefixer')
                            ],
                        ],
                    },
                }
            }, {
                loader: 'sass-loader',
                options: {
                    webpackImporter: true,
                    implementation: require('sass'),
                }
            }]
        },
            {
            test: /\.svg/,
            use: {
                loader: "svg-url-loader",
                options: {
                    encoding: "base64",
                    iesafe: true,
                }
            },
        }
        ]
    },

}]

function transformEntries(entries){
    return entries.reduce((acc, path) => {
        const key =
            path.split("/")
                .map(part => part === "ts" ? "js" : part)
                .join("/")
                .replace(/.ts|.tsx|.scss|.sass$/, "")
        return {
            ...acc,
            [key]: "./static_src/" + path
        }
    }, {})
}