from Region import dB
from Region import OWNER as OWNER_ID

if OWNER_ID:
    auth = eval(dB.get("AUTH_USERS") or "[]")
    if OWNER_ID not in auth:
        auth.append(OWNER_ID)
        dB.set("AUTH_USERS", str(auth))

def get_auth():
    return eval(dB.get("AUTH_USERS") or "[]")


def is_auth(id):
    if id in eval(dB.get("AUTH_USERS") or "[]"):
        return True
    return False


def add_auth(id):
    auth = eval(dB.get("AUTH_USERS") or "[]")
    if id not in auth:
        auth.append(id)
        dB.set("AUTH_USERS", str(auth))


def rem_auth(id):
    auth = eval(dB.get("AUTH_USERS") or "[]")
    if id in auth:
        auth.remove(id)
        dB.set("AUTH_USERS", str(auth))