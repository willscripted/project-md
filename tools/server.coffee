express = require('express')
serve = require('serve-static')
logger = require('morgan')
fs = require('fs')
spdy = require('spdy')

# Serve build/
app = express()
  .use(logger('dev'))
  .use(serve('./demo/'))

options = {
  key: fs.readFileSync("#{__dirname}/certs/server.key"),
  cert: fs.readFileSync("#{__dirname}/certs/server.crt"),
  ca: fs.readFileSync("#{__dirname}/certs/server.csr")
}

server = spdy.createServer(options, app)

port = process.env.PORT || 3333
server.listen(port)

console.log("listening on port #{port}")
