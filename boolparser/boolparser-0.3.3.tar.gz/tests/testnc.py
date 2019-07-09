


def test_trivial():
    from boolparser import BoolParser, EvaluateVariable
    
    d=dict(a=1,b=2,c=3,d=4)
    def define_class(dic):
        class d_ev(EvaluateVariable):
            def eval(self):
                return dic[self.value]
        return d_ev
    bp = BoolParser(define_class(d))
    assert bp.parse("a==1")
    assert not bp.parse("a>1")
    assert not bp.parse("!b==2")
    assert not bp.parse("!(b==2)")
    assert bp.parse("!b==0")

def test_nc():
    import netCDF4
    import os
    from boolparser.core import BoolParser, EvaluateVariable

    class ncar(object):
        def __init__(self,var):
            self.var = var
            return
        def __ge__(self, num):
            return self.var>=num
        def __le__(self, num):
            return self.var<=num
        def __gt__(self, num):
            return self.var>num
        def __lt__(self, num):
            return self.var<num

    def define_class(nc):
        class ev_nc(EvaluateVariable):
            def eval(self):
                if self.value in nc.variables:
                    return ncar(nc.variables[self.value][:])
                elif self.value in nc.dimensions:
                    return ncar(nc.dimensions[self.value][:])
                else:
                    raise NameError("Not a variable: {0}".format(self.value))
                    return self.value
        return ev_nc

    _ROOT = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(_ROOT, 'data', "adr32.nc")
    nc = netCDF4.Dataset(filename)
    nceval = define_class(nc)
    bp = BoolParser(nceval)
    test = """(SOLAR_ZENITHAL_ANGLE>55)&(SOLAR_ZENITHAL_ANGLE<56)"""
    for line in test.split("\n"):
        res = bp.parse(line)
        assert (res.size == 101)
        # if any(res):
        # print (nc.variables["SOLAR_ZENITHAL_ANGLE"][res])


if __name__=="__main__":
    test_nc()