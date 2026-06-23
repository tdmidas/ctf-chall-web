#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
  web_server.py  --  CTF Web Challenge: Cookie Manipulation
============================================================================
Simple Flask web app simulating an admin panel. The server sets a cookie
  role=user  when visited. Students must CHANGE the cookie to  role=admin
to access the /admin page and retrieve the FLAG.

NOTE: This is a lesson about "NEVER trust data from the client".
      Cookies are sent by the browser -> users can modify them -> unsafe
      for authorization.
============================================================================
"""
import os
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

FLAG = os.environ.get("CTF_FLAG", "UIT{c00k1e_n0t_s4f3}")

# ============================================================================
#  HTML TEMPLATES (simple, text-only)
# ============================================================================
STYLE = """
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Consolas', 'Courier New', monospace;
    background: #fff;
    color: #222;
    padding: 40px;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.7;
  }
  h1 { font-size: 1.3rem; margin-bottom: 16px; border-bottom: 1px solid #ccc; padding-bottom: 8px; }
  .info { margin: 12px 0; }
  .flag-box { margin-top: 20px; padding: 16px; background: #f0f0f0; border: 1px solid #aaa; font-size: 1.1rem; font-weight: bold; }
  a { color: #0066cc; }
  hr { border: none; border-top: 1px solid #ddd; margin: 20px 0; }
</style>
"""

HOME_PAGE = """<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><title>Web Challenge</title>""" + STYLE + """</head>
<body>
  <h1>Web Challenge - Cookie Manipulation</h1>

  <div class="info">
    Your current role: <strong>user</strong><br>
    The flag is only visible to <strong>admin</strong>.
  </div>

  <p><a href="/admin">Go to /admin page</a></p>

</body></html>"""

ADMIN_DENIED = """<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><title>Access Denied</title>""" + STYLE + """</head>
<body>
  <h1>Access Denied</h1>

  <div class="info">
    Your current role: <strong>{{ role }}</strong><br>
    You do not have permission to access this page.<br>
    Only admin can see the flag.
  </div>

  <p><a href="/">&larr; Go back</a></p>

</body></html>"""

ADMIN_OK = """<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"><title>Admin - FLAG</title>""" + STYLE + """</head>
<body>
  <h1>Welcome, Admin!</h1>

  <div class="info">
    You have successfully exploited the <strong>insecure cookie</strong> vulnerability.
  </div>

  <div class="flag-box">FLAG: {{ flag }}</div>

  <hr>

</body></html>"""


# ============================================================================
#  ROUTES
# ============================================================================
@app.route("/")
def home():
    resp = make_response(HOME_PAGE)
    # Always set cookie role=user when visiting the home page
    if request.cookies.get("role") != "user":
        resp.set_cookie("role", "user", path="/", httponly=False, samesite="Lax")
    return resp


@app.route("/admin")
def admin():
    role = request.cookies.get("role", "guest")
    if role == "admin":
        html = render_template_string(ADMIN_OK, flag=FLAG)
        return html
    else:
        html = render_template_string(ADMIN_DENIED, role=role)
        return html, 403


# ============================================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
