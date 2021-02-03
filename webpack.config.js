const path = require("path");


const entries = [
    "admin/ts/form.ts"
].reduce((acc, path) => {
    const key =
        path.split("/")
        .map(part => part === "ts" ? "js" : part)
        .join("/")
        .replace(/.ts|.tsx$/, "")
    return {
        ...acc,
        [key]: "./static_src/" + path
    }
}, {})

module.exports = {
    mode: 'production',
    entry: entries,
    output:{
        path: path.resolve(__dirname, 'static_compiled'),
        filename: "[name].js"
    },
    module: {
        rules: [{
            // Include ts, tsx, js, and jsx files.
            test: /\.(ts|js)x?$/,
            exclude: [/node_modules/],
            use: [{
                loader: 'ts-loader',
                options: {}
            }]
        }],
    },
}
