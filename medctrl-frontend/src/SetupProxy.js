const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {

  if(process.env.REACT_APP_RDR_DEV) {
    app.use(
      '/api',
      createProxyMiddleware({
        target: 'https://med-ctrl.science.uu.nl/dev',
        changeOrigin: true,
      })
    )
  }
  else {
    app.use(
      '/api',
      createProxyMiddleware({
        target: 'http://localhost:8000',
        changeOrigin: true,
      })
    )
  }


}
