
var test = require('tape'),
    fs   = require('fs'),
    _    = require('lodash'),
    path = require('path');

var sys = require('sys'),
    spawnSync = require('child_process').spawnSync;

var invoke = function (args) {
  return function(input){
    var cmd  = path.resolve(__dirname, "../bin/project-md"),
        args = args,
        opts = {input: input},
        results = spawnSync(cmd, args, opts);

    return results.stdout.toString('utf-8');
  };
};

var asClean  = invoke(['-f', 'md',   '-t', 'md'  ]),
    asJSON = invoke(['-f', 'md',   '-t', 'json']),
    asMd   = invoke(['-f', 'json', '-t', 'md'  ]);

test('testing werks', function(t){
  t.plan(1);
  t.equal('aoeu', 'aoeu');
});

// Assert all dirty md converts to correct clean md

var files = fs.readdirSync(__dirname + '/dirtymd');
_.each(files, function(file){

  var opts = {encoding: "utf-8"},
      dirty = fs.readFileSync(__dirname + '/dirtymd/' + file, opts),
      clean = fs.readFileSync(__dirname + '/md/' + file, opts);

  test('cleans '+ file, function(t){
    var msg = "" + file + " [md -> md]";
    t.equal(asClean(dirty), clean, msg);
    t.end();
  });

});


// Assert all clean md converts to json

var files = fs.readdirSync(__dirname + '/md');
_.each(files, function(file){
  var opts  = {encoding: "utf-8"},
      md    = fs.readFileSync(__dirname + '/md/'   + file, opts),
      json  = fs.readFileSync(__dirname + '/json/' + file, opts);

  test('md -> json '+ file, function(t){
    var msg = "" + file + " [md -> json]";
    t.deepEqual(asJSON(md), json, msg);
    t.end();
  });

});

// Assert all json converts back to clean md

var files = fs.readdirSync(__dirname + '/md');
_.each(files, function(file){
  var opts = {encoding: "utf-8"},
      json = fs.readFileSync(__dirname + '/json/' + file, opts),
      md   = fs.readFileSync(__dirname + '/md/'   + file, opts);

  test('json -> md '+ file, function(t){
    var msg = "" + file + " [json -> md]";
    t.equal(asMd(json), md, msg);
    t.end();
  });

});


