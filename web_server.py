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
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)
FLAG = os.environ.get("CTF_FLAG", "UIT{c00k1e_n0t_s4f3}")

STYLE = """
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;
       background:radial-gradient(1200px 600px at 50% -10%,#15301f 0%,#0a0e0a 60%);
       color:#e8efe8;min-height:100vh;display:flex;flex-direction:column;
       align-items:center;justify-content:center;padding:28px;line-height:1.6}
  .banner{text-align:center;margin-bottom:24px;max-width:640px}
  .banner h1{font-size:1.5rem;color:#d4af37;letter-spacing:.5px}
  .banner p{color:#9fb0a2;margin-top:8px;font-size:.95rem}
  .card{background:#0f160f;border:1px solid #283a28;border-radius:14px;
        padding:22px 24px;max-width:560px;width:100%;text-align:center}
  .card .role{display:inline-block;padding:2px 10px;border-radius:999px;
        background:#1c2a1c;border:1px solid #3a523a;color:#d4af37;font-weight:700}
  .btn{display:inline-block;margin-top:18px;padding:11px 22px;border-radius:10px;
       background:#d4af37;color:#0a0e0a;font-weight:800;text-decoration:none;letter-spacing:.3px}
  .btn:hover{background:#e7c84a}
  .deny{color:#ff8b8b;font-weight:700}
  /* ===== TAM VE WORLD CUP ===== */
  .ok-title{color:#7CFC9A;font-weight:800;margin-bottom:18px;text-align:center;font-size:1.15rem}
  .ticket{display:flex;width:700px;max-width:100%;border-radius:18px;overflow:hidden;
          box-shadow:0 24px 60px rgba(0,0,0,.6);border:1px solid #2a3a2a}
  .t-main{flex:1;padding:26px 30px;background:linear-gradient(135deg,#11180f,#0a0e0a)}
  .t-top{display:flex;justify-content:space-between;align-items:flex-start}
  .t-logo{font-size:1.7rem;font-weight:900;color:#fff;letter-spacing:.5px;line-height:1.1}
  .t-logo .yr{color:#d4af37}
  .t-city{color:#9fb0a2;letter-spacing:4px;font-size:.72rem;margin-top:4px}
  .t-tag{font-size:.65rem;letter-spacing:2px;color:#0a0e0a;background:#d4af37;
         padding:4px 9px;border-radius:6px;font-weight:800;white-space:nowrap}
  .t-match{margin:18px 0;padding:13px 0;border-top:1px solid #283a28;border-bottom:1px solid #283a28;
           font-size:1.2rem;font-weight:800;letter-spacing:3px;color:#fff}
  .t-match em{color:#d4af37;font-style:normal;font-weight:500;letter-spacing:1px}
  .t-row{font-size:.9rem;color:#cfe0d2;margin:7px 0}
  .t-row b{display:inline-block;min-width:78px;color:#7a8a7a;letter-spacing:1px;
           font-size:.68rem;font-weight:700}
  .t-code{margin-top:18px;padding:15px;border:2px dashed #d4af37;border-radius:12px;
          background:rgba(212,175,55,.07);text-align:center}
  .t-code .lbl{color:#d4af37;font-size:.72rem;letter-spacing:2px;margin-bottom:7px}
  .t-flag{font-family:'Consolas','Courier New',monospace;font-size:1.3rem;font-weight:800;
          color:#fff;word-break:break-all}
  .t-stub{width:158px;background:linear-gradient(160deg,#1c5a3a,#0c3a24);color:#fff;
          display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;
          border-left:3px dashed #0a0e0a;text-align:center;padding:14px}
  .t-stub .trophy{font-size:3.1rem;filter:drop-shadow(0 4px 8px rgba(0,0,0,.5))}
  .t-stub .num{font-size:2.6rem;font-weight:900;color:#d4af37;line-height:1}
  .t-stub .admit{font-size:.72rem;letter-spacing:3px;font-weight:800}
  .foot{margin-top:18px;color:#9fb0a2;font-size:.82rem;text-align:center}
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
    <span style="color:#9fb0a2;font-size:.9rem">Gợi ý: bảo vệ chỉ nhìn vào tấm "thẻ role" mà bạn cầm theo...</span>
    <br><a class="btn" href="/">← Quay lại cổng</a>
  </div>
</body></html>"""

ADMIN_OK = """<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vé VIP Chung kết World Cup</title>""" + STYLE + """</head><body>
  <div class="ok-title">✅ Chào mừng Admin! Đây là vé VIP chung kết của bạn 🎟️</div>
  <div class="ticket">
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
      <div class="trophy">🏆</div>
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
