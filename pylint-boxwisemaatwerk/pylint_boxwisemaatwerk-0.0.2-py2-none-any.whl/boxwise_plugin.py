import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
import checkers
from checkers.add_reference_checker import AddReferenceChecker


def register(linter):
    print "adding checker for trancon"
    linter.register_checker(AddReferenceChecker(linter))
