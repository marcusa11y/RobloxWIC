import os as _0
import ast as _1
import sys as _2
import zlib as _3
import base64 as _4
import string as _5
import random as _6
import builtins as _7
import argparse as _8

class _9:
    def __init__(self, _a: str, _b: bool=False, _c: int=1) -> None:
        self.__d = _a
        self.__e = []
        self.__f = {}
        self.__g = [chr(i) for i in range(256, 0x24976) if chr(i).isidentifier()]
        self.__h = _b
        if _c < 1:
            raise ValueError("Recursion length cannot be less than 1")
        else:
            self.__i = _c

    def obfuscate(self) -> str:
        self.__j()
        self.__k()

        __l = [
            self.__m,
            self.__n,
            self.__o
        ] * self.__i
        _6.shuffle(__l)

        if __l[-1] == self.__o:
            for _p, _q in enumerate(__l):
                if _q != self.__o:
                    __l[_p] = self.__o
                    __l[-1] = _q
                    break

        for _r in __l:
            _r()

        if self.__h:
            self.__s()
        return self.__d

    def __j(self) -> None:
        def _t(_u):
            if isinstance(_u, _1.Import):
                for _v in _u.names:
                    self.__e.append((None, _v.name))
            elif isinstance(_u, _1.ImportFrom):
                _w = _u.module
                for _v in _u.names:
                    self.__e.append((_w, _v.name))

            for _x in _1.iter_child_nodes(_u):
                _t(_x)

        _y = _1.parse(self.__d)
        _t(_y)
        self.__e.sort(reverse=True, key=lambda x: len(x[1]) + len(x[0]) if x[0] is not None else 0)

    def __k(self) -> None:
        for _w, _z in self.__e:
            if _w is not None:
                _A = "from %s import %s\n" % (_w, _z)
            else:
                _A = "import %s\n" % _z
            self.__d = _A + self.__d

    def __B(self, _C: str) -> str:
        if _C in self.__f.keys():
            return self.__f.get(_C)
        else:
            while True:
                _D = "".join(_6.choices(self.__g, k=_6.randint(10, 25)))
                if _D not in self.__f.values():
                    self.__f[_C] = _D
                    return _D

    def __j(self) -> None:
        _E = _1.parse(self.__d)
        _E.body.insert(0, _1.Expr(value=_1.Constant(":: You managed to break through BlankOBF v2; Give yourself a pat on your back! ::")))
        for _F, _G in enumerate(_E.body[1:]):
            if isinstance(_G, _1.Expr) and isinstance(_G.value, _1.Constant):
                _E.body[_F + 1] = _1.Pass()

            elif isinstance(_G, (_1.FunctionDef, _1.AsyncFunctionDef)):
                for _H in _G.body:
                    if isinstance(_H, _1.Expr) and isinstance(_H.value, _1.Constant):
                        _G.body[_G.body.index(_H)] = _1.Pass()

            elif isinstance(_G, _1.ClassDef):
                for _H in _G.body:
                    if isinstance(_H, _1.Expr) and isinstance(_H.value, _1.Constant):
                        _G.body[_G.body.index(_H)] = _1.Pass()

                    elif isinstance(_H, (_1.FunctionDef, _1.AsyncFunctionDef)):
                        for _I in _H.body:
                            if isinstance(_I, _1.Expr) and isinstance(_I.value, _1.Constant):
                                _H.body[_H.body.index(_I)] = _1.Pass()
        self.__d = _1.unparse(_E)

    def __J(self) -> None:
        _K = self.__d.splitlines()
        for _L in range(len(_K) - 1, 0, -1):
            if _6.randint(1, 10) > 3:
                _M = 0
                _N = "#"
                for _O in range(_6.randint(7, 55)):
                    _N += " " + "".join(_6.choices(self.__g, k=_6.randint(2, 10)))
                for _P in _K[_L]:
                    if _P != " ":
                        break
                    else:
                        _M += 1
                _K.insert(_L, (" " * _M) + _N)
        self.__d = "\n".join(_K)

    def __Q(self) -> None:
        class _R(_1.NodeTransformer):
            def __init__(self, _S: _9) -> None:
                self.__T = _S

            def __U(self, _V: str) -> None:
                if _V not in dir(_7) and _V not in [x[1] for x in self.__T.__e]:
                    return self.__T.__B(_V)
                else:
                    return _V

            def visit_Name(self, _W: _1.Name) -> _1.Name:
                if _W.id in dir(_7) or _W.id in [x[1] for x in self.__T.__e]:
                    _W = _1.Call(
                        func=_1.Call(
                            func=_1.Name(id="getattr", ctx=_1.Load()),
                            args=[_1.Call(func=_1.Name(id="__import__", ctx=_1.Load()), args=[self.visit_Constant(_1.Constant(value="builtins"))], keywords=[]),
                                  self.visit_Constant(_1.Constant(value="eval"))],
                            keywords=[]
                        ),
                        args=[_1.Call(func=_1.Name(id="bytes", ctx=_1.Load()), args=[_1.Subscript(value=_1.List(elts=[_1.Constant(value=x) for x in list(_W.id.encode())][::-1], ctx=_1.Load()), slice=_1.Slice(upper=None, lower=None, step=_1.Constant(value=-1))], ctx=_1.Store())], keywords=[])],
                        keywords=[]
                    )
                    return _W
                else:
                    _W.id = self.__U(_W.id)
                    return self.generic_visit(_W)

            def visit_FunctionDef(self, _X: _1.FunctionDef) -> _1.FunctionDef:
                _X.name = self.__U(_X.name)
                return self.generic_visit(_X)

            def visit_arg(self, _Y: _1.arg) -> _1.arg:
                _Y.arg = self.__U(_Y.arg)
                return _Y

            def visit_Constant(self, _Z: _1.Constant) -> _1.Constant:
                if isinstance(_Z.value, int):
                    _A0 = _6.randint(1, 2)
                    match _A0:
                        case 1:
                            _A1 = _6.randint(69**3, _2.maxsize)
                            _A2 = _Z.value * _A1
                            _A3 = _Z.value * (_A1 - 1)
                            _Z = _1.BinOp(left=_1.Constant(value=_A2), op=_1.Sub(), right=_1.Constant(value=_A3))
                        case 2:
                            _A1 = _6.randint(69**3, _2.maxsize)
                            _A4 = _6.randint(50, 500)
                            _Z = _1.BinOp(
                                left=_1.BinOp(
                                    left=_1.BinOp(
                                        left=_1.BinOp(
                                            left=_1.Constant(value=_A1 * 2),
                                            op=_1.Add(),
                                            right=_1.Constant(value=_Z.value * 2 * _A4)
                                        ),
                                        op=_1.FloorDiv(),
                                        right=_1.Constant(value=2)
                                    ),
                                    op=_1.Sub(),
                                    right=_1.Constant(value=_A1)
                                ),
                                op=_1.Sub(),
                                right=_1.Constant(value=_Z.value * (_A4 - 1))
                            )
                elif isinstance(_Z.value, str):
                    _A5 = list(_Z.value.encode())[::-1]
                    _Z = _1.Call(func=_1.Attribute(value=_1.Call(func=_1.Name(id="bytes", ctx=_1.Load()), args=[_1.Subscript(value=_1.List(elts=[_1.Constant(value=x) for x in _A5], ctx=_1.Load()), slice=_1.Slice(lower=None, upper=None, step=_1.Constant(value=-1)), ctx=_1.Load())], keywords=[]), attr="decode", ctx=_1.Load()), args=[], keywords=[])
                elif isinstance(_Z.value, bytes):
                    _A5 = list(_Z.value)[::-1]
                    _Z = _1.Call(func=_1.Name(id="bytes", ctx=_1.Load()), args=[_1.Subscript(value=_1.List(elts=[_1.Constant(value=x) for x in _A5], ctx=_1.Load()), slice=_1.Slice(lower=None, upper=None, step=_1.Constant(value=-1)), ctx=_1.Load())], keywords=[])
                return _Z

            def visit_Attribute(self, _A6: _1.Attribute) -> _1.Attribute:
                _A6 = _1.Call(func=_1.Name(id="getattr", ctx=_1.Load()), args=[_A6.value, _1.Constant(_A6.attr)], keywords=[])
                return self.generic_visit(_A6)

        _A7 = _1.parse(self.__d)
        _R(self).visit(_A7)
        self.__d = _1.unparse(_A7)

    def __m(self) -> None:
        _A8 = """
_0 = ""
_1 = ""
_2 = ""
_3 = ""

exec(__import__("zlib").decompress(__import__("base64").b64decode(_0 + _1 + _2 + _3)))
"""
        _A9 = _4.b64encode(_3.compress(self.__d.encode())).decode()
        _Aa = []
        for _Ab in range(0, len(_A9), int(len(_A9)/4)):
            _Aa.append(_A9[_Ab:_Ab + int(len(_A9)/4)])
        _Aa.reverse()

        _Ac = _1.parse(_A8)
        for _Ad in _1.walk(_Ac):
            if isinstance(_Ad, _1.Assign) and isinstance(_Ad.value, _1.Constant) and isinstance(_Ad.value.value, str) and _Aa:
                _Ae = "".join(_6.choices(_5.ascii_letters, k=_6.randint(5, 100)))
                _Af = "".join(_6.choices(_5.ascii_letters, k=_6.randint(5, 100)))
                _Ag = _Aa.pop()
                _Ad.value = _1.Subscript(
                    value=_1.Constant(value=_Ae + _Ag + _Af),
                    slice=_1.Slice(
                        upper=_1.Constant(value=len(_Ae) + len(_Ag)),
                        lower=_1.Constant(value=len(_Ae)),
                        step=None
                    ),
                    ctx=_1.Store()
                )
        self.__d = _1.unparse(_Ac)
        self.__Q()
        self.__J()

    def __n(self) -> None:
        _Ah = """
_ai = []
for _aj in range(1, 100):
    if _ai[_ak] ^ _aj == _ai[_al]:
        exec(__import__("zlib").decompress(bytes(map(lambda _am: _am ^ _aj, _ai[0:_ak] + _ai[_ak + 1: _al] + _ai[_al + 1:]))))
        break
"""
        _an = _6.randint(1, 100)
        _ak = _6.randbytes(1)[0]
        _al = _ak ^ _an

        _ai = list(map(lambda _ao: _an ^ _ao, _3.compress(self.__d.encode())))

        _ak = _6.randint(0, int(len(_ai)/2))
        _al = _6.randint(_ak, len(_ai) - 1)
        _ai.insert(_ak, _ak)
        _ai.insert(_al, _al)
        _Ah = _Ah.replace("_ak", str(_ak)).replace("_al", str(_al))

        _Ac = _1.parse(_Ah)
        for _Ad in _1.walk(_Ac):
            if isinstance(_Ad, _1.List):
                _Ad.elts = [_1.Constant(value=x) for x in _ai]

        self.__d = _1.unparse(_Ac)
        self.__Q()
        self.__J()

    def __o(self) -> None:
        _Ap = """
_aq = []
_data = list([int(x) for item in [_value.split(".") for _value in _aq] for x in item])
exec(compile(__import__("zlib").decompress(__import__("base64").b64decode(bytes(_data))), "<(*3*)>", "exec"))
"""
        def _ar(data: bytes) -> list:
            _as = []
            for _at in range(0, len(data), 4):
                _au = data[_at:_at+4]
                _as.append(".".join([str(x) for x in _au]))
            return _as

        _av = _4.b64encode(_3.compress(self.__d.encode()))
        _aw = _ar(_av)

        self.__d = _Ap
        self.__Q()
        _Ac = _1.parse(self.__d)
        for _Ad in _1.walk(_Ac):
            if isinstance(_Ad, _1.Assign) and isinstance(_Ad.value, _1.List):
                _Ad.value.elts = [_1.Constant(value=x) for x in _aw]
        self.__d = _1.unparse(_Ac)
        self.__J()

def _ax() -> None:
    _ay = _8.ArgumentParser(
        prog=_0.path.basename(__file__),
        description="BlankOBF v2: Obfuscates Python code to make it unreadable and hard to reverse."
    )
    _ay.add_argument("--input", "-i", required=True, help="The file containing the code to obfuscate", metavar="PATH")
    _ay.add_argument("--output", "-o", required=False,
                    help="The file to write the obfuscated code (defaults to Obfuscated_[input].py)",
                    metavar="PATH")
    _ay.add_argument("--recursive", required=False,
                    help="Recursively obfuscates the code N times (slows down the code; not recommended)",
                    metavar="N")
    _ay.add_argument("--include_imports", required=False, action="store_true",
                    help="Include the import statements on the top of the obfuscated file")

    _az = _ay.parse_args()

    if not _0.path.isfile(_az.input):
        print("Input file does not exist.")
        exit(1)

    if not _az.output:
        _az.output = "Obfuscated_%s.py" % (_0.path.splitext(_0.path.basename(_az.input))[0])

    with open(_az.input, "r", encoding="utf-8") as _A0:
        _A1 = _A0.read()

    _A2 = _9(_A1, _az.include_imports, int(_az.recursive) if _az.recursive else 1)
    _A3 = _A2.obfuscate()

    try:
        with open(_az.output, "w", encoding="utf-8") as _A0:
            _A0.write(_A3)
    except Exception:
        print("Unable to save the file.")

if __name__ == "__main__":
    _ax()