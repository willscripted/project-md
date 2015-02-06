
bodyParser = require('body-parser')
express    = require('express')
fs         = require('fs')
logger     = require('morgan')
serve      = require('serve-static')
spdy       = require('spdy')

# Serve build/
app = express()
  .use(logger('dev'))
  .use(bodyParser.text())
  .use(bodyParser.json())
  .use(serve('./demo/'))

app.post('/project-md', (req, resp) ->
  sys = require('sys')
  spawn = require('child_process').spawn

  child = spawn("#{__dirname}/../bin/project-md")
  child.stdout.on('data', (data) ->
    resp.send(data)
    child.kill('SIGTERM')
  )
  child.on('error', () -> console.log "err", arguments)

  child.stdin.setEncoding = 'utf-8'
  child.stdin.write(req.body)
)

options = {
  key: fs.readFileSync("#{__dirname}/certs/server.key"),
  cert: fs.readFileSync("#{__dirname}/certs/server.crt"),
  ca: fs.readFileSync("#{__dirname}/certs/server.csr")
}

server = spdy.createServer(options, app)

port = process.env.PORT || 3333
server.listen(port)

console.log("listening on port #{port}")
