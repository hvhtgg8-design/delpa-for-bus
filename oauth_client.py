import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
from cryptography.fernet import Fernet
import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_FILE = os.path.join(BASE_DIR, "encoded_secrets.json")

# --- Load encoded secrets ---
with open(SECRETS_FILE, "r") as f:
    data = json.load(f)

SECRET_KEY = data["key"].encode()
cipher = Fernet(SECRET_KEY)

GITHUB_CLIENT_ID = cipher.decrypt(data["github_id"].encode()).decode()
GITHUB_CLIENT_SECRET = cipher.decrypt(data["github_secret"].encode()).decode()
GOOGLE_CLIENT_ID = cipher.decrypt(data["google_id"].encode()).decode()
GOOGLE_CLIENT_SECRET = cipher.decrypt(data["google_secret"].encode()).decode()

REDIRECT_URI = "http://localhost:8765/callback"

# --- Global variable to store the OAuth code ---
OAUTH_CODE = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global OAUTH_CODE
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            OAUTH_CODE = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h2>Login successful! You can close this window.</h2>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h2>Error: code not found</h2>")

def run_local_server() -> str:
    global OAUTH_CODE
    OAUTH_CODE = None
    server = HTTPServer(("localhost", 8765), OAuthHandler)
    server.handle_request()  # wait for a single request
    if not OAUTH_CODE:
        raise Exception("Failed to retrieve OAuth code")
    return OAUTH_CODE

# --- GitHub Login ---
def github_login():
    auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=read:user user:email"
    )
    webbrowser.open(auth_url)
    code = run_local_server()

    token_resp = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }
    ).json()

    access_token = token_resp.get("access_token")
    if not access_token:
        raise Exception("GitHub OAuth failed")

    user_resp = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    return {"id": str(user_resp["id"]), "username": user_resp["login"]}

# --- Google Login ---
def google_login():
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
        f"&access_type=offline"
    )
    webbrowser.open(auth_url)
    code = run_local_server()

    token_resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        }
    ).json()

    access_token = token_resp.get("access_token")
    if not access_token:
        raise Exception("Google OAuth failed")

    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"alt": "json"},
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    return {"id": str(user_info["id"]), "username": user_info["email"]}