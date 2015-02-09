
bodyParser = require('body-parser')
express    = require('express')
fs         = require('fs')
logger     = require('morgan')
serve      = require('serve-static')
spdy       = require('spdy')

sys = require('sys')
spawn = require('child_process').spawn

# Serve build/
app = express()
  .use(logger('dev'))
  .use(bodyParser.text())
  .use(bodyParser.json())
  .use(serve('./demo/'))

app.post('/toJson', (req, resp) ->
  child = spawn("#{__dirname}/../bin/toJson")
  resp.type('json')

  child.stdout.on('data', (data) ->
    console.log "data received", data
    resp.send(data.toString('utf-8'))
  )

  child.on('error', () -> console.log "err", arguments)
  child.stdout.on('end', ->
    child.kill('SIGTERM')
  )

  child.stdin.setEncoding = 'utf-8'
  child.stdin.write(req.body)
  child.stdin.end()
)

app.post('/toMd', (req, resp) ->
  child = spawn("#{__dirname}/../bin/toMd")

  resp.type('text')

  child.stdout.on('data', (data) ->
    console.log "data received", data
    resp.send(data.toString('utf-8'))
  )

  child.on('error', () -> console.log "err", arguments)

  child.stdout.on('end', ->
    child.kill('SIGTERM')
  )

  child.stdin.setEncoding = 'utf-8'
  child.stdin.write(JSON.stringify(req.body))
  child.stdin.end()
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
