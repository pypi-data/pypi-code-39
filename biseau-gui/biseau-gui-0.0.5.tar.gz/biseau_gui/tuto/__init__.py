
from . import asp_basics, biseau_basics, fca_basics, python_scripting_basics
from .tuto import TutorialViewer

TutorialViewer.tutorials = {
    asp_basics.TUTORIAL_NAME: ('asp', asp_basics.ORDERED_TUTO),
    biseau_basics.TUTORIAL_NAME: ('asp', biseau_basics.ORDERED_TUTO),
    fca_basics.TUTORIAL_NAME: ('asp', fca_basics.ORDERED_TUTO),
    python_scripting_basics.TUTORIAL_NAME:
        ('python', python_scripting_basics.ORDERED_TUTO),
}
