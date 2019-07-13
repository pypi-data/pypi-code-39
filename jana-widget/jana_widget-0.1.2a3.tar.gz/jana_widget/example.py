import ipywidgets as widgets
from traitlets import Unicode

@widgets.register
class HelloWorld(widgets.DOMWidget):
    """An example widget."""
    _view_name = Unicode('HelloView').tag(sync=True)
    _model_name = Unicode('HelloModel').tag(sync=True)
    _view_module = Unicode('jana-widget').tag(sync=True)
    _model_module = Unicode('jana-widget').tag(sync=True)
    _view_module_version = Unicode('^0.1.2').tag(sync=True)
    _model_module_version = Unicode('^0.1.2').tag(sync=True)
    value = Unicode('Hello World!').tag(sync=True)

    def create(self):
        from IPython.core.display import Javascript
        return Javascript(
           """
           var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var HelloModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name : 'HelloModel',
        _view_name : 'HelloView',
        _model_module : 'jana-widget',
        _view_module : 'jana-widget',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        value : 'Hello World'
    })
});


// Custom View. Renders the widget model.
var HelloView = widgets.DOMWidgetView.extend({
    render: function() {
        this.value_changed();
        this.model.on('change:value', this.value_changed, this);
    },

    value_changed: function() {
        this.el.textContent = this.model.get('value');
    }
});


module.exports = {
    HelloModel : HelloModel,
    HelloView : HelloView
};""")


"""
require.undef('mapboxglModule');
define('mapboxglModule', ["@jupyter-widgets/base"], widgets => {
let MapboxGLView = widgets.DOMWidgetView.extend({
        defaults: _.extend({}, widgets.DOMWidgetModel.prototype.defaults, { value: '' }),
        render: function() {
            this.value_changed();
            this.model.on('change:value', this.value_changed, this);
        },
value_changed: function() {
            this.el.textContent = this.model.get('value').my_key;
        },
    });
return {
        MapboxGLView,
    };
});
"""
