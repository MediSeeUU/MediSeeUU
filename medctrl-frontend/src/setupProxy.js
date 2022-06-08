// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  if (process.env.REACT_APP_RDR_DEV) {
    app.use(
      '/api',
      createProxyMiddleware({
        target: 'https://med-ctrl.science.uu.nl/dev',
        changeOrigin: true,
      })
    )
  } else {
    app.use(
      '/api',
      createProxyMiddleware({
        target: 'http://localhost:8000',
        changeOrigin: true,
      })
    )
  }
}
