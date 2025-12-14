import tkinter as tk
from tkinter import messagebox, simpledialog
from code_it_for_it import login, change_password, enable_2fa, oauth_login, link_oauth, audit
from oauth_client import github_login, google_login
from hashlib import sha256
import json
from cryptography.fernet import Fernet

def load_encoded_secrets():
    with open("encoded_secrets.json", "r") as f:
        encoded_secrets = json.load(f)
    return encoded_secrets

def decode_secret(encoded_secret, key):
    cipher = Fernet(key)
    return cipher.decrypt(encoded_secret).decode()

def get_secret_key():
    return b'9tf7hyuCCa-idN2gISr2NkTA8UMigL7RMPBEdie6oDk='

encoded_secrets = load_encoded_secrets()

github_client_id = decode_secret(encoded_secrets["github_id"].encode(), get_secret_key())
github_client_secret = decode_secret(encoded_secrets["github_secret"].encode(), get_secret_key())
google_client_id = decode_secret(encoded_secrets["google_id"].encode(), get_secret_key())
google_client_secret = decode_secret(encoded_secrets["google_secret"].encode(), get_secret_key())

RAW_ADMIN_CODE = """kP!9f@#A7%&B(*d2Qw8^Rs$Z1m)..."""
ADMIN_HASH = sha256(RAW_ADMIN_CODE.encode()).hexdigest()

current_user: str | None = None
current_role: str = "user"

root = tk.Tk()
root.geometry("420x520")
root.title("Secure Login")

tk.Label(root, text="Username").pack()
u = tk.Entry(root)
u.pack()
tk.Label(root, text="Password").pack()
p = tk.Entry(root, show="*")
p.pack()
tk.Label(root, text="PIN").pack()
pin = tk.Entry(root, show="*")
pin.pack()

def verify_secret(code: str, hashed: str) -> bool:
    return sha256(code.encode()).hexdigest() == hashed

def admin_prompt() -> bool:
    code = simpledialog.askstring("Admin Login", "Admin Secret Code", show="*")
    if code and verify_secret(code, ADMIN_HASH):
        audit(current_user or "UNKNOWN", "ADMIN_LOGIN_SUCCESS")
        return True
    audit(current_user or "UNKNOWN", "ADMIN_LOGIN_FAILED")
    return False

def open_main_page():
    main_win = tk.Toplevel(root)
    main_win.title("Main Page")
    main_win.geometry("500x400")
    
    tk.Label(main_win, text=f"Welcome {current_user} ({current_role})", font=("Arial", 16)).pack(pady=10)
    tk.Button(main_win, text="Logout", command=lambda: logout(main_win)).pack(pady=5)
    
    dvd_canvas = tk.Canvas(main_win, width=400, height=300, bg="black")
    dvd_canvas.pack(pady=20)
    dvd_logo = dvd_canvas.create_text(50, 50, text="DVD", fill="white", font=("Arial", 24, "bold"))
    
    dx, dy = 3, 3
    def move_logo():
        nonlocal dx, dy
        coords = dvd_canvas.bbox(dvd_logo)
        if coords:
            x1, y1, x2, y2 = coords
            if x2 >= 400 or x1 <= 0:
                dx = -dx
            if y2 >= 300 or y1 <= 0:
                dy = -dy
            dvd_canvas.move(dvd_logo, dx, dy)
        dvd_canvas.after(30, move_logo)
    move_logo()

def logout(window):
    global current_user, current_role
    current_user = None
    current_role = "user"
    window.destroy()
    root.deiconify()

def change_pass():
    old = simpledialog.askstring("Old", "Old password", show="*") or ""
    new = simpledialog.askstring("New", "New password", show="*") or ""
    if change_password(current_user or "", old, new):
        messagebox.showinfo("OK", "Password changed")
    else:
        messagebox.showerror("Fail", "Wrong password")

def login_btn():
    global current_user, current_role
    username = u.get() or ""
    password = p.get() or ""
    user_pin = pin.get() or ""
    
    if not login(username, password, user_pin):
        messagebox.showerror("Fail", "Login failed")
        return
    
    current_user = username
    
    if messagebox.askyesno("Admin", "Login as admin?"):
        if admin_prompt():
            current_role = "admin"
        else:
            messagebox.showerror("Denied", "Bad admin code")
            return
    else:
        current_role = "user"
    
    root.withdraw()
    open_main_page()

def gh():
    global current_user, current_role
    r = github_login()
    user = oauth_login("github", r["id"])
    if user:
        current_user = user
        current_role = "user"
        root.withdraw()
        open_main_page()

def gg():
    global current_user, current_role
    r = google_login()
    user = oauth_login("google", r["id"])
    if user:
        current_user = user
        current_role = "user"
        root.withdraw()
        open_main_page()

tk.Button(root, text="Login", command=login_btn).pack(pady=5)
tk.Button(root, text="GitHub Login", command=gh).pack(pady=5)
tk.Button(root, text="Google Login", command=gg).pack(pady=5)

root.mainloop()
