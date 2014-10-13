var apps = apps || {};

(function(apps){
  function Model(){
    this.params =  {"name": "", "age": 0, "description": "", "id": 1};
    this.modifiedHook = [];
  }

  Model.prototype.change = function(k, val){
    this.params[k] = val;
    this.onModified();
  };
  Model.prototype.value = function(){
    return this.params;
  };
  Model.prototype.onModified = function(){
    for(var i=0,j=this.modifiedHook.length;i<j;i++){
      this.modifiedHook[i](this);
    }
  };


  function Gateway(baseurl){
    this.baseurl = baseurl;
  }

  Gateway.prototype.send = function send(method, url, params){
    return $.ajax({
      type: method,
      url: url,
      processData: false,
      contentType: 'application/json',
      data: JSON.stringify(params)
    });
  };

  Gateway.prototype.GET = function(url, params){
    return this.send("GET", url, params);
  };
  Gateway.prototype.POST = function(url, params){
    return this.send("POST", url, params);
  };
  Gateway.prototype.PUT = function(url, params){
    return this.send("PUT", url, params);
  };
  Gateway.prototype.DELETE = function(url, params){
    return this.send("DELETE", url, params);
  };


  function UIView(el, model){
    this.$el = $(el);
    this.model = model;

    var self = this; //hmm
    this.$el.find("input[name='id']").on("input", function(e){
      self.model.change("id", Number.parseInt($(e.currentTarget).val()));
    });
    this.$el.find("input[name='name']").on("input", function(e){
      self.model.change("name", $(e.currentTarget).val());
    });
    this.$el.find("input[name='age']").on("input", function(e){
      self.model.change("age", Number.parseInt($(e.currentTarget).val()));
    });
    this.$el.find("textarea[name='description']").on("input", function(e){
      self.model.change("description", $(e.currentTarget).val());
    });

    this.model.modifiedHook.push(this.onModified.bind(this));
    self.model.onModified();
  }

  UIView.prototype.onModified = function onModified(){
    this.$el.find("pre.input").text(JSON.stringify(this.model.value(), null, 2));
  };

  UIView.prototype.afterAPI = function afterAPI(d){
    d.done(function(data){
      this.$el.find("pre.output").text(JSON.stringify(data, null, 2));
    }.bind(this))
     .fail(function(data){
       this.$el.find("pre.output").text(data.responseText);
     }.bind(this));
  };


  var APIViewFactory = function(api){
    return function APIView(gateway, subview, model){
      this.gateway = gateway;
      this.subview = subview;
      this.model = model;
      this.api = api;
    };
  };

  var CreateAPIView = new APIViewFactory(function(){
    var d = this.gateway.POST(this.gateway.baseurl+"/", this.model.params);
    return this.subview.afterAPI(d);
  });

  var EditAPIView = new APIViewFactory(function(){
    var url = this.gateway.baseurl+"/"+this.model.params.id+"/";
    var d = this.gateway.PUT(url, this.model.params);
    return this.subview.afterAPI(d);
  });

  var ShowAPIView = new APIViewFactory(function(){
    var url = this.gateway.baseurl+"/"+this.model.params.id+"/";
    var d = this.gateway.GET(url, null);
    return this.subview.afterAPI(d);
  });

  var DeleteAPIView = new APIViewFactory(function(){
    var url = this.gateway.baseurl+"/"+this.model.params.id+"/";
    var d = this.gateway.DELETE(url, null);
    return this.subview.afterAPI(d);
  });

  var SchemaAPIView = new APIViewFactory(function(){
    var d = this.gateway.GET(this.gateway.baseurl+"/schema", null);
    return this.subview.afterAPI(d);
  });

  var ListingAPIView = new APIViewFactory(function(){
    var d = this.gateway.GET(this.gateway.baseurl+"/", null);
    return this.subview.afterAPI(d);
  });


  var App = function(el, baseurl){
    this.model = new Model();
    this.gateway = new Gateway(baseurl);
    this.uiview = new UIView(el, this.model);

    this.createAPI = new CreateAPIView(this.gateway, this.uiview, this.model);
    this.uiview.$el.find("button.create").on("click", this.createAPI.api.bind(this.createAPI));
    this.editAPI = new EditAPIView(this.gateway, this.uiview, this.model);
    this.uiview.$el.find("button.edit").on("click", this.editAPI.api.bind(this.editAPI));
    this.showAPI = new ShowAPIView(this.gateway, this.uiview, this.model);
    this.uiview.$el.find("button.show").on("click", this.showAPI.api.bind(this.showAPI));
    this.deleteAPI = new DeleteAPIView(this.gateway, this.uiview, this.model);
    this.uiview.$el.find("button.delete").on("click", this.deleteAPI.api.bind(this.deleteAPI));
    this.schemaAPI = new SchemaAPIView(this.gateway, this.uiview, this.model);
    this.uiview.$el.find("button.schema").on("click", this.schemaAPI.api.bind(this.schemaAPI));
    this.listingAPI = new ListingAPIView(this.gateway, this.uiview, this.model);
    this.uiview.$el.find("button.listing").on("click", this.listingAPI.api.bind(this.listingAPI));
  };
  apps.App = App;
})(apps);
