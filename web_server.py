#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
  web_server.py  --  CTF Web Challenge: Cookie Manipulation (deploy build)
  Theme: FIFA World Cup 2026 - "ve VIP chung ket chi danh cho admin"
============================================================================
Server gan cookie `role=user`. Trang /admin chi phat "ve VIP" (co FLAG) cho
role = "admin". Bai hoc: cookie nam o phia client - sua duoc tuy y -> dung tin.
============================================================================
"""
import os
from flask import Flask, request, make_response, render_template_string, send_from_directory

app = Flask(__name__)
HERE = os.path.dirname(os.path.abspath(__file__))
FLAG = os.environ.get("CTF_FLAG", "UIT{c00k1e_n0t_s4f3}")

STYLE = """
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#ffffff;color:#1a1a1a;
       min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;
       padding:32px;line-height:1.65}
  .banner{text-align:center;margin-bottom:22px;max-width:640px}
  .banner h1{font-size:1.45rem;color:#111}
  .banner p{color:#666;margin-top:8px;font-size:.95rem}
  .card{background:#fff;border:1px solid #e3e3e3;border-radius:14px;padding:22px 24px;max-width:560px;
        width:100%;text-align:center;box-shadow:0 6px 20px rgba(0,0,0,.05)}
  .card .role{display:inline-block;padding:2px 10px;border-radius:999px;background:#eef6f0;
        border:1px solid #bfe3cc;color:#0a7d3c;font-weight:700}
  .btn{display:inline-block;margin-top:18px;padding:11px 22px;border-radius:10px;background:#0a7d3c;
       color:#fff;font-weight:800;text-decoration:none;letter-spacing:.3px}
  .btn:hover{background:#0c8f45}
  .deny{color:#c62828;font-weight:700}
  .ok-title{color:#0a7d3c;font-weight:800;margin-bottom:18px;text-align:center;font-size:1.15rem}
  /* ===== TAM VE WORLD CUP (nen trang) ===== */
  .ticket{display:flex;width:700px;max-width:100%;background:#fff;border:1px solid #e3e3e3;
          border-radius:16px;overflow:hidden;box-shadow:0 16px 44px rgba(0,0,0,.14)}
  .t-stripes{width:12px;flex:0 0 12px;
             background:repeating-linear-gradient(180deg,#e4002b 0 13px,#1346a0 13px 26px,#0a7d3c 26px 39px)}
  .t-main{flex:1;padding:24px 28px;color:#141414}
  .t-top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
  .t-logo{font-size:1.65rem;font-weight:900;color:#111;line-height:1.1}
  .t-logo .yr{color:#0a7d3c}
  .t-city{color:#888;letter-spacing:4px;font-size:.72rem;margin-top:3px}
  .t-tag{font-size:.65rem;letter-spacing:2px;color:#fff;background:#0a7d3c;padding:4px 9px;
         border-radius:6px;font-weight:800;white-space:nowrap}
  .t-match{margin:16px 0;padding:12px 0;border-top:1px solid #eee;border-bottom:1px solid #eee;
           font-size:1.18rem;font-weight:800;letter-spacing:3px;color:#111}
  .t-match em{color:#0a7d3c;font-style:normal;font-weight:600;letter-spacing:1px}
  .t-row{font-size:.9rem;color:#333;margin:7px 0}
  .t-row b{display:inline-block;min-width:80px;color:#999;letter-spacing:1px;font-size:.68rem;font-weight:700}
  .t-code{margin-top:16px;padding:14px;border:2px dashed #0a7d3c;border-radius:12px;
          background:#f2fbf5;text-align:center}
  .t-code .lbl{color:#0a7d3c;font-size:.72rem;letter-spacing:2px;margin-bottom:6px;font-weight:700}
  .t-flag{font-family:'Consolas','Courier New',monospace;font-size:1.3rem;font-weight:800;
          color:#111;word-break:break-all}
  .t-stub{width:152px;flex:0 0 152px;background:#0a7d3c;color:#fff;display:flex;flex-direction:column;
          align-items:center;justify-content:center;gap:8px;text-align:center;padding:14px;
          border-left:2px dashed #cfcfcf}
  .t-stub .t-badge{background:#fff;border-radius:12px;padding:7px;line-height:0;box-shadow:0 2px 6px rgba(0,0,0,.2)}
  .t-stub .t-badge img{width:78px;height:78px;object-fit:contain;display:block}
  .t-stub .num{font-size:2.5rem;font-weight:900;color:#fff;line-height:1}
  .t-stub .admit{font-size:.72rem;letter-spacing:3px;font-weight:800}
  .foot{margin-top:18px;color:#666;font-size:.82rem;text-align:center}
</style>
"""

HOME_PAGE = """<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FIFA World Cup 2026 - Vé VIP</title>""" + STYLE + """</head><body>
  <div class="banner">
    <h1>🏆 FIFA WORLD CUP 2026 — Cổng vé VIP</h1>
    <p>Chủ tịch FIFA chỉ trao <b>vé VIP dự trận chung kết</b> cho những tài khoản
       được cấp quyền <b>admin</b>.</p>
  </div>
  <div class="card">
    Bạn đang vào cổng với quyền: <span class="role">{{ role }}</span><br>
    Rất tiếc, "user" thường thì chưa được nhận vé. Thử vào khu vực phát vé xem sao 👀
    <br><a class="btn" href="/admin">→ Vào khu vực vé VIP (/admin)</a>
  </div>
</body></html>"""

ADMIN_DENIED = """<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vé VIP - Từ chối</title>""" + STYLE + """</head><body>
  <div class="banner">
    <h1>⛔ Khu vực vé VIP — chỉ dành cho admin</h1>
  </div>
  <div class="card">
    Quyền hiện tại của bạn: <span class="role">{{ role }}</span><br>
    <span class="deny">Bạn không phải admin</span> nên bảo vệ không cho vào nhận vé chung kết.<br>
    <span style="color:#888;font-size:.9rem">Gợi ý: bảo vệ chỉ nhìn vào tấm "thẻ role" mà bạn cầm theo...</span>
    <br><a class="btn" href="/">← Quay lại cổng</a>
  </div>
</body></html>"""

ADMIN_OK = """<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vé VIP Chung kết World Cup</title>""" + STYLE + """</head><body>
  <div class="ok-title">✅ Chào mừng Admin! Đây là vé VIP chung kết của bạn 🎟️</div>
  <div class="ticket">
    <div class="t-stripes"></div>
    <div class="t-main">
      <div class="t-top">
        <div>
          <div class="t-logo">FIFA WORLD CUP <span class="yr">2026</span></div>
          <div class="t-city">NEW YORK</div>
        </div>
        <div class="t-tag">MATCH TICKET</div>
      </div>
      <div class="t-match">FRANCE <em>vs</em> ENGLAND</div>
      <div class="t-row"><b>DATE</b> JUNE 12, 2026 — CHUNG KẾT</div>
      <div class="t-row"><b>HOLDER</b> ADMIN (VIP)</div>
      <div class="t-row"><b>GATE / SEAT</b> A1 · ROW 26</div>
      <div class="t-code">
        <div class="lbl">★ MÃ VÉ VIP (FLAG) ★</div>
        <div class="t-flag">{{ flag }}</div>
      </div>
    </div>
    <div class="t-stub">
      <div class="t-badge"><img src="/logo-fifa.png" alt="FIFA"></div>
      <div class="num">26</div>
      <div class="admit">ADMIT ONE</div>
    </div>
  </div>
  <div class="foot">Nộp mã vé ở trên (dạng UIT{...}) lên trang nộp flag để ghi điểm.</div>
</body></html>"""


@app.route("/")
def home():
    # Always (re)issue a clean plaintext role=user cookie.
    resp = make_response(render_template_string(HOME_PAGE, role="user"))
    resp.set_cookie("role", "user", path="/", httponly=False, samesite="Lax")
    return resp


@app.route("/admin")
def admin():
    role = request.cookies.get("role", "")
    if role == "admin":
        return render_template_string(ADMIN_OK, flag=FLAG)
    return render_template_string(ADMIN_DENIED, role=role or "guest"), 403


@app.route("/logo-fifa.png")
def logo_fifa():
    return send_from_directory(HERE, "logo-fifa.png")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
