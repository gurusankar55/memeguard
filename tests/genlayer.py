# Minimal mock of the genlayer runtime, only for tests/test_v2_flow.py
import types
class _A:
    def __init__(s,h): s.as_hex=h
class _Msg: sender_address=_A("0x0"); value=0
def _dec(f): return f
class _W:
    payable=staticmethod(_dec)
    def __call__(s,f): return f
class _P: write=_W(); view=staticmethod(_dec)
class _Web:
    page=""
    def render(s,url,mode="text"): return _Web.page
class _ND:
    web=_Web(); answer="OK"
    def exec_prompt(s,p): return _ND.answer
class _EQ:
    @staticmethod
    def strict_eq(f): return f()
class gl:
    message=_Msg(); Contract=object; public=_P(); nondet=_ND(); eq_principle=_EQ()
    @staticmethod
    def get_contract_at(a):
        class X:
            def emit_transfer(s,value): pass
        return X()
def u256(x): return x
