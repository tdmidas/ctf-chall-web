#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================================
  web_server.py  --  CTF Web Challenge: Cookie Manipulation (deploy build)
  Theme: ticketbox (nen trang) - dat ve cac tran FIFA World Cup 2026.
============================================================================
Server gan cookie `role=user`. Ve thuong ai cung dat duoc (ticket khong co
flag). Nut "Dat ve" cua ve VIP bi xam, chi bam duoc khi cookie role=admin;
khi do flag moi duoc nhung vao trang -> ticket VIP hien flag.
============================================================================
"""
import os
from flask import Flask, request, make_response, render_template_string, send_from_directory

app = Flask(__name__)
HERE = os.path.dirname(os.path.abspath(__file__))
FLAG = os.environ.get("CTF_FLAG", "UIT{c00k1e_n0t_s4f3}")

PAGE = """<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ticketbox — FIFA World Cup 2026</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#f4f6f8;color:#1a1a1a}
  .hd{background:#2ebd6b}
  .hd .in{max-width:1140px;margin:0 auto;padding:13px 18px;display:flex;align-items:center;gap:16px}
  .logo{font-size:1.55rem;font-weight:900;color:#fff;letter-spacing:-.5px}
  .rolechip{margin-left:auto;font-family:'Consolas',monospace;background:#fff;color:#1f7a4d;border-radius:6px;
            padding:3px 10px;font-weight:700;font-size:.9rem}
  .section{max-width:1140px;margin:0 auto;padding:26px 18px 50px}
  .h1{font-size:1.5rem;color:#111}
  .sub{color:#667;margin-top:6px;font-size:.95rem}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:20px;margin-top:22px}
  .card{background:#fff;border:1px solid #e3e6ea;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;
        box-shadow:0 4px 14px rgba(0,0,0,.05)}
  .poster{height:120px;display:flex;align-items:center;justify-content:center;text-align:center;padding:14px;
          font-weight:900;color:#fff;font-size:1.02rem;line-height:1.3;letter-spacing:.3px}
  .poster small{display:block;font-weight:700;font-size:.72rem;opacity:.9;margin-top:6px;letter-spacing:1px}
  .body{padding:13px 15px;display:flex;flex-direction:column;flex:1}
  .ttl{color:#111;font-weight:700;font-size:.97rem;min-height:2.6em}
  .price{color:#1f9d57;font-weight:800;margin-top:8px}
  .date{color:#8a8a8a;font-size:.85rem;margin-top:5px}
  .buy{margin-top:12px;border:none;border-radius:9px;padding:10px;font-weight:800;cursor:pointer;
       background:#2ebd6b;color:#fff;font-size:.92rem;font-family:inherit}
  .buy:hover{background:#28a862}
  .buy.off{background:#e3e6ea;color:#9aa;cursor:not-allowed}
  .lockmsg{margin-top:8px;font-size:.78rem;color:#b8860b;text-align:center}
  .ov{display:none;position:fixed;inset:0;background:rgba(0,0,0,.55);align-items:center;justify-content:center;padding:18px;z-index:9}
  .ovbox{position:relative;width:100%;max-width:700px}
  .ovclose{position:absolute;top:-14px;right:-6px;background:#fff;color:#111;border:none;border-radius:50%;
           width:34px;height:34px;font-size:1.1rem;cursor:pointer;font-weight:800;box-shadow:0 3px 10px rgba(0,0,0,.4)}
  .ticket{display:flex;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.4);color:#141414}
  .t-stripes{width:12px;flex:0 0 12px;background:repeating-linear-gradient(180deg,#e4002b 0 13px,#1346a0 13px 26px,#2ebd6b 26px 39px)}
  .t-main{flex:1;padding:24px 28px;min-width:0}
  .t-top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
  .t-logo{font-size:1.3rem;font-weight:900;color:#111;line-height:1.15;word-break:break-word}
  .t-city{color:#888;letter-spacing:3px;font-size:.72rem;margin-top:3px}
  .t-tag{font-size:.62rem;letter-spacing:2px;color:#fff;background:#2ebd6b;padding:4px 9px;border-radius:6px;font-weight:800;white-space:nowrap}
  .t-row{font-size:.9rem;color:#333;margin:10px 0 0}
  .t-row b{display:inline-block;min-width:74px;color:#999;letter-spacing:1px;font-size:.66rem;font-weight:700}
  .t-code{margin-top:16px;padding:14px;border:2px dashed #2ebd6b;border-radius:12px;background:#f2fbf5;text-align:center}
  .t-code .lbl{color:#1f7a4d;font-size:.72rem;letter-spacing:2px;margin-bottom:6px;font-weight:700}
  .t-flag{font-family:'Consolas','Courier New',monospace;font-size:1.2rem;font-weight:800;color:#111;word-break:break-all}
  .t-stub{width:150px;flex:0 0 150px;background:#2ebd6b;color:#fff;display:flex;flex-direction:column;align-items:center;
          justify-content:center;gap:8px;text-align:center;padding:14px;border-left:2px dashed #cfcfcf}
  .t-badge{background:#fff;border-radius:12px;padding:7px;line-height:0;box-shadow:0 2px 6px rgba(0,0,0,.2)}
  .t-badge img{width:70px;height:70px;object-fit:contain;display:block}
  .t-stub .num{font-size:2.3rem;font-weight:900}
  .t-stub .admit{font-size:.7rem;letter-spacing:3px;font-weight:800}
</style></head><body>

<div class="hd"><div class="in">
  <div class="logo">ticket box</div>
  <div class="rolechip">role={{ role }}</div>
</div></div>

<div class="section">
  <h1 class="h1">🏆 FIFA World Cup 2026 — Đặt vé các trận đấu</h1>
  <p class="sub">Chọn trận và đặt vé. Riêng vé VIP trận chung kết chỉ dành cho tài khoản admin.</p>

  <div class="grid">
    <div class="card">
      <div class="poster" style="background:linear-gradient(135deg,#1346a0,#b91c1c)">FRANCE vs ENGLAND<small>BẢNG A · VÒNG BẢNG</small></div>
      <div class="body"><div class="ttl">France vs England — Vòng bảng</div><div class="price">Từ 1.500.000đ</div>
        <div class="date">📅 12 tháng 06, 2026</div>
        <button class="buy" onclick="book('France vs England','12/06/2026')">Đặt vé</button></div>
    </div>
    <div class="card">
      <div class="poster" style="background:linear-gradient(135deg,#1f9d57,#0b6e3a)">BRAZIL vs ARGENTINA<small>BẢNG C · VÒNG BẢNG</small></div>
      <div class="body"><div class="ttl">Brazil vs Argentina — Vòng bảng</div><div class="price">Từ 1.800.000đ</div>
        <div class="date">📅 13 tháng 06, 2026</div>
        <button class="buy" onclick="book('Brazil vs Argentina','13/06/2026')">Đặt vé</button></div>
    </div>

    <div class="card">
      <div class="poster" style="background:linear-gradient(135deg,#b8860b,#3b2f00)">🏆 CHUNG KẾT<small>VÉ VIP · FINAL</small></div>
      <div class="body"><div class="ttl">Vé VIP Chung kết FIFA World Cup 2026</div><div class="price">Từ 9.999.000đ</div>
        <div class="date">📅 19 tháng 07, 2026</div>
        <button class="buy {{ 'off' if not is_admin else '' }}" {{ 'disabled' if not is_admin else '' }} onclick="bookVip()">Đặt vé{{ ' 🔒' if not is_admin else '' }}</button>
        {% if not is_admin %}<div class="lockmsg">Chỉ tài khoản admin mới đặt được vé này</div>{% endif %}
      </div>
    </div>
  </div>
</div>

<div class="ov" id="ov" onclick="closeT(event)">
  <div class="ovbox">
    <button class="ovclose" id="ovclose" onclick="closeT(event)">✕</button>
    <div id="ovbody"></div>
  </div>
</div>

<script>
const VIP_FLAG = {{ (flag if is_admin else "") | tojson }};

function ticketHTML(title, date, codeLbl, code, holder){
  // Chi hien o "ma ve" khi co code (ve VIP co flag). Ve thuong -> an di cho khoi nham la flag.
  const codeBox = code ? `<div class="t-code"><div class="lbl">${codeLbl}</div><div class="t-flag">${code}</div></div>` : '';
  return `<div class="ticket">
    <div class="t-stripes"></div>
    <div class="t-main">
      <div class="t-top">
        <div><div class="t-logo">${title}</div><div class="t-city">FIFA WORLD CUP 2026 · E-TICKET</div></div>
        <div class="t-tag">ADMIT ONE</div>
      </div>
      <div class="t-row"><b>NGÀY</b> ${date}</div>
      <div class="t-row"><b>NGƯỜI</b> ${holder}</div>
      <div class="t-row"><b>GHẾ</b> A12 · ROW 26</div>
      ${codeBox}
    </div>
    <div class="t-stub">
      <div class="t-badge"><img src="/logo-fifa.png" alt="logo"></div>
      <div class="num">26</div><div class="admit">ADMIT ONE</div>
    </div>
  </div>`;
}

function show(html){ document.getElementById('ovbody').innerHTML = html; document.getElementById('ov').style.display='flex'; }
function closeT(e){ if(!e || e.target.id==='ov' || e.target.id==='ovclose'){ document.getElementById('ov').style.display='none'; } }

function book(title, date){ show(ticketHTML(title, date, '', '', 'Khách')); }   // ve thuong: khong co ma ve

function bookVip(){
  if(!VIP_FLAG){ show(ticketHTML('Chung kết World Cup 2026', '19/07/2026', '', '', 'Khách')); return; }
  show(ticketHTML('CHUNG KẾT FIFA WORLD CUP 2026', '19/07/2026', '★ MÃ VÉ VIP (FLAG) ★', VIP_FLAG, 'ADMIN (VIP)'));
}
</script>
</body></html>"""


@app.route("/")
def home():
    role = request.cookies.get("role", "")
    is_admin = (role == "admin")
    resp = make_response(render_template_string(
        PAGE, role=(role or "user"), is_admin=is_admin, flag=FLAG))
    # Chi gan role=user khi chua co cookie -> de hoc sinh tu doi sang admin van giu duoc.
    if not role:
        resp.set_cookie("role", "user", path="/", httponly=False, samesite="Lax")
    return resp


@app.route("/logo-fifa.png")
def logo_fifa():
    return send_from_directory(HERE, "logo-fifa.png")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
