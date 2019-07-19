from north_c9.controller import C9Controller
from north_c9.sequences import SequenceBuilder

controller = C9Controller()
controller.home(if_needed=True)
builder = SequenceBuilder(controller)