import os, json, time, base64, hashlib, secrets
from cryptography.fernet import Fernet

CONFIG_FILE = "config.json"
KEY_FILE = "secret.key"

# ================= ENCRYPTION =================

def load_key():
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as f:
            f.write(Fernet.generate_key())
    return open(KEY_FILE, "rb").read()

def encrypt(data: bytes) -> bytes:
    return Fernet(load_key()).encrypt(data)

def decrypt(data: bytes) -> bytes:
    return Fernet(load_key()).decrypt(data)

# ================= CONFIG =================

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"users": {}, "audit": []}
    with open(CONFIG_FILE, "rb") as f:
        return json.loads(decrypt(f.read()))

def save_config(cfg):
    with open(CONFIG_FILE, "wb") as f:
        f.write(encrypt(json.dumps(cfg, indent=2).encode()))

# ================= HASHING =================

def hash_secret(v: str) -> str:
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", v.encode(), salt, 200_000)
    return base64.b64encode(salt + h).decode()

def verify_secret(v: str, stored: str) -> bool:
    d = base64.b64decode(stored)
    return hashlib.pbkdf2_hmac("sha256", v.encode(), d[:16], 200_000) == d[16:]

# ================= AUDIT =================

def audit(user: str, action: str):
    cfg = load_config()
    cfg["audit"].append({
        "time": int(time.time()),
        "user": user,
        "action": action
    })
    save_config(cfg)

# ================= USERS =================

def create_user(username: str, password: str, pin: str | None = None):
    cfg = load_config()
    cfg["users"][username] = {
        "password": hash_secret(password),
        "pin": hash_secret(pin) if pin else None,
        "github_id": None,
        "google_id": None,
        "recovery": []
    }
    audit(username, "account_created")
    save_config(cfg)

def login(username: str, password: str, pin: str | None = None) -> bool:
    cfg = load_config()
    user = cfg["users"].get(username)
    if not user:
        return False
    if not verify_secret(password, user["password"]):
        return False
    if user["pin"] and not verify_secret(pin or "", user["pin"]):
        return False

    audit(username, "login_password")
    return True

def change_password(username: str, old: str, new: str) -> bool:
    cfg = load_config()
    user = cfg["users"].get(username)
    if not user or not verify_secret(old, user["password"]):
        return False
    user["password"] = hash_secret(new)
    audit(username, "password_changed")
    save_config(cfg)
    return True

# ================= OAUTH =================

def link_oauth(username: str, provider: str, oid: str):
    cfg = load_config()
    cfg["users"][username][f"{provider}_id"] = oid
    audit(username, f"{provider}_linked")
    save_config(cfg)

def oauth_login(provider: str, oid: str):
    cfg = load_config()
    for u, d in cfg["users"].items():
        if d.get(f"{provider}_id") == oid:
            audit(u, f"login_{provider}")
            return u
    return None

# ================= 2FA =================

def enable_2fa(username: str):
    cfg = load_config()
    codes = [secrets.token_hex(4) for _ in range(5)]
    cfg["users"][username]["recovery"] = [hash_secret(c) for c in codes]
    audit(username, "2fa_enabled")
    save_config(cfg)
    return codes

def recover_account(username: str, code: str) -> bool:
    cfg = load_config()
    user = cfg["users"].get(username)
    if not user:
        return False
    for h in user["recovery"]:
        if verify_secret(code, h):
            user["recovery"].remove(h)
            audit(username, "account_recovered")
            save_config(cfg)
            return True
    return False