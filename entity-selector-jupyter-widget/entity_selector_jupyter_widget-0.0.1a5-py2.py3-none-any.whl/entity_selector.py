from __future__ import print_function
import time

import ipywidgets as widgets
from traitlets import Unicode, observe, HasTraits


def on_change(change):
    print("changed to %s" % change['new'])
    return change['new']


@widgets.register
class EntitySelector(widgets.DOMWidget, HasTraits):
    _view_name = Unicode('EntitySelectorView').tag(sync=True)
    _model_name = Unicode('EntitySelectorModel').tag(sync=True)
    _view_module = Unicode('frontend_entity_selector_jupyter_widget').tag(sync=True)
    _model_module = Unicode('frontend_entity_selector_jupyter_widget').tag(sync=True)
    _view_module_version = Unicode('^0.0.1').tag(sync=True)
    _model_module_version = Unicode('^0.0.1').tag(sync=True)
    # value = Unicode('fff').tag(sync=True)
    text = Unicode('').tag(sync=True)
    search = Unicode('').tag(sync=True)
    res = Unicode('').tag(sync=True)
    input_str1 = Unicode('')
    input_str2 = Unicode('')

    def __init__(self, input_str1, input_str2):
        self.text = input_str1
        self.search = input_str2
        super(EntitySelector, self).__init__()
        # self.get_results()

    # @observe('res')
    # def _update_data(self, change):
    #     print(change)
    # @observe('res')
    # def _res_changed(self, change):
    #     print("{name} changed from {old} to {new}".format(**change))
    #
    def result(self):
        while True:
            if res != '':
                return res
            time.sleep(1)
        # self.observe(on_change)

