# CTF Web Challenge - Cookie Manipulation

A simple Flask web app for a CTF seminar challenge. The server sets a plaintext `role=user` cookie. Students must change the `role` cookie to `admin` to access the flag. Lesson: cookies live on the client and can be edited freely — never trust them.

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
