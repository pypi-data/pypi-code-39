def get_ns(ns):
    namespaces = {
        "link": "{http://www.xbrl.org/2003/linkbase}",
        "xbrli": "{http://www.xbrl.org/2003/instance}",
        "xl": "{http://www.xbrl.org/2003/XLink}",
        "xlink": "{http://www.w3.org/1999/xlink}",
        "xml": "{http://www.w3.org/XML/1998/namespace}",
        "xsi": "{http://www.w3.org/2001/XMLSchema-instance}",
        "xsd": "{http://www.w3.org/2001/XMLSchema}"
    }
    return namespaces[ns]
