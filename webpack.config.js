const path = require("path");

module.exports = {
  mode: "development", // or 'production' based on your needs
  entry: {
    account: "./account/static/account/js/account.js", // Entry point for the account app
    employer: "./employer/static/employer/js/employer. js", // Entry point for the employer app
  },
  output: {
    filename: "bundle.js",
    path: path.resolve(__dirname, "static/dist"), // Where you want Webpack to output the bundle
    publicPath: "/static/dist/",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
    ],
  },
  devServer: {
    contentBase: path.resolve(__dirname, "static"),
    hot: true,
    watchContentBase: true,
    port: 8080,
    proxy: {
      "/": "http://localhost:8000", // Proxy Django backend
    },
  },
};


const BrowserSyncPlugin = require("webpack-browser-sync-plugin");

module.exports = {
  // ...rest of your Webpack config
  plugins: [
    new BrowserSyncPlugin(
      {
        proxy: "http://localhost:8000", // Proxy your Django app
        files: ["**/*.css", "**/*.html"], // Watch CSS and HTML changes
        open: false,
        port: 3000, // You can access your app on localhost:3000 with live reload
      },
      { reload: false }
    ),
  ],
};
