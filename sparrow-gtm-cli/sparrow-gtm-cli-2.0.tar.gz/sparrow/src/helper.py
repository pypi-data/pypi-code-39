import json


def extract_info(src: list or dict, what="trigger", ids=True) -> list:
    """
    extract_info extracts variables and tags ids recursively from dict
    extract_info can operate on list or nested lists as well

    :param ids:
    :param src: accepts lists or dict
    :param what: accepts 3 options trigger, tag and variable default to trigger
    :return: list: output a list of unique ids
    """
    i = []
    o = []

    if type(src) is dict:
        t = 'tagId' if ids else 'name'
        tr = 'firingTriggerId' if ids else 'name'
        v = 'variableId' if ids else 'name'
        if what == "tag":
            for tag in src.get('containerVersion').get('tag'):
                if tag.get(t):
                    i.append(tag[t])
        elif what == "trigger":
            for tag in src.get('containerVersion').get('tag'):
                if tag.get(tr):
                    i.append(tag[tr])
        elif what == "variable":
            try:
                for variable in src.get('containerVersion').get('variable'):
                    if variable.get(v):
                        i.append(variable[v])
            except TypeError:
                """ignore error no need to output any critical message"""
                pass

    else:
        i = src

    def deep_extract(ls):
        if type(ls) is list:
            for ids in ls:
                if not o.__contains__(ids):
                    deep_extract(ids)
        else:
            if not o.__contains__(ls):
                o.append(ls)

        return o

    for tr in i:
        deep_extract(tr)

    return o


def info(src: dict):
    if not src.get('containerVersion'):
        err = "sparrow error: GTM configuration file is not valid"
        print(err)
        exit(1)
    else:
        tags = len(extract_info(src, what='tag'))
        triggers = len(extract_info(src, what='trigger'))
        variables = len(extract_info(src, what='variable'))
        output = f"""
-----------------------------------------------------------
|                   General container info                |
-----------------------------------------------------------

Export-time:                {src['exportTime']}
Name:                       {src['containerVersion']['container'].get('name')}
Domain:                     {src['containerVersion']['container'].get('domainName')}
Public-id:                  {src['containerVersion']['container'].get('publicId')}
Container-id:               {src['containerVersion']['container'].get('containerId')}
Context:                    {src['containerVersion']['container'].get('usageContext')}
#Tags:                      {tags}
#Triggers:                  {triggers}
#Variables:                 {variables}

    """
        return output


def general_help(gray=False):
    if not gray:
        general_cli_help = """
Usage: sparrow [globals] <command> 

Globals:
  -v, --version                                 output the version number
  -h, --help                                    output usage information

Commands:
  extract <file.json> <input.json>              extract configuration file from source
  info <file.json>                              print information about the container
  migrate <file.json>                           migrate legacy container to v5


Examples

sparrow extract configuration.json target.json
    output -> output.json should be created in the current working directory

sparrow info configuration.json
    output -> Container related info

"""
        return general_cli_help
    else:
        general_cli_help = """
Usage: sparrow [globals] <command> 

Globals:
  -v, --version                                 output the version number
  -h, --help                                    output usage information

Commands:
  extract <file.json> <input.json> [flags]      extract configuration file from source
  info <file.json>                              print information about the container
  migrate <file.json>                           migrate legacy container to v5
  

Examples

sparrow extract configuration.json target.json
    output -> output.json should be created in the current working directory

sparrow info configuration.json
    output -> Container related info

        """
        return general_cli_help


def command_not_found(cmd):
    err = f"""sparrow command not found {cmd}\n"""
    return err


def migrate(f):
    with open(f, "r", encoding='utf-8') as fi:
        """ first case to migrate container version"""
        source = json.load(fi)
        sdk = source['containerVersion']["container"]["usageContext"][0] + "_SDK_5"
        key = source['containerVersion']["container"]["usageContext"][0]
        mand = {
            "type" : "BOOLEAN",
            "key"  : "overrideGaSettings",
            "value": "true"
        }

        source['containerVersion']["container"]["usageContext"][0] = sdk

        ecomm = {
            "type" : "TEMPLATE",
            "key"  : "readDataFrom",
            "value": "FIREBASE_EVENT_DATA"
        }
        for t in source['containerVersion']['tag']:
            if t['type'] == 'ua':
                t["parameter"].append(mand)
                for p in t["parameter"]:
                    if p.get("key") == "useEcommerceDataLayer":
                        del p
                        t["parameter"].append(ecomm)

        def1 = {
            "type" : "TEMPLATE",
            "key"  : "defaultValue",
            "value": "NA"
        }
        def2 = {
            "type" : "TEMPLATE",
            "key"  : "eventType",
            "value": "CUSTOM"
        }

        defvalue = {
            "type" : "BOOLEAN",
            "key"  : "setDefaultValue",
            "value": "true"
        }

        for v in source['containerVersion']['variable']:
            if v["type"] == "v":
                v["type"] = "md"
                v['parameter'].append(def1)
                v['parameter'].append(def2)

        for v in source['containerVersion']['variable']:
            if v.get('parameter') is not None:
                for p in v['parameter']:
                    if p.get("key") == "setDefaultValue":
                        p["value"] = True

        with open('output_v5.json', "w", encoding='utf-8') as f:
            json.dump(fp=f, obj=source, ensure_ascii=False)
            print("Successful > output_v5.json generated")
