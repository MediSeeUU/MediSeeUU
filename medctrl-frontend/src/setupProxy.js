const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'https://med-ctrl.science.uu.nl/dev',
      changeOrigin: true,
    })
  )
}
