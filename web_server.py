#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
  web_server.py  --  CTF Web Challenge: Cookie Manipulation (deploy build)
  Theme: World Cup Ticket Box - phan quyen bang cookie `role`
============================================================================
Server gan cookie `role=user`. Trang dat ve VIP (/admin) chi mo cho role =
"admin". Bai hoc: web tin cookie phia client -> sua cookie role=admin la vuot quyen.
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
  body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#f4f6f8;color:#1a1a1a;
       min-height:100vh;line-height:1.6}
  .wrap{max-width:960px;margin:0 auto;padding:0 18px 40px}
  /* navbar */
  .nav{background:#0a7d3c;color:#fff;padding:12px 0;margin-bottom:0}
  .nav .in{max-width:960px;margin:0 auto;padding:0 18px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
  .brand{font-size:1.15rem;font-weight:800;letter-spacing:.3px}
  .acct{font-size:.9rem;display:flex;align-items:center;gap:8px}
  .rolechip{font-family:'Consolas',monospace;background:#fff;color:#0a7d3c;border:1px dashed #0a7d3c;
            border-radius:6px;padding:2px 8px;font-weight:700}
  /* hero */
  .hero{background:linear-gradient(135deg,#0a7d3c,#0c8f45);color:#fff;border-radius:0 0 16px 16px;
        padding:30px 24px;text-align:center;margin-bottom:24px}
  .hero .tag{font-size:.72rem;letter-spacing:3px;opacity:.9}
  .hero h1{font-size:1.5rem;margin:8px 0 6px}
  .hero p{opacity:.92;font-size:.95rem}
  /* ticket grid */
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:6px}
  .tk{background:#fff;border:1px solid #e3e6ea;border-radius:14px;padding:18px;position:relative;
      box-shadow:0 4px 14px rgba(0,0,0,.05);display:flex;flex-direction:column;gap:6px}
  .tk .stage{font-size:.7rem;letter-spacing:2px;color:#0a7d3c;font-weight:800}
  .tk .match{font-weight:700;font-size:1.05rem}
  .tk .price{font-size:1.4rem;font-weight:900;color:#111;margin-top:4px}
  .buy{margin-top:10px;border:none;border-radius:9px;padding:10px;font-weight:800;cursor:pointer;
       background:#0a7d3c;color:#fff;text-align:center;text-decoration:none;font-size:.95rem}
  .buy:hover{background:#0c8f45}
  .buy.alt{background:#d4af37;color:#1a1a1a}
  .buy.alt:hover{background:#e7c84a}
  .tk.locked{border:2px solid #d4af37;background:#fffdf4}
  .tk .lock{position:absolute;top:-11px;left:14px;background:#d4af37;color:#1a1a1a;font-size:.66rem;
            font-weight:800;letter-spacing:1px;padding:3px 9px;border-radius:999px}
  .note{margin-top:22px;background:#fff;border:1px solid #e3e6ea;border-left:4px solid #0a7d3c;
        border-radius:10px;padding:14px 16px;font-size:.93rem}
  .note code{background:#eef6f0;border:1px solid #cfe6d6;border-radius:5px;padding:1px 6px;font-family:'Consolas',monospace}
  /* deny */
  .denybox{background:#fff;border:1px solid #e3e6ea;border-radius:14px;padding:26px;margin-top:24px;text-align:center;
           box-shadow:0 6px 20px rgba(0,0,0,.05)}
  .denybox h1{font-size:1.3rem;color:#c62828}
  .hint{margin-top:14px;background:#fff8e6;border:1px solid #f0dba0;border-radius:10px;padding:12px 14px;
        font-size:.9rem;text-align:left}
  .hint code{background:#fff;border:1px solid #e6d28f;border-radius:5px;padding:1px 6px;font-family:'Consolas',monospace}
  /* ===== TAM VE VIP (trang admin) ===== */
  .ok-title{color:#0a7d3c;font-weight:800;margin:24px 0 16px;text-align:center;font-size:1.15rem}
  .ticket{display:flex;max-width:700px;margin:0 auto;background:#fff;border:1px solid #e3e3e3;
          border-radius:16px;overflow:hidden;box-shadow:0 16px 44px rgba(0,0,0,.14)}
  .t-stripes{width:12px;flex:0 0 12px;
             background:repeating-linear-gradient(180deg,#e4002b 0 13px,#1346a0 13px 26px,#0a7d3c 26px 39px)}
  .t-main{flex:1;padding:24px 28px}
  .t-top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
  .t-logo{font-size:1.65rem;font-weight:900;color:#111;line-height:1.1}
  .t-logo .yr{color:#0a7d3c}
  .t-city{color:#888;letter-spacing:4px;font-size:.72rem;margin-top:3px}
  .t-tag{font-size:.65rem;letter-spacing:2px;color:#fff;background:#0a7d3c;padding:4px 9px;border-radius:6px;font-weight:800;white-space:nowrap}
  .t-match{margin:16px 0;padding:12px 0;border-top:1px solid #eee;border-bottom:1px solid #eee;
           font-size:1.18rem;font-weight:800;letter-spacing:3px;color:#111}
  .t-match em{color:#0a7d3c;font-style:normal;font-weight:600;letter-spacing:1px}
  .t-row{font-size:.9rem;color:#333;margin:7px 0}
  .t-row b{display:inline-block;min-width:80px;color:#999;letter-spacing:1px;font-size:.68rem;font-weight:700}
  .t-code{margin-top:16px;padding:14px;border:2px dashed #0a7d3c;border-radius:12px;background:#f2fbf5;text-align:center}
  .t-code .lbl{color:#0a7d3c;font-size:.72rem;letter-spacing:2px;margin-bottom:6px;font-weight:700}
  .t-flag{font-family:'Consolas','Courier New',monospace;font-size:1.3rem;font-weight:800;color:#111;word-break:break-all}
  .t-stub{width:152px;flex:0 0 152px;background:#0a7d3c;color:#fff;display:flex;flex-direction:column;
          align-items:center;justify-content:center;gap:8px;text-align:center;padding:14px;border-left:2px dashed #cfcfcf}
  .t-stub .t-badge{background:#fff;border-radius:12px;padding:7px;line-height:0;box-shadow:0 2px 6px rgba(0,0,0,.2)}
  .t-stub .t-badge img{width:78px;height:78px;object-fit:contain;display:block}
  .t-stub .num{font-size:2.5rem;font-weight:900;color:#fff;line-height:1}
  .t-stub .admit{font-size:.72rem;letter-spacing:3px;font-weight:800}
  .foot{margin-top:16px;color:#666;font-size:.82rem;text-align:center}
  .back{display:inline-block;margin-top:16px;color:#0a7d3c;font-weight:700;text-decoration:none}
</style>
"""

NAV = """
<div class="nav"><div class="in">
  <div class="brand">🎟️ WorldCup <span style="font-weight:900">Ticket Box</span></div>
  <div class="acct">👤 Khách · <span class="rolechip">role={{ role }}</span></div>
</div></div>"""

HOME_PAGE = """<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WorldCup Ticket Box — Đặt vé FIFA World Cup 2026</title>""" + STYLE + """</head><body>
""" + NAV + """
<div class="hero">
  <div class="tag">FIFA WORLD CUP 2026 · NEW YORK</div>
  <h1>Đặt vé các trận đấu World Cup 2026</h1>
  <p>Chọn trận và mua vé. Vé VIP trận chung kết chỉ mở cho tài khoản <b>admin</b>.</p>
</div>
<div class="wrap">
  <div class="grid">
    <div class="tk">
      <div class="stage">VÒNG BẢNG</div>
      <div class="match">France vs England</div>
      <div class="price">$50</div>
      <button class="buy" onclick="alert('Đặt vé thành công (demo).')">Đặt vé</button>
    </div>
    <div class="tk">
      <div class="stage">TỨ KẾT</div>
      <div class="match">Brazil vs Argentina</div>
      <div class="price">$120</div>
      <button class="buy" onclick="alert('Đặt vé thành công (demo).')">Đặt vé</button>
    </div>
    <div class="tk locked">
      <div class="lock">🔒 ADMIN ONLY</div>
      <div class="stage">VIP · CHUNG KẾT</div>
      <div class="match">Vé vàng VIP</div>
      <div class="price">VIP</div>
      <a class="buy alt" href="/admin">Vào khu vực vé VIP →</a>
    </div>
  </div>
  <div class="note">
    Hệ thống nhận diện quyền của bạn qua <b>cookie <code>role</code></b> — hiện tại đang là
    <span class="rolechip">{{ role }}</span>. Chỉ tài khoản có <code>role=admin</code> mới mở được
    khu vực vé VIP chung kết.
  </div>
</div>
</body></html>"""

ADMIN_DENIED = """<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vé VIP — Từ chối truy cập</title>""" + STYLE + """</head><body>
""" + NAV + """
<div class="wrap">
  <div class="denybox">
    <h1>⛔ Khu vực vé VIP — chỉ dành cho admin</h1>
    <p>Quyền hiện tại của bạn: <span class="rolechip">role={{ role }}</span> — không phải admin nên không thể nhận vé VIP.</p>
    <div class="hint">
      💡 Máy chủ <b>chỉ kiểm tra giá trị cookie <code>role</code></b> mà trình duyệt bạn gửi lên —
      mà cookie thì nằm ở phía bạn và sửa được tuỳ ý. Thử mở <b>F12 → Application → Cookies</b> xem
      cookie <code>role</code> đang là gì...
    </div>
    <a class="back" href="/">← Quay lại trang đặt vé</a>
  </div>
</div>
</body></html>"""

ADMIN_OK = """<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vé VIP Chung kết World Cup</title>""" + STYLE + """</head><body>
""" + NAV.replace("{{ role }}", "admin") + """
<div class="wrap">
  <div class="ok-title">✅ Truy cập admin thành công! Đây là vé VIP chung kết của bạn 🎟️</div>
  <div class="ticket">
    <div class="t-stripes"></div>
    <div class="t-main">
      <div class="t-top">
        <div>
          <div class="t-logo">FIFA WORLD CUP <span class="yr">2026</span></div>
          <div class="t-city">NEW YORK</div>
        </div>
        <div class="t-tag">VIP TICKET</div>
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
  <div style="text-align:center"><a class="back" href="/">← Về trang đặt vé</a></div>
</div>
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
