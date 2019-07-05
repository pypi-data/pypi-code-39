

# pylint: disable=C,W,R,F



##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from Cheetah.compat import unicode
from javatools.cheetah.change_Change import change_Change
from javatools.cheetah import xml_entity_escape as escape

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '3.1.0'
__CHEETAH_versionTuple__ = (3, 1, 0, 'final', 1)
__CHEETAH_src__ = 'javatools/cheetah/classdiff_MethodRemoved.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jun 21 15:26:13 2019'
__CHEETAH_docstring__ = '" "'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class classdiff_MethodRemoved(change_Change):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(classdiff_MethodRemoved, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def description(self, **KWS):



        ## CHEETAH: generated from #block description at line 6, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''
<!-- START BLOCK: description -->
''')
        change = getattr(self, "change")
        info = change.get_ldata()
        a = info.get_name()
        b = ", ".join(info.pretty_arg_types())
        c = info.pretty_type()
        write('''
<h3>''')
        write(_filter( escape("%s(%s):%s" % (a, b, c))))
        write('''</h3>
<div class="description">Method Removed</div>
''')
        write('''
<!-- END BLOCK: description -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def details(self, **KWS):



        ## CHEETAH: generated from #block details at line 20, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''
<!-- START BLOCK: details -->
<div class="details">
<div class="lrdata">
''')
        _v = VFFSL(SL,"method_table",False)(VFN(VFFSL(SL,"change",True),"get_ldata",False)()) # '$method_table($change.get_ldata())' on line 23, col 1
        if _v is not None: write(_filter(_v, rawExpr='$method_table($change.get_ldata())'))
        write('''
</div>
</div>
''')
        write('''
<!-- END BLOCK: details -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def method_table(self, info, **KWS):



        ## CHEETAH: generated from #def method_table(info) at line 30, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''<table class="left-headers">
''')
        _v = VFFSL(SL,"row",False)("Method Name", info.get_name()) # '$row("Method Name", info.get_name())' on line 32, col 1
        if _v is not None: write(_filter(_v, rawExpr='$row("Method Name", info.get_name())'))
        write('''
''')
        _v = VFFSL(SL,"row",False)("Return Type", info.pretty_type()) # '$row("Return Type", info.pretty_type())' on line 33, col 1
        if _v is not None: write(_filter(_v, rawExpr='$row("Return Type", info.pretty_type())'))
        write('''
''')
        _v = VFFSL(SL,"row",False)("Argument Types", "(%s)" % ", ".join(info.pretty_arg_types())) # '$row("Argument Types", "(%s)" % ", ".join(info.pretty_arg_types()))' on line 34, col 1
        if _v is not None: write(_filter(_v, rawExpr='$row("Argument Types", "(%s)" % ", ".join(info.pretty_arg_types()))'))
        write('''
''')
        _v = VFFSL(SL,"row",False)("Method Flags", "0x%04x: %s" %
      (info.access_flags, " ".join(info.pretty_access_flags())))
        if _v is not None: write(_filter(_v, rawExpr='$row("Method Flags", "0x%04x: %s" %\n      (info.access_flags, " ".join(info.pretty_access_flags())))'))
        write('''

''')
        if info.get_signature(): # generated from line 38, col 1
            _v = VFFSL(SL,"row",False)("Generics Signature", info.get_signature()) # '$row("Generics Signature", info.get_signature())' on line 39, col 1
            if _v is not None: write(_filter(_v, rawExpr='$row("Generics Signature", info.get_signature())'))
            write('''
''')
        write('''
''')
        if info.get_exceptions(): # generated from line 42, col 1
            _v = VFFSL(SL,"row",False)("Exceptions", ", ".join(info.pretty_exceptions())) # '$row("Exceptions", ", ".join(info.pretty_exceptions()))' on line 43, col 1
            if _v is not None: write(_filter(_v, rawExpr='$row("Exceptions", ", ".join(info.pretty_exceptions()))'))
            write('''
''')
        write('''
''')
        if not info.get_code(): # generated from line 46, col 1
            _v = VFFSL(SL,"row",False)("Abstract", "True") # '$row("Abstract", "True")' on line 47, col 1
            if _v is not None: write(_filter(_v, rawExpr='$row("Abstract", "True")'))
            write('''
''')
        write('''
''')
        if info.is_deprecated(): # generated from line 50, col 1
            _v = VFFSL(SL,"row",False)("Deprecated", "True") # '$row("Deprecated", "True")' on line 51, col 1
            if _v is not None: write(_filter(_v, rawExpr='$row("Deprecated", "True")'))
            write('''
''')
        write('''
</table>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def row(self, label, data, **KWS):



        ## CHEETAH: generated from #def row(label, data) at line 59, col 1.
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''<tr>
<th>''')
        _v = VFFSL(SL,"label",True) # '$label' on line 61, col 5
        if _v is not None: write(_filter(_v, rawExpr='$label'))
        write('''</th>
<td>''')
        write(_filter( escape(data)))
        write('''</td>
</tr>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        

    def writeBody(self, **KWS):



        ## CHEETAH: main method generated for this template
        trans = KWS.get("trans")
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''


''')
        self.description(trans=trans)
        write('''


''')
        self.details(trans=trans)
        write('''








''')
        # 
        #  The end.
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_classdiff_MethodRemoved = 'writeBody'

## END CLASS DEFINITION

if not hasattr(classdiff_MethodRemoved, '_initCheetahAttributes'):
    templateAPIClass = getattr(classdiff_MethodRemoved,
                               '_CHEETAH_templateClass',
                               Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(classdiff_MethodRemoved)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://cheetahtemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=classdiff_MethodRemoved()).run()


