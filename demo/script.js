
var request = superagent;

var pprint = function(json){
  return JSON.stringify(json, null, 2);
};

var View = Ractive.extend({
  template: "#format-template",
  init: function(){
    this.observe('entry', function(entry){
      request
        .post('/project-md')
        .set('Content-Type', 'text/plain')
        .send(entry)
        .end(function(resp){
          this.set('json', pprint(resp.body));
        }.bind(this));
    });
  }
});

var view = new View({
  el: "#page",
  data: {
    entry: document.getElementById('demo-data').innerHTML
  }
});
