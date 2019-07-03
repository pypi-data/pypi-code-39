# number of significant digits for floats
FLOAT_PRECISION = 4

import re
import sys
import types
from collections import defaultdict

import math

typeRE = re.compile("<type '(.*)'>")
classRE = re.compile("<class '(.*)'>")

import inspect

# TODO: maybe use the 'six' library to smooth over Py2 and Py3 incompatibilities?
is_python3 = (sys.version_info[0] == 3)
if is_python3:
    # avoid name errors (GROSS!)
    long = int
    unicode = str


def is_class(dat):
    """Return whether dat is a class."""
    if is_python3:
        return isinstance(dat, type)
    else:
        return type(dat) in (types.ClassType, types.TypeType)


def is_instance(dat):
    """Return whether dat is an instance of a class."""
    if is_python3:
        return type(dat) not in PRIMITIVE_TYPES and \
               isinstance(type(dat), type) and \
               not isinstance(dat, type)
    else:
        # ugh, classRE match is a bit of a hack :(
        return type(dat) == types.InstanceType or classRE.match(str(type(dat)))


def get_name(obj):
    """Return the name of an object."""
    return obj.__name__ if hasattr(obj, '__name__') else get_name(type(obj))


PRIMITIVE_TYPES = (int, long, float, str, unicode, bool, type(None))


def encode_primitive(dat):
    t = type(dat)
    if t is float:
        if math.isinf(dat):
            if dat > 0:
                return ['SPECIAL_FLOAT', 'Infinity']
            else:
                return ['SPECIAL_FLOAT', '-Infinity']
        elif math.isnan(dat):
            return ['SPECIAL_FLOAT', 'NaN']
        else:
            # render floats like 3.0 as '3.0' and not as 3
            if dat == int(dat):
                return ['SPECIAL_FLOAT', '%.1f' % dat]
            else:
                return round(dat, FLOAT_PRECISION)
    elif t is str and (not is_python3):
        # hack only for Python 2 strings ... always turn into unicode
        # and display '?' when it's not valid unicode
        return dat.decode('utf-8', 'replace')
    else:
        # return all other primitives verbatim
        return dat


# grab a line number like ' <line 2>' or ' <line 2b>'
def create_lambda_line_number(codeobj, line_to_lambda_code):
    try:
        lambda_lineno = codeobj.co_firstlineno
        lst = line_to_lambda_code[lambda_lineno]
        ind = lst.index(codeobj)
        # add a suffix for all subsequent lambdas on a line beyond the first
        # (nix this for now because order isn't guaranteed when you have
        #  multiple lambdas on the same line)
        '''
        if ind > 0:
          lineno_str = str(lambda_lineno) + chr(ord('a') + ind)
        else:
          lineno_str = str(lambda_lineno)
        '''
        lineno_str = str(lambda_lineno)
        return ' <line ' + lineno_str + '>'
    except:
        return ''


# Note that this might BLOAT MEMORY CONSUMPTION since we're holding on
# to every reference ever created by the program without ever releasing
# anything!
class ObjectEncoder:
    def __init__(self, parent):
        self.parent = parent  # should be a PGLogger object

        # Key: canonicalized small ID
        # Value: encoded (compound) heap object
        self.encoded_heap_objects = {}

        self.render_heap_primitives = parent.render_heap_primitives

        self.id_to_small_IDs = {}
        self.cur_small_ID = 1

        # wow, creating unique identifiers for lambdas is quite annoying,
        # especially if we want to properly differentiate:
        # 1.) multiple lambdas defined on the same line, and
        # 2.) the same lambda code defined multiple times on different lines
        #
        # However, it gets confused when there are multiple identical
        # lambdas on the same line, like:
        # f(lambda x:x*x, lambda y:y*y, lambda x:x*x)

        # (assumes everything is in one file)
        # Key:   line number
        # Value: list of the code objects of lambdas defined
        #        on that line in the order they were defined
        self.line_to_lambda_code = defaultdict(list)

    def should_hide_var(self, var):
        return self.parent.should_hide_var(var)

    # searches through self.parents.types_to_inline and tries
    # to match the type returned by type(obj).__name__ and
    # also 'class' and 'instance' for classes and instances, respectively
    def should_inline_object_by_type(self, obj):
        # fast-pass optimization -- common case
        if not self.parent.types_to_inline:
            return False

        # copy-pasted from the end of self.encode()
        typ = type(obj)
        typename = typ.__name__

        # pick up built-in functions too:
        if typ in (types.FunctionType, types.MethodType, types.BuiltinFunctionType, types.BuiltinMethodType):
            typename = 'function'

        if not typename:
            return False

        alt_typename = None
        if is_class(obj):
            alt_typename = 'class'
        elif is_instance(obj) and typename != 'function':
            # if obj is an instance of the Fooo class, then we want to match
            # on both 'instance' and 'Fooo'
            # (exception: 'function' objects are sometimes also instances,
            #  but we still want to call them 'function', so ignore them)
            typename = 'instance'
            class_name = None
            if hasattr(obj, '__class__'):
                # common case ...
                class_name = get_name(obj.__class__)
            else:
                # super special case for something like
                # "from datetime import datetime_CAPI" in Python 3.2,
                # which is some weird 'PyCapsule' type ...
                # http://docs.python.org/release/3.1.5/c-api/capsule.html
                class_name = get_name(type(obj))
            alt_typename = class_name

        for re_match in self.parent.types_to_inline:
            if re_match(typename):
                return True
            if alt_typename and re_match(alt_typename):
                return True
        return False

    def get_heap(self):
        return self.encoded_heap_objects

    def reset_heap(self):
        # VERY IMPORTANT to reassign to an empty dict rather than just
        # clearing the existing dict, since get_heap() could have been
        # called earlier to return a reference to a previous heap state
        self.encoded_heap_objects = {}

    def set_function_parent_frame_ID(self, ref_obj, enclosing_frame_id):
        assert ref_obj[0] == 'REF'
        func_obj = self.encoded_heap_objects[ref_obj[1]]
        assert func_obj[0] == 'FUNCTION'
        func_obj[-1] = enclosing_frame_id

    # return either a primitive object or an object reference;
    # and as a side effect, update encoded_heap_objects
    def encode(self, dat, get_parent):
        """Encode a data value DAT using the GET_PARENT function for parent ids."""
        # primitive type
        if not self.render_heap_primitives and type(dat) in PRIMITIVE_TYPES:
            return encode_primitive(dat)
        # compound type - return an object reference and update encoded_heap_objects
        else:
            # IMPORTED_FAUX_PRIMITIVE feature added on 2018-06-13:
            is_externally_defined = False  # is dat defined in external (i.e., non-user) code?
            try:
                # some objects don't return anything for getsourcefile() but DO return
                # something legit for getmodule(). e.g., "from io import StringIO"
                # so TRY getmodule *first* and then fall back on getsourcefile
                # since getmodule seems more robust empirically ...
                gsf = inspect.getmodule(dat).__file__
                if not gsf:
                    gsf = inspect.getsourcefile(dat)

                # a hacky heuristic is that if gsf is an absolute path, then it's likely
                # to be some library function and *not* in user-defined code
                #
                # NB: don't use os.path.isabs() since it doesn't work on some
                # python installations (e.g., on my webserver) and also adds a
                # dependency on the os module. just do a simple check:
                #
                # hacky: do other checks for strings that are indicative of files
                # that load user-written code, like 'generate_json_trace.py'
                if gsf and gsf[0] == '/' and 'generate_json_trace.py' not in gsf:
                    is_externally_defined = True
            except (AttributeError, TypeError):
                pass  # fail soft
            my_id = id(dat)

            # if dat is an *real* object instance (and not some special built-in one
            # like ABCMeta, or a py3 function object), then DON'T treat it as
            # externally-defined because a user might be instantiating an *instance*
            # of an imported class in their own code, so we want to show that instance
            # in da visualization - ugh #hacky
            if (is_instance(dat) and
                    type(dat) not in (
                            types.FunctionType, types.MethodType, types.BuiltinFunctionType,
                            types.BuiltinMethodType) and
                    hasattr(dat, '__class__') and (get_name(dat.__class__) != 'ABCMeta')):
                is_externally_defined = False

            # if this is an externally-defined object (i.e., from an imported
            # module, don't try to recurse into it since we don't want to see
            # the internals of imported objects; just return an
            # IMPORTED_FAUX_PRIMITIVE object and continue along on our way
            if is_externally_defined:
                label = 'object'
                try:
                    label = type(dat).__name__
                    if is_class(dat):
                        label = 'class'
                    elif is_instance(dat):
                        label = 'object'
                except:
                    pass
                return ['IMPORTED_FAUX_PRIMITIVE', 'imported ' + label]  # punt early!

            # next check whether it should be inlined
            if self.should_inline_object_by_type(dat):
                label = 'object'
                try:
                    label = type(dat).__name__
                    if is_class(dat):
                        class_name = get_name(dat)
                        label = class_name + ' class'
                    elif is_instance(dat):
                        # a lot of copy-pasta from other parts of this file:
                        # TODO: clean up
                        class_name = None
                        if hasattr(dat, '__class__'):
                            # common case ...
                            class_name = get_name(dat.__class__)
                        else:
                            # super special case for something like
                            # "from datetime import datetime_CAPI" in Python 3.2,
                            # which is some weird 'PyCapsule' type ...
                            # http://docs.python.org/release/3.1.5/c-api/capsule.html
                            class_name = get_name(type(dat))
                        if class_name:
                            label = class_name + ' instance'
                        else:
                            label = 'instance'
                except:
                    pass
                return ['IMPORTED_FAUX_PRIMITIVE', label + ' (hidden)']  # punt early!

            try:
                my_small_id = self.id_to_small_IDs[my_id]
            except KeyError:
                my_small_id = self.cur_small_ID
                self.id_to_small_IDs[my_id] = self.cur_small_ID
                self.cur_small_ID += 1

            del my_id  # to prevent bugs later in this function

            ret = ['REF', my_small_id]

            # punt early if you've already encoded this object
            if my_small_id in self.encoded_heap_objects:
                return ret

            # major side-effect!
            new_obj = []
            self.encoded_heap_objects[my_small_id] = new_obj

            typ = type(dat)

            if typ == list:
                new_obj.append('LIST')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))
            elif typ == tuple:
                new_obj.append('TUPLE')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))
            elif typ == set:
                new_obj.append('SET')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))
            elif typ == dict:
                new_obj.append('DICT')
                for (k, v) in dat.items():
                    # don't display some built-in locals ...
                    if k not in ('__module__', '__return__', '__locals__'):
                        new_obj.append([self.encode(k, get_parent), self.encode(v, get_parent)])
            elif typ in (types.FunctionType, types.MethodType):
                if is_python3:
                    argspec = inspect.getfullargspec(dat)
                else:
                    argspec = inspect.getargspec(dat)

                printed_args = [e for e in argspec.args]

                default_arg_names_and_vals = []
                if argspec.defaults:
                    num_missing_defaults = len(printed_args) - len(argspec.defaults)
                    assert num_missing_defaults >= 0
                    # tricky tricky tricky how default positional arguments work!
                    for i in range(num_missing_defaults, len(printed_args)):
                        default_arg_names_and_vals.append(
                            (printed_args[i], self.encode(argspec.defaults[i - num_missing_defaults], get_parent)))

                if argspec.varargs:
                    printed_args.append('*' + argspec.varargs)

                if is_python3:
                    # kwonlyargs come before varkw
                    if argspec.kwonlyargs:
                        printed_args.extend(argspec.kwonlyargs)
                        if argspec.kwonlydefaults:
                            # iterate in order of appearance in kwonlyargs
                            for varname in argspec.kwonlyargs:
                                if varname in argspec.kwonlydefaults:
                                    val = argspec.kwonlydefaults[varname]
                                    default_arg_names_and_vals.append((varname, self.encode(val, get_parent)))
                    if argspec.varkw:
                        printed_args.append('**' + argspec.varkw)
                else:
                    if argspec.keywords:
                        printed_args.append('**' + argspec.keywords)

                func_name = get_name(dat)

                pretty_name = func_name

                # sometimes might fail for, say, <genexpr>, so just ignore
                # failures for now ...
                try:
                    pretty_name += '(' + ', '.join(printed_args) + ')'
                except TypeError:
                    pass

                # put a line number suffix on lambdas to more uniquely identify
                # them, since they don't have names
                if func_name == '<lambda>':
                    cod = (dat.__code__ if is_python3 else dat.func_code)  # ugh!
                    lst = self.line_to_lambda_code[cod.co_firstlineno]
                    if cod not in lst:
                        lst.append(cod)
                    pretty_name += create_lambda_line_number(cod,
                                                             self.line_to_lambda_code)

                encoded_val = ['FUNCTION', pretty_name, None]
                if get_parent:
                    enclosing_frame_id = get_parent(dat)
                    encoded_val[2] = enclosing_frame_id
                new_obj.extend(encoded_val)
                # OPTIONAL!!!
                if default_arg_names_and_vals:
                    new_obj.append(default_arg_names_and_vals)  # *append* it as a single list element

            elif typ is types.BuiltinFunctionType:
                pretty_name = get_name(dat) + '(...)'
                new_obj.extend(['FUNCTION', pretty_name, None])
            elif is_class(dat) or is_instance(dat):
                self.encode_class_or_instance(dat, new_obj)
            elif typ is types.ModuleType:
                new_obj.extend(['module', dat.__name__])
            elif typ in PRIMITIVE_TYPES:
                assert self.render_heap_primitives
                new_obj.extend(['HEAP_PRIMITIVE', type(dat).__name__, encode_primitive(dat)])
            else:
                typeStr = str(typ)
                m = typeRE.match(typeStr)

                if not m:
                    m = classRE.match(typeStr)

                assert m, typ

                if is_python3:
                    encoded_dat = str(dat)
                else:
                    # ugh, for bytearray() in Python 2, str() returns
                    # non-JSON-serializable characters, so need to decode:
                    encoded_dat = str(dat).decode('utf-8', 'replace')
                new_obj.extend([m.group(1), encoded_dat])

            return ret

    def encode_class_or_instance(self, dat, new_obj):
        """Encode dat as a class or instance."""
        if is_instance(dat):
            if hasattr(dat, '__class__'):
                # common case ...
                class_name = get_name(dat.__class__)
            else:
                # super special case for something like
                # "from datetime import datetime_CAPI" in Python 3.2,
                # which is some weird 'PyCapsule' type ...
                # http://docs.python.org/release/3.1.5/c-api/capsule.html
                class_name = get_name(type(dat))

            pprint_str = None
            # do you or any of your superclasses have a __str__ field? if so, pretty-print yourself!
            if hasattr(dat, '__str__'):
                try:
                    pprint_str = dat.__str__()

                    # sometimes you'll get 'trivial' pprint_str like: '<__main__.MyObj object at 0x10f465cd0>'
                    # or '<module 'collections' ...'
                    # IGNORE THOSE!!!
                    if pprint_str[0] == '<' and pprint_str[-1] == '>' and (
                            ' at ' in pprint_str or pprint_str.startswith('<module')):
                        pprint_str = None
                except:
                    pass

            # TODO: filter for trivial-looking pprint_str like those produced
            # by object.__str__
            if pprint_str:
                new_obj.extend(['INSTANCE_PPRINT', class_name, pprint_str])
            else:
                new_obj.extend(['INSTANCE', class_name])

            # don't traverse inside modules, or else risk EXPLODING the visualization
            if class_name == 'module':
                return
        else:
            superclass_names = [e.__name__ for e in dat.__bases__ if e is not object]
            new_obj.extend(['CLASS', get_name(dat), superclass_names])

        # traverse inside of its __dict__ to grab attributes
        # (filter out useless-seeming ones, based on anecdotal observation):
        hidden = ('__doc__', '__module__', '__return__', '__dict__',
                  '__locals__', '__weakref__', '__qualname__')
        if hasattr(dat, '__dict__'):
            user_attrs = sorted([e for e in dat.__dict__ if e not in hidden])
        else:
            user_attrs = []

        for attr in user_attrs:
            if not self.should_hide_var(attr):
                new_obj.append([self.encode(attr, None), self.encode(dat.__dict__[attr], None)])
