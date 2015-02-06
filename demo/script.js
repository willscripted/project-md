
View = Ractive.extend({
  template: "#format-template",
  init: function(){
    this.on('change-entry', function(){
      console.log('changing entry', arguments);
    });
  }

});

demoData = document.getElementById('demo-data').innerHTML;

view = new View({
  el: "#page",
  data: {
    entry: demoData
  }
});
