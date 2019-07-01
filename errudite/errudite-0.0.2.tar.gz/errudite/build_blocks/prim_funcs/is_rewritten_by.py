import math
import traceback
from typing import Union,List
from spacy.tokens import Doc, Span, Token
from ...utils.check import DSLValueError
import logging
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
from ..prim_func import PrimFunc

@PrimFunc.register()
def is_rewritten_by(instance: 'Instance', rewrite: str="SELECTED") -> bool:
    """
    Test if an instance is generated by the named rewrite rule.
    
    Parameters
    ----------
    instance : Instance
        The instance to be tested.
        *Automatically filled in when using the DSL parser.*
    rewrite : str, optional
        Use a named rule rewrite to get instances rewritten by the rule.
        If using "SELECTED", it will be automatically resolved to 
        ``Instance.model`` , by default "SELECTED"
    
    Returns
    -------
    bool
        If an instance is generated by the named rewrite rule.
    """
    output = False
    try:
        output = instance != None
    except DSLValueError as e:
        #logger.error(e)
        raise(e)
    except Exception as e:
        #print(f'[is_digit]')
        #traceback.print_exc()
        ex = Exception(f"Unknown exception from [ is_rewritten_by ]: {e}")
        #logger.error(ex)
        raise(ex)
    #finally:
    else:
        #pass
        return output