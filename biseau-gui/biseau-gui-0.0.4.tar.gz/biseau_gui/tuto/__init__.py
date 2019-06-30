
from . import asp_basics, biseau_basics
from .tuto import TutorialViewer

TutorialViewer.tutorials = {
    asp_basics.TUTORIAL_NAME: asp_basics.ORDERED_TUTO,
    biseau_basics.TUTORIAL_NAME: biseau_basics.ORDERED_TUTO,

}
