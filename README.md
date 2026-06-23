# CTF Web Challenge - Cookie Manipulation

A simple Flask web app for a CTF seminar challenge. The server sets a `role` cookie whose value is **base64-encoded** (`dXNlcg==` = `"user"`). Students must send a `role` cookie that base64-decodes to `admin` (i.e. `YWRtaW4=`) to access the flag. Lesson: base64 is encoding, not security.

## Deploy on Render

1. Push this repo to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com) → **New Web Service**
3. Connect this repo
4. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_server:app --bind 0.0.0.0:$PORT`
5. (Optional) Set environment variable `CTF_FLAG` to customize the flag value
6. Deploy!

## Run Locally

```bash
pip install flask
python web_server.py
# Open http://localhost:5000
```
