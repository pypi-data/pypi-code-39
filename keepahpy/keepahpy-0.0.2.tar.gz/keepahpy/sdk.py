from flask import current_app, request, Response
import requests
from functools import wraps
import json
import inspect
import re
import logging
from pprint import pprint

### Module Args / Config :
KEEPAH_BACKEND_IP=None
KEEPAH_CLIENT_SECRET=None
contentURL=None
App_name=None
logging_level=None

Login_page = ''

logging.basicConfig(format='Keepah-SDK: %(levelname)s : %(message)s', level=logging.INFO)
INFO = logging.info
WARNING = logging.warning
ERROR = logging.error

def KeepahRequest(method, pfad, data={}):
    r = method(
        KEEPAH_BACKEND_IP + pfad,
        headers={'Content-Type': 'application/json; charset=utf-8', 'Authorization':  KEEPAH_CLIENT_SECRET},
        data=json.dumps(data))
    return r

def is_allowed(user, action, resource):
    path = 'memberships/validate_email/{0}/{1}/{2}'.format(user, resource, action)
    r = KeepahRequest(requests.get, path)
    return r

def publish(resource_name, resource_type):
    data = {"description": resource_name, "resourceTypeName": resource_type}
    resp = KeepahRequest(requests.put, 'resources/' + resource_name, data)
    return resp

def delete(resource_name):
    resp = KeepahRequest(requests.delete, 'resources/' + resource_name)
    return resp

def authorize(user, resource_name, action):
    data = {"resourceName": resource_name, "actionName": action, "userEmail": user}
    resp = KeepahRequest(requests.put, 'memberships', data)
    return resp

def unauthorize(user, resource_name, action):
    data = {"resourceName": resource_name, "actionName": action, "userEmail": user}
    resp = KeepahRequest(requests.delete, 'memberships', data)
    return resp
    
def get_actions():
    resp = KeepahRequest(requests.get, 'actions?')
    return resp.json()

def get_types():
    resp = KeepahRequest(requests.get, 'resource_types?')
    return resp.json()

def get_actions_for_type(resource_type):
    resp = KeepahRequest(requests.get, 'actions?resource_type=' + resource_type)
    return resp

def get_users_memberships(user_email):
    resp = KeepahRequest(requests.get, 'memberships?user_email=' + user_email)
    return resp

def get_Keepahs_resources(resource_type=None):
    if resource_type is None:
        return KeepahRequest(requests.get, "resources?").json()
    else:
        return KeepahRequest(requests.get, "resources?resource_type="+resource_type).json()

def get_users_email_from_token(tk):
    resp = KeepahRequest(requests.get, 'users?user_token='+tk)
    if resp.content != b'':
        return resp.json()[0]["email"]

def get_user():
    user_tok = None
    try:
        user_tok = request.headers['Authorization'].split()[1]
    except Exception:
        user_tok = _scan_request_for(['token', 'user', 'user_token', 'userToken'])
    if user_tok is None:
        return 'No user found in request', 401

    resp = KeepahRequest(requests.get, 'users?user_token='+user_tok)
    if resp.content == b'':
        return 'User not found'
    else:
        user_email = resp.json()[0]["email"]
        return user_email


pat = re.compile(r'(?P<type>\<\w+[\*]*\>|\{\w+[\*]*\})|(?P<parent>parent(\<\w+[\*]*\>|\{\w+[\*]*\}))|(?P<child>child(\<\w+[\*]*\>|\{\w+[\*]*\}))')
ident = re.compile(r'[\{\}\<\>]|parent[\{\<]|child[\<\{]')


class Action(object):

    commands = {'read': ('get', 'show', 'view', 'read', 'display', 'open', 'see', 'open', 'display'),
                'write': ('post', 'add', 'create', 'publish', 'write', 'upload'),
                'update': ('put', 'update', 'modify', 'change', 'edit'),
                'delete': ('delete', 'remove'),
                'authorize': ('authorize'),
                'unauthorize': ('unauthorize')
    }

    def __init__(self, val):
        
        self.original_value = val
        self.command = self.type = self.parent = self.child = None
        self.name = self.description = self.displayName = None

        command = val.split()[0]
        types = {t: None for t in ('type', 'parent', 'child')} 
        for m in pat.finditer(val):
            for k, v in m.groupdict().items():
                if v is not None:
                    types[k] = re.sub(ident, '', v)
        name = display = description = re.sub(ident, '', val)
        params = {"description": None, "displayName": display, \
                  "actionArgs": types, "name": name, "command": command}
        for kw, v in params.items():
            if kw is "actionArgs":
                for k, vl in v.items():
                    self.__setattr__(k, vl)
            else:
                self.__setattr__(kw, v)

        self.cmd = self.get_command_type()
        self.keywords = self.get_parent_child_pair()

    def format_for_publishing(self):
        d = {}
        for kw in ("description", "displayName", "name"):
            d[kw] = self.__getattribute__(kw)
        d['resourceTypeName'] = self.keywords[0]
        return d

    def get_command_type(self):
        cmd_type = None
        for k, v in Action.commands.items():
            if self.command in v:
                cmd_type = k
                break
        if cmd_type is None:
            WARNING("I couldn't understand the command '%s' ; using default value = 'read'", self.command)
            cmd_type = 'read'
        return cmd_type

    def get_parent_child_pair(self):
        t, p, c = self.type, self.parent, self.child
        prt = chl = None
        sm = sum([int(bool(x)) for x in (t, p, c)])
        if sm == 0:
            WARNING('No type supplied to action "%s" ; resourceType = "app" is infered', self.original_value)
            prt = chl = 'app'
        elif sm == 1:
            if self.cmd in ('write', 'delete', 'update'):
                if t or c:
                    T = t if t else c
                    prt = 'app'
                    chl = T
                    WARNING('single type supplied to action "%s" ; parent-type = "*app*" and child-type = "%s" is infered', self.original_value, chl)
                elif p:
                    WARNING('Single type supplied to action "%s" ; parent-type = "%s" and child-type = None is infered.\n' + \
                            'The command for this action has been set to "read" and no Resource will be published to Keepah.', \
                            self.original_value, p)
                    prt = p
                    chl = None
                    self.cmd = 'read'
            else:
                prt = [x for x in (p, t, c) if bool(x)][0]
        elif sm == 2:
            if self.cmd in ('write', 'delete', 'update'):
                prt, chl = [x for x in (p, t, c) if bool(x)]
            else:
                ERROR('Too much types in action "%s" ; commands with value = %s (= "%s") only need one resourceType.', \
                    self.original_value, self.command , self.cmd)
        elif sm > 2:
            ERROR('Too much types in action "%s" ; commands with value = %s (= "%s") need at most two resourceTypes.', \
                    self.original_value, self.command , self.cmd)                
            prt = chl = None
        return prt, chl

def make_likely_kw(st):
    kws = [st, 'name', 'id']
    for tail in ('_name', 'Name', '_id', 'Id'):
        kws += [st + tail]
    return kws
    
def _scan_request_for(kws):
    instance = None
    req = request
    for place in [req.args, req.view_args, req.json]:
        if place:
            for kw in kws:
                try:
                    instance = place[kw]
                    INFO("Found keyword %s = %s in request", kw, instance)
                    break
                except KeyError:
                    continue
            if instance:
                break
    if instance is None:
        ERROR("I couldn't find a value for the keyword %s in the request to url %s", kws, req.full_path)
        return None
    else:
        return instance

def get_value_from_request(arg):
    if arg == 'app':
        return App_name
    return _scan_request_for(make_likely_kw(arg))

def get_value_from_return_value(kw, rv, endpoint):
    val = None
    if type(rv) is Response and not rv.is_json:
        ERROR("I need the return value for the endpoint %s to be a json in order to add created resources to Keepah.", endpoint)
        return None
    elif type(rv) is Response and rv.is_json:
        rv = rv.get_json()
        for k in make_likely_kw(kw):
            try:
                val = rv[k]
                INFO("Found keyword %s = %s in return value", k, val)
                break
            except KeyError:
                continue
    elif type(rv) is str:
        try:
            rv = json.loads(rv)
        except json.JSONDecodeError:
            ERROR("I need the return value for the endpoint %s to be a json in order to add created resources to Keepah.", endpoint)
            return None
        for k in make_likely_kw(kw):
            try:
                val = rv[k]
                INFO("Found keyword %s = %s in return value", k, val)
                break
            except KeyError:
                continue
    if val is None:
        ERROR("I couldn't find a value for the keyword %s in the return value of the endpoint %s", kw, endpoint)
        return None
    else:
        return val


class Keepah(object):
    def __init__(self, action=None, converter=None):
        self.action = action
        self.pre_converter = self.post_converter = self.converter = None
        if callable(converter):
            self.converter = converter
        elif type(converter) is tuple:
            self.pre_converter = converter[0]
            self.post_converter = converter[1]
        elif type(converter) is dict:
            pass # TODO

    def __call__(self, f):
        
        def wrapped(*args, **kwargs):
            
            user_email = get_user()
            if user_email == 'User not found':
                return Response('Please contact an administrator to register.', status=401, mimetype='application/json')
                
            if type(self.action) == dict:
                action = Action(self.action[request.method])
            else:
                action = Action(self.action)
            
            pre_kw, post_kw = action.keywords
            resource_name = get_value_from_request(pre_kw)
            if self.pre_converter and resource_name != App_name:
                resource_name = self.pre_converter(resource_name)
            elif self.converter and resource_name != App_name:
                resource_name = self.converter(resource_name)

            r = is_allowed(user_email, action.name, resource_name)
            INFO('Allowed? %s %s %s ',  resource_name, action.name, r.text)

            if r.content != b'Ok':
                return Response('Unauthorized', status=401, mimetype='application/json')
            else:
                # inject user and his memberships into view_func
                kwargs['user'] = {'email': user_email} 
                kwargs['memberships'] = get_users_memberships(user_email).json()
                result = f(*args, **kwargs)

                if post_kw is None or '*' in post_kw:
                    return result
                else:

                    if action.cmd is "write":
                        resource_name = get_value_from_return_value(post_kw, result, request.endpoint)
                        if self.post_converter:
                            resource_name = self.post_converter(resource_name)
                        elif self.converter:
                            resource_name = self.converter(resource_name)

                        _ = publish(resource_name, post_kw)
                        ## authorize the user for all actions of the created type :
                        actions = get_actions_for_type(post_kw).json()
                        for a in actions:
                            r = authorize(user_email, resource_name, a['name'])
                            if r.status_code == 201:
                                continue
                            else:
                                print(r.content)

                    elif action.cmd is "delete":
                        if post_kw == App_name:
                            pass
                        else:
                            resource_name = get_value_from_return_value(post_kw, result, request.endpoint)
                            if self.post_converter:
                                resource_name = self.post_converter(resource_name)
                            elif self.converter:
                                resource_name = self.converter(resource_name)

                            _ = delete(resource_name)

                    elif action.cmd is "update":
                        # what is there to update by Keepah?...
                        pass
                    elif action.cmd is "authorize":
                        resource_name = get_value_from_return_value(post_kw, result, request.endpoint)
                        if self.post_converter:
                            resource_name = self.post_converter(resource_name)
                        elif self.converter:
                            resource_name = self.converter(resource_name)

                        new_user = get_value_from_return_value("user", result, request.endpoint)
                        new_action = get_value_from_return_value("action", result, request.endpoint)
                        authorize(new_user, resource_name, new_action)
                    
                    elif action.cmd is "unauthorize":
                        resource_name = get_value_from_return_value(post_kw, result, request.endpoint)
                        if self.post_converter:
                            resource_name = self.post_converter(resource_name)
                        elif self.converter:
                            resource_name = self.converter(resource_name)

                        new_user = get_value_from_return_value("user", result, request.endpoint)
                        new_action = get_value_from_return_value("action", result, request.endpoint)
                        unauthorize(new_user, resource_name, new_action)

                    return result

        wrapped.__name__ = f.__name__ 

        return wrapped

def register_app(app, resources=[], overwrite=False):
    for k, v in app.config['AUTH_PARAMS'].items():
        globals()[k] = v

    typs = set()
    typs_act = dict()
    to_register = {'actions': [], 'resourceTypes': [], 'resources': []}

    def add(act):
        act = act.format_for_publishing()
        typ = act['resourceTypeName']
        typs.add(typ)
        try:
            typs_act[typ] += [act['name']]
        except KeyError:
            typs_act[typ] = [act['name']]
        to_register['actions'] += [act]
        
    for func in iter(app.view_functions.values()):
        if func.__closure__ is not None:
            for cell in func.__closure__:
                if isinstance(cell.cell_contents, Keepah) and 'action' in cell.cell_contents.__dict__.keys():
                    action = cell.cell_contents.action
                    if type(action) is dict:
                        for v in action.values():
                            A = Action(v)
                            add(A)
                    else:
                        A = Action(action)
                        add(A)
    for typ in typs:
        if typ:
            to_register['resourceTypes'] += [{'name': typ, 'displayName': typ.upper(), 'description': None}]
    
    INFO('found resourceTypes : %s', typs)
    INFO('mapping resourceTypes -> actions : %s', typs_act)

    def sorted_olist(olist):
        return sorted(olist, key=lambda r: r['name'])

    K_resources = sorted_olist(get_Keepahs_resources())
    K_actions = sorted_olist(get_actions())
    K_types = sorted_olist(get_types())
    Keepahs = {'actions': K_actions, 'resourceTypes': K_types, 'resources': K_resources}
    # pprint(["KEEPAHS =", Keepahs])

    App_Resource = {'displayName': 'master level', 'name': App_name, 'resourceTypeName': 'app'}
    to_register['resources'] += [App_Resource]
    if resources:
        if overwrite:
            to_register['resources'] += resources
        else:
            resources += [App_Resource]
            U_names = set([d['name'] for d in resources])
            resources += [d for d in K_resources if d['name'] not in U_names]
            to_register['resources'] = resources
    else:
        if not overwrite:
            to_register['resources'] = K_resources

    to_register['resources'] = sorted_olist(to_register['resources'])
    to_register['resourceTypes'] = sorted_olist(to_register['resourceTypes'])
    to_register['actions'] = sorted_olist(to_register['actions'])

    INFO('***** REGISTERING FOLLOWING CONTENT BY KEEPAH : ********')
    pprint(["TO_REGISTER =", to_register])

    to_register['contentURL'] = contentURL
    to_register['displayName'] = App_name
    to_register['name'] = App_name.lower()

    reg = KeepahRequest(requests.put, 'register', data=to_register)
    pprint(["Registered Resources :", sorted_olist(get_Keepahs_resources())])
    return reg