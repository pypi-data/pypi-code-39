from base64 import *
import zlib
import marshal


__Developer__ = "Nasir Ali"

"""
:INFO

DEV : Nasir Ali
GITHUB : github.com/nasirxo
FB : fb.com/nasir.xo

"""
#Encypt Code String
def NENC(code):
 xdat = b16encode(code)
 return marshal.dumps(zlib.compress(xdat))

#Decyot and Run Code String
def NRUN(code):
  exec(b16decode(zlib.decompress(marshal.loads(code))))


