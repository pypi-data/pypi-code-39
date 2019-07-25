
class Action:
    def __init__(self, item):
        self.item = item
    
    def __call__(self, module):
        pass

class NotRecognized(RuntimeError):
    pass
    
class Scanner:
    def __call__(self, item):
        raise NotRecognized(item)
    
    def callback(self, item, module):
        return self(item)(module)
    
    def __and__(self, other):
        return AllOf([self, other])
    
    def __or__(self, other):
        return FirstOf([self, other])
    
    def __add__(self, other):
        return SomeOf([self, other])

    def __pos__(self):
        return pos(self)
    
    def __neg__(self):
        return neg(self)

def pos(scanner):
    if isinstance(scanner, (Pos, Neg)):
        return scanner if isinstance(scanner, Pos) else neg(scanner._scanner)
    else:
        return Pos(scanner)

def neg(scanner):
    if isinstance(scanner, (Pos, Neg)):
        return neg(scanner._scanner) if isinstance(scanner, Pos) else pos(scanner._scanner)
    else:
        return Neg(scanner)
    
class Pos(Scanner):
    def __init__(self, scanner):
        self._scanner = scanner

    def __call__(self, item):
        self._scanner(item)
        return Action(item)

class Neg(Scanner):
    def __init__(self, scanner):
        self._scanner = scanner

    def __call__(self, item):
        try:
            self._scanner(item)
        except NotRecognized:
            return Action(item)
        raise NotRecognized(item)

class CompoundAction(Action):
    def __init__(self, item, iaction):
        Action.__init__(self, item)
        self.iaction = list(iaction)
        
    def __call__(self, module):
        for a in self.iaction:
            a(module)

def compound_action(item, iaction):
    iaction = list(iaction)
    if not iaction:
        raise ValueError('Expected at least one action for compound_action()')
    if len(iaction) == 1:
        return iaction[0]
    return CompoundAction(item, iaction)

class MultiScanner(Scanner):
    def __init__(self, iscanner):
        Scanner.__init__(self)
        self.iscanner = list(iscanner)
        assert len(self.iscanner) > 0
            
class AllOf(MultiScanner):
    def __call__(self, item):
        iaction = [s(item) for s in self.iscanner]
        return compound_action(item, iaction)

def all_of(iscanner):
    iscanner = list(iscanner)
    if not iscanner:
        raise ValueError('Expected at least one scanner')
    if len(iscanner) == 1:
        return iscanner[0]
    return AllOf(iscanner)

class FirstOf(MultiScanner):
    def __call__(self, item):
        for s in self.iscanner:
            try:
                return s(item)
            except NotRecognized:
                pass
        raise NotRecognized(item)

def first_of(iscanner):
    iscanner = list(iscanner)
    if not iscanner:
        raise ValueError('Expected at least one scanner')
    if len(iscanner) == 1:
        return iscanner[0]
    return FirstOf(iscanner)


class SomeOf(MultiScanner):
    def __init__(self, iscanner, min_match=1):
        MultiScanner.__init__(self, iscanner)
        if min_match < 1:
            raise ValueError('Expected min_match >= 1')
        self.min_match = min_match
        
    def __call__(self, item):
        iaction = []
        for s in self.iscanner:
            try:
                iaction.append(s(item))
            except NotRecognized:
                pass
        n = len(iaction)
        if n < self.min_match or not n:
            raise NotRecognized(item)
        else:
            return compound_action(item, iaction)

def some_of(iscanner, min_match=1):
    if min_match < 1:
        raise ValueError('Expected min_match >= 1')
    iscanner = list(iscanner)
    n = len(iscanner)
    if n < min_match or not n:
        raise ValueError('Insufficient number of scanners')
    if n == 1:
        return iscanner[0]
    return SomeOf(iscanner, min_match=min_match)
