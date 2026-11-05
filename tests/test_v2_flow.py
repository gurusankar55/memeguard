# Local simulation of the MemeGuard v2 flow with a mock genlayer module.
# Run: python tests/test_v2_flow.py
import sys; sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import os; exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'contracts', 'meme_guard.py')).read())
from genlayer import gl, _Web, _ND
W=10**18
def as_(a,v=0): gl.message.sender_address=type(gl.message.sender_address)(a); gl.message.value=v
m=MemeGuard()
C="0xcreatorabcdef12"; A="0xaaaa"; B="0xbbbb"; D="0xdddd"
as_(C,W//10); m.create_coin("Moon","MOON","https://x.io","We will ship the site soon ok","")
_Web.page="memeguard-verify:moon:"+C[-8:]+" moon coin"; m.guard_check(0)
c=json.loads(m.get_coin(0)); assert c["status"]=="LIVE"
as_(A,5*W); m.buy(0); as_(B,1*W); m.buy(0); as_(D,1*W); m.buy(0)
# D sells then buys with balance
as_(D); m.sell(0, m.balance_of(0,D)//2)
cl=int(m.claimable_of(D)); print("D claimable", cl/W)
m.buy_with_balance(0, 200)  # 0.2 GEN
print("D after buy_with_balance", int(m.claimable_of(D))/W)
try: m.buy_with_balance(0,10**9); print("BAD")
except Exception as e: print("ok:",e)
# freeze via report
_ND.answer="SCAM_SIGNS"; as_(B); m.report_coin(0,"scam page now")
c=json.loads(m.get_coin(0)); print("status",c["status"])
# small holder votes -> not enough
as_(D); m.vote_refund(0); print("after D vote", json.loads(m.get_coin(0))["status"])
try: as_(C); m.vote_refund(0); print("BAD")
except Exception as e: print("ok:",e)
as_(B); m.vote_refund(0); print("after B vote", json.loads(m.get_coin(0))["status"])
c=json.loads(m.get_coin(0)); print("burned", c["creator_burned"], "locked", c["creator_locked"])
try: as_(C); m.appeal_freeze(0); print("BAD")
except Exception as e: print("ok:",e)
pool=c["pool_wei"]
tot=0
for x in (A,B,D):
    as_(x); r=int(m.refund_of(0,x)); m.claim_refund(0); tot+=r; print(x,"refund",r/W)
c=json.loads(m.get_coin(0)); print("pool left",c["pool_wei"]/W, "paid",tot/W,"of",pool/W)
try: as_(A); m.claim_refund(0); print("BAD")
except Exception as e: print("ok:",e)
try: as_(A); m.sell(0,1); print("BAD")
except Exception as e: print("ok:",e)
# appeal path on new coin
as_(B,W//10); m.create_coin("Cat","CATZ","https://y.io","Site and repo live in 30 days","")
_ND.answer="OK"; _Web.page="memeguard-verify:catz:"+B[-8:]; m.guard_check(1)
as_(A,W); m.buy(1); _ND.answer="MISMATCH"; as_(D); m.report_coin(1,"site changed")
as_(A); m.vote_refund(1)  # A is only holder -> 100% -> refund
print("coin1", json.loads(m.get_coin(1))["status"])
as_(D,W//10); m.create_coin("Dog2","DOGX","https://z.io","Site and repo live in 30 days","")
_ND.answer="OK"; _Web.page="memeguard-verify:dogx:"+D[-8:]; m.guard_check(2)
_ND.answer="SCAM_SIGNS"; as_(A); m.report_coin(2,"scam scam")
_ND.answer="OK"; as_(D); m.appeal_freeze(2); c=json.loads(m.get_coin(2)); print("appeal",c["status"],c["appeal_result"])
_ND.answer="SCAM_SIGNS"; as_(B); m.report_coin(2,"again bad")
try: as_(D); m.appeal_freeze(2); print("BAD")
except Exception as e: print("ok:",e)
print("ALL DONE")
