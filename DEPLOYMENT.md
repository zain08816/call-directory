# Pushing to Production

Your app must be reachable over **HTTPS** at a stable URL so Twilio can send webhooks. Below are the main steps and hosting options.

---

## 1. Build the admin dashboard

From the project root:

```bash
cd admin
npm install
npm run build
cd ..
```

The built files go to `admin/dist/`. The FastAPI app serves them at `/admin/`.

---

## 2. Set production environment variables

On the production server (or in your host’s env/config), set:

| Variable | Description |
|----------|-------------|
| `TWILIO_ACCOUNT_SID` | From [Twilio Console](https://console.twilio.com) |
| `TWILIO_AUTH_TOKEN` | From Twilio Console |
| `TWILIO_PHONE_NUMBER` | Your Twilio number (e.g. `+15551234567`) |
| `ALLOWED_PHONE_NUMBERS` | Comma-separated E.164 numbers that can use the service |
| `BASE_URL` | **Your production URL** (e.g. `https://yourdomain.com`) — required for “Place test call” and TwiML callbacks |

Optional:

- `CONTACTS_PATH` — path to `contacts.json` (default: `data/contacts.json`)

Ensure `data/contacts.json` (or your custom path) exists on the server and is readable by the app.

---

## 3. Point Twilio to production

In [Twilio Console](https://console.twilio.com) → Phone Numbers → your number:

- **Voice** → A CALL COMES IN → Webhook → `https://YOUR_PRODUCTION_DOMAIN/webhooks/voice` (POST)
- **SMS** → A MESSAGE COMES IN → Webhook → `https://YOUR_PRODUCTION_DOMAIN/webhooks/sms` (POST)

Use the same `BASE_URL` you set above (no trailing slash in Twilio).

---

## 4. Hosting options

### A. VPS (DigitalOcean, Linode, EC2, etc.)

1. **Server**: Create a VM (e.g. Ubuntu), open port 80/443.
2. **App**:
   - Install Python 3.10+, Node (for building; or build locally and upload `admin/dist`).
   - Clone/copy the project, create venv, `pip install -r requirements.txt`.
   - Build admin: `cd admin && npm ci && npm run build && cd ..`.
   - Run with a process manager (see below).
3. **HTTPS**: Put **Nginx** (or Caddy) in front, use **Let’s Encrypt** (e.g. `certbot`) for SSL.
4. **Process manager**: Use **systemd** so the app restarts on reboot.

Example systemd unit (`/etc/systemd/system/call-directory.service`):

```ini
[Unit]
Description=Call/SMS Directory
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/call-directory
Environment="PATH=/path/to/call-directory/.venv/bin"
ExecStart=/path/to/call-directory/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Nginx (or Caddy) proxies `https://yourdomain.com` → `http://127.0.0.1:8000`.

---

### B. Railway

1. Create a [Railway](https://railway.app) project and connect your repo (or upload the project).
2. Add a **Nixpacks** or **Dockerfile** service. Railway often detects Python; ensure the start command is:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
   (Railway sets `PORT`.)
3. Build the admin before starting the server, or build in CI and commit `admin/dist` so the server only runs uvicorn.
4. In Railway dashboard, set all env vars (`TWILIO_*`, `ALLOWED_PHONE_NUMBERS`, `BASE_URL` = your Railway URL, e.g. `https://your-app.up.railway.app`).
5. Deploy; use the generated HTTPS URL as `YOUR_PRODUCTION_DOMAIN` in Twilio and `BASE_URL`.

---

### C. Render

1. Create a [Render](https://render.com) **Web Service**, connect the repo.
2. **Build**: `pip install -r requirements.txt` and build admin, e.g.:
   - Build command: `pip install -r requirements.txt && cd admin && npm install && npm run build && cd ..`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Set env vars in Render dashboard; set `BASE_URL` to the Render URL (e.g. `https://your-app.onrender.com`).
4. Ensure `data/contacts.json` is present (commit it or mount a disk if Render supports it).

---

### D. Fly.io

1. Install [flyctl](https://fly.io/docs/hands-on/install-flyctl/) and log in.
2. In the project root, run `fly launch` (creates `fly.toml`). Choose a region.
3. Add a **Dockerfile** (or use Fly’s Python build) that:
   - Installs Python deps and builds the admin (Node in the image).
   - Runs `uvicorn app.main:app --host 0.0.0.0 --port 8080` (or the port Fly expects).
4. Set secrets: `fly secrets set TWILIO_ACCOUNT_SID=... TWILIO_AUTH_TOKEN=... TWILIO_PHONE_NUMBER=... ALLOWED_PHONE_NUMBERS=... BASE_URL=https://your-app.fly.dev`
5. Deploy with `fly deploy`. Use the app URL for Twilio webhooks and `BASE_URL`.

---

## 5. Checklist before going live

- [ ] Admin built: `admin/dist` exists and is served at `/admin/`.
- [ ] Production env set: `TWILIO_*`, `ALLOWED_PHONE_NUMBERS`, `BASE_URL`.
- [ ] `data/contacts.json` (or `CONTACTS_PATH`) present and correct on the server.
- [ ] Twilio Voice webhook → `https://YOUR_DOMAIN/webhooks/voice` (POST).
- [ ] Twilio SMS webhook → `https://YOUR_DOMAIN/webhooks/sms` (POST).
- [ ] HTTPS works and the app responds at `BASE_URL` (e.g. `https://yourdomain.com/admin/`, `https://yourdomain.com/privacy`, `https://yourdomain.com/terms`).

---

## 6. Docker

The repo includes a multi-stage **Dockerfile** that builds the admin and runs the FastAPI app.

**Build and run locally:**

```bash
docker compose up --build
```

**Production:** Build the image and run it on your host (VPS, Railway, Fly, etc.), passing env vars via `-e`, `--env-file`, or your platform’s config. Example:

```bash
docker build -t call-directory .
docker run -d -p 8000:8000 --env-file .env call-directory
```

Use a reverse proxy (e.g. Nginx + Let’s Encrypt) in front for HTTPS, or deploy the image to a platform that provides SSL.
