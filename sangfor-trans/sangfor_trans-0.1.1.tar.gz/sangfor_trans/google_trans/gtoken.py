# -*- coding: utf-8 -*-
import ast
import math
import re
import time

import requests


from sangfor_trans.google_trans.compat import PY3
from sangfor_trans.google_trans.compat import unicode
from sangfor_trans.google_trans.utils import rshift


class TokenAcquirer(object):
    """
    Google翻译token生成类
    使用令牌授权请求，令牌生成基于翻译文本和特定的算法，且每小时更新一次

    Example usage:
        >>> from google_trans.gtoken import TokenAcquirer
        >>> acquirer = TokenAcquirer()
        >>> text = 'test'
        >>> tk = acquirer.do(text)
        >>> tk
        950629.577246
    """

    # 使用非贪婪模式匹配，包括换行符
    RE_TKK = re.compile(r'tkk:\'(.+?)\'', re.DOTALL)
    # RE_RAWTKK = re.compile(r'tkk:\'(.+?)\'', re.DOTALL)

    def __init__(self, tkk='0', session=None, host='translate.google.com'):
        """
        初试化ttk参数和host
        “translate.google.com”：需翻墙
        “translate.google.cn”： 无需翻墙
        """
        self.session = session or requests.Session()
        self.tkk = tkk
        self.host = host if 'http' in host else 'https://' + host

    def _update(self):
        """update tkk
        """
        now = math.floor(int(time.time() * 1000) / 3600000.0)
        # TKK有效的时候，不需要跟新
        if self.tkk and int(self.tkk.split('.')[0]) == now:
            return

        r = self.session.get(self.host)

        raw_tkk = self.RE_TKK.search(r.text)
        if raw_tkk:
            self.tkk = raw_tkk.group(1)
            return

        # 替换var保留字后成Python代码
        code = unicode(self.RE_TKK.search(r.text).group(1)).replace('var ', '')
        # 转义特殊ascii字符比如 \x3d(=)
        if PY3:  
            code = code.encode().decode('unicode-escape')
        else: 
            code = code.decode('string_escape')

        if code:
            tree = ast.parse(code)
            visit_return = False
            operator = '+'
            n, keys = 0, dict(a=0, b=0)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    name = node.targets[0].id
                    if name in keys:
                        if isinstance(node.value, ast.Num):
                            keys[name] = node.value.n
                        # 节点值对象判断
                        elif isinstance(node.value, ast.UnaryOp) and isinstance(node.value.op, ast.USub):  
                            keys[name] = -node.value.operand.n
                elif isinstance(node, ast.Return):
                    visit_return = True
                elif visit_return and isinstance(node, ast.Num):
                    n = node.n
                elif visit_return and n > 0:
                    if isinstance(node, ast.Add):  
                        pass
                    elif isinstance(node, ast.Sub):  
                        operator = '-'
                    elif isinstance(node, ast.Mult):  
                        operator = '*'
                    elif isinstance(node, ast.Pow):  
                        operator = '**'
                    elif isinstance(node, ast.BitXor):  
                        operator = '^'
            # 使用安全eval方法，避免异常
            clause = compile('{1}{0}{2}'.format(operator, keys['a'], keys['b']), '', 'eval')
            value = eval(clause, dict(__builtin__={}))
            result = '{}.{}'.format(n, value)

            self.tkk = result

    def _lazy(self, value):
        """
        该方法的原始代码如下格式:
           ... code-block: javascript
               var ek = function(a) {
                return function() {
                    return a;
                };
               }
        """
        return lambda: value

    def _xr(self, a, b):
        size_b = len(b)
        c = 0
        while c < size_b - 2:
            d = b[c + 2]
            d = ord(d[0]) - 87 if 'a' <= d else int(d)
            d = rshift(a, d) if '+' == b[c + 1] else a << d
            a = a + d & 4294967295 if '+' == b[c] else a ^ d

            c += 3
        return a

    def acquire(self, text):
        a = []
        for i in text:
            val = ord(i)
            if val < 0x10000:
                a += [val]
            else:
                a += [
                    math.floor((val - 0x10000)/0x400 + 0xD800),
                    math.floor((val - 0x10000)%0x400 + 0xDC00)
                    ]

        b = self.tkk if self.tkk != '0' else ''
        d = b.split('.')
        b = int(d[0]) if len(d) > 1 else 0

        e = []
        g = 0
        size = len(text)
        while g < size:
            l = a[g]
            if l < 128:
                e.append(l)       
            else:
                if l < 2048:
                    e.append(l >> 6 | 192)
                else:
                    # append calculated value if l matches special condition
                    if (l & 64512) == 55296 and g + 1 < size and \
                            a[g + 1] & 64512 == 56320:
                        g += 1
                        l = 65536 + ((l & 1023) << 10) + (a[g] & 1023) # This bracket is important
                        e.append(l >> 18 | 240)
                        e.append(l >> 12 & 63 | 128)
                    else:
                        e.append(l >> 12 | 224)
                    e.append(l >> 6 & 63 | 128)
                e.append(l & 63 | 128)   
            g += 1
        a = b
        for i, value in enumerate(e):
            a += value
            a = self._xr(a, '+-a^+6')
        a = self._xr(a, '+-3^+b+-f')
        a ^= int(d[1]) if len(d) > 1 else 0
        if a < 0:  
            a = (a & 2147483647) + 2147483648
        a %= 1000000  # int(1E6)

        return '{}.{}'.format(a, a ^ b)

    def do(self, text):
        self._update()
        tk = self.acquire(text)
        return tk
