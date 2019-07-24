"""
A resolver based on the Mycroft Adapt intent parser.
"""


import re
from time import time
from ast import Str, Expr, parse

from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine

from neulang.base import BaseResolver


class AdaptResolver(BaseResolver):
    def __init__(self):
        self._pifs = {}
        super().__init__()
        self._ad_test = re.compile(r"^add_adapt_handler(\s.+)?")
        self._eng = IntentDeterminationEngine()
        return

    def resolve(self, o_node):
        if not self.is_adapt(o_node):
            return False
        a_node = None
        head = o_node.get("head")
        h_match = self._ad_test.match(head)

        if h_match:
            a_node = self.add_handler(o_node)
            assert a_node is None, f"None expected but got {type(a_node).__name__}"

        else:
            a_node = self.nl_call(o_node)
        return a_node

    def add_handler(self, data):
        engine = self._eng
        ignores = ["intent_parts", "body"]
        data = self._node_to_list(data, ignore_first=ignores)
        if not len(data) in [1, 2]:
            raise ValueError(f"adapt handler takes 1 or 2 fields")
        matches = data[0].get("intent_parts")
        assert all(
            [isinstance(m, Str) for m in matches]
        ), f"Expected all strings for intent parts"
        itt_parts = [m.s for m in matches]
        th = f"ad_{abs(hash(time()))}"

        for idx, ip in enumerate(itt_parts[:]):
            # hack if no named groups in rx
            ip_fix = ip

            while re.search(r"<<\w+>>", ip_fix):
                ip_fix = ip_fix.replace("<<", "(?P<").replace(">>", ">.+)")
            ip = ip_fix
            if not ("req_" in ip or "opt_" in ip):
                ip = f"(?P<req_{th}__{idx}>{ip})"
            itt_parts[idx] = ip
        topic = "neulang.resolvers.adapt.intent_parts_lists"
        self._pubsub.pub(topic, itt_parts)
        ib = IntentBuilder(f"{th}")
        ipn_rx = re.compile(r"P<\w+>.")

        for part in itt_parts:
            intermed = [
                ipn[2:-2]
                if not ipn[2:-2].isidentifier()
                else ib.optionally(ipn[2:-2].partition("_")[-1])
                if "opt_" in ipn
                else ib.require(ipn[2:-2].partition("_")[-1])
                if "req_" in ipn
                else None
                for ipn in ipn_rx.findall(part)
            ]
            if None in intermed:
                cnt = intermed.count(None)
                raise ValueError(
                    f'found {cnt} named group{"s" if cnt > 1 else ""} missing a "req_" or "opt" in "{part}"'
                )
            bad = [i for i in intermed if isinstance(i, str)]
            if any(bad):
                n = "are" if len(bad) > 1 else "is"
                raise NameError(
                    "all intent part names must be valid identifiers; {} {} not".format(
                        '", "'.join(bad), n
                    )
                )
            part = part.replace("opt_", "").replace("req_", "")
            engine.register_regex_entity(part)
        itt = ib.build()
        engine.register_intent_parser(itt)
        if len(data) == 1:
            return None
        body = data[1].get("body", [])
        body = [Expr(a_n) if not type(a_n) in self._stmt_types else a_n for a_n in body]
        pif = body or []
        self._pifs[th] = pif
        return None

    def nl_call(self, data):
        """Convert a natural language 'call' into a list of nodes."""
        head = data.get("head")
        body = data.get("body", [])
        itt = context = p_body = None
        engine = self._eng
        anl = []

        if body:
            # process body
            p_body = self._node_to_list(data)
        intents = [i for i in engine.determine_intent(head)]
        if not intents:
            return False
        itt = intents[0]
        bit = itt.get("intent_type")
        pif = self._pifs.get(bit)
        if not pif:
            return False
        assert isinstance(pif, list), f"Unable to resolve `{head}`"
        del itt["intent_type"]
        del itt["confidence"]
        itta = [
            parse(f'{k}="{v}"').body[0]
            for k, v in itt.items()
            if not k.startswith(f"{bit}__")
        ]
        anl.extend(itta)
        th = f"nl_{abs(hash(time()))}"

        if p_body:
            im = []
            left = [
                im.append(nd)
                if hasattr(nd, "lineno")
                else im.extend(nd)
                if isinstance(nd, list) and all([hasattr(n, "lineno") for n in nd])
                else nd
                for nd in p_body
                if nd
            ]
            assert not any(left), "Some items not properly processed"
            anl.extend(im)
            self._pifs[bit.replace("ad", "nl")] = im

        else:
            p_body = self._pifs.get(bit.replace("ad", "nl"), [])
            anl.extend(p_body)
        anl.extend(pif)
        return anl

    def is_adapt(self, node):
        # Just a stub until a way to detect
        return True
