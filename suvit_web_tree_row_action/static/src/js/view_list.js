openerp.suvit_web_tree_row_action = function(instance, local) {

  var QWeb = instance.web.qweb;


  var do_action = function(view, id, context){
    var model_obj = new instance.web.Model(view.dataset.model);
    model_obj.call('get_formview_action', [id]).then(function(action){
      action['target'] = context.open_formview;
      view.do_action(action);
    });
  };

  instance.web.ListView.include({

    do_activate_record: function (index, id, dataset, view) {
        var context = this.ViewManager.action.context;
        if (!context.open_formview)
          return this._super(index, id, dataset, view);

        do_action(this, id, context);
    }

  });

  instance.web.form.Many2ManyListView.include({

    do_activate_record: function (index, id) {
        var context = this.ViewManager.field.context;
        if (!context.open_formview)
          return this._super(index, id);

        do_action(this, id, context);
    }

  });

  instance.web.form.One2ManyListView.include({

    do_activate_record: function(index, id) {
        var context = this.ViewManager.o2m.field.context;
        if (!context.open_formview)
          return this._super(index, id);

        do_action(this, id, context);
    }

  });

};