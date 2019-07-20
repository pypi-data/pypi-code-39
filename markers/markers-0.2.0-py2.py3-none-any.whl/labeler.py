import ipywidgets as widgets # type: ignore
from traitlets import Unicode, Dict, List # type: ignore

from .label import Label

def noop(*args): pass

class MissingCycle(Exception): pass

@widgets.register
class Labeler(widgets.DOMWidget):
    """A data labeling widget to be used with Markers.ai."""
    _view_name = Unicode('AnnotationView').tag(sync=True)
    _model_name = Unicode('AnnotationModel').tag(sync=True)
    _view_module = Unicode('markers').tag(sync=True)
    _model_module = Unicode('markers').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    project = Dict({}).tag(sync=True)
    document = Dict({}).tag(sync=True)
    task = Dict({}).tag(sync=True)
    fragment_classes = List([]).tag(sync=True)
    document_classes = List([]).tag(sync=True)
    metadata = Dict({}).tag(sync=True)

    # NOTE: variables prefixed with _ indicate class vars that are not serialized for the widget

    def __init__(self, project, cycle, **kwargs):
        if not cycle:
            raise MissingCycle('Labeler cannot be created without a cycle.')

        self.cycle = cycle
        super(Labeler, self).__init__(**kwargs)

        self._project = project
        self.project = project.serialize_for_labeler()
        self.document_classes = project.document_classes
        self.fragment_classes = project.fragment_classes
        self._current_task = None

        self.on_msg(self._handle_message)

        self._load_next_task()

    def _handle_message(self, _, content, buffers):
        handlers = {
            'close_widget': self._handle_close,
            'save_label': self._handle_save_label,
            'skip_document': self._handle_skip_task
        }
        handler = handlers.get(content['event'], noop)
        handler(content.get('data', None))

    def _handle_close(self, *args):
        self.close()

    def _handle_save_label(self, data):
        if data['documentClassId']:
            found = list(filter(lambda doc_class: doc_class['id'] == data['documentClassId'], self.document_classes))
            document_class = found[0]
        else:
            document_class = {}

        # NOTE: data['annotations'] and document_class can be null
        new_label = Label.create_from_labeler(self._project, self.document, document_class, data['annotations'])
        self.cycle.add_label(self._current_task, new_label)

        self._load_next_task()

    def _handle_skip_task(self, *args):
        self.cycle.skip_task(self._current_task)
        self._load_next_task()

    def _load_next_task(self):
        try:
            self._current_task = self.cycle.next_task()

            self.document = self._current_task.document.serialize()
            self.task = self._current_task.serialize()

            cycle_metadata = self.cycle.metadata
            self.metadata = {
                'task_progress': cycle_metadata['task_counts']['total'] - cycle_metadata['task_counts']['incomplete'],
                'task_count': cycle_metadata['task_counts']['total']
            }
        except IndexError as e:
            self.metadata = {
                'status': 'complete'
            }
