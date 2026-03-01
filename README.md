# Call/SMS Directory

Call or text a single Twilio number to reach a menu of predefined contacts: **voice** calls are bridged to the contact you choose; **SMS** is relayed bidirectionally between you and the chosen contact.

Only phone numbers in the allowlist can use the system.

## Setup

### 1. Twilio

- Create a [Twilio](https://www.twilio.com) account and buy a phone number (Voice + SMS).
- In Twilio Console → Phone Numbers → your number:
  - **Voice**: "A CALL COMES IN" → Webhook → `https://YOUR_DOMAIN/webhooks/voice` (HTTP POST).
  - **SMS**: "A MESSAGE COMES IN" → Webhook → `https://YOUR_DOMAIN/webhooks/sms` (HTTP POST).

### 2. Environment

Copy `.env.example` to `.env` and set:

- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`
- `ALLOWED_PHONE_NUMBERS`: comma-separated E.164 numbers (e.g. your phone) that can call/text the system

### 3. Contacts

Copy `data/contacts.json.example` to `data/contacts.json`, then edit with your predefined contacts:

```json
[
  { "id": 1, "name": "Mom", "phone": "+15551234567" },
  { "id": 2, "name": "Dad", "phone": "+15559876543" }
]
```

### 4. Run locally

```bash
cd call-directory
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run `./run-admin.sh` from the `call-directory` folder.

**If you use Cursor/VS Code with a remote workspace** and get "Connection Refused" (Error -102): open the **Ports** panel (View → Ports), forward port **8000**, then click **Open in Browser** for that port. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

Expose the app to the internet (required for Twilio webhooks):

```bash
ngrok http 8000
```

Use the `https://...` ngrok URL as `YOUR_DOMAIN` when configuring the Twilio webhooks above.

### 5. Run with Docker or Podman

Ensure `.env` is configured (see step 2). From the project root:

```bash
docker compose up --build
```

On Fedora/Bluefin, the default is Podman; you can use `podman compose up --build` instead. To use **Docker Engine** on Fedora, add Docker’s repo and install:

```bash
sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

Then log out and back in (or reboot) so the `docker` group takes effect. Run `docker compose up --build` from the project root.

The app is at http://localhost:8000 (admin at http://localhost:8000/admin/).

To expose the app via ngrok (for Twilio webhooks), add `NGROK_AUTHTOKEN` to `.env` (get it from [dashboard.ngrok.com](https://dashboard.ngrok.com/get-started/your-authtoken)). The ngrok service runs alongside the app and prints its public URL in the logs. View it with `docker compose logs ngrok` or `podman compose logs ngrok`, then set `BASE_URL` in `.env` to that URL for test calls.

For production deployment with Docker, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Usage

- **Voice**: Call your Twilio number → hear "Press 1 for Mom, 2 for Dad..." → press a digit → you are connected to that contact.
- **SMS**: Text your Twilio number → receive "Reply with a number: 1 Mom, 2 Dad..." → reply with a digit → you are "connected"; your messages are relayed to that contact and their replies are relayed to you. Reply **STOP** (or **0**) to disconnect and see the menu again.

## Admin dashboard

React + TypeScript dashboard (Vite) to view contacts, recent calls, recent SMS, and to trigger test calls or test SMS.

**Development** (frontend only, with API proxy to backend):

```bash
cd call-directory/admin
npm install
npm run dev
```

Open http://localhost:5173. The Vite dev server proxies `/api` and `/webhooks` to the backend (port 8000); run the backend separately if you need live API data.

**Production** (serve built dashboard from FastAPI):

```bash
cd call-directory/admin
npm install
npm run build
```

Then start the backend; it will serve the built app from `admin/dist` at [http://localhost:8000/admin/](http://localhost:8000/admin/). The root URL `/` redirects to `/admin/`.

- **Contacts** – Lists phone numbers in the directory (from `data/contacts.json`).
- **Recent calls** – Calls sent/received via Twilio (from Twilio API).
- **Recent SMS** – Messages sent and to where (from Twilio API).
- **Test call** – Enter a phone number and click "Place test call". Requires `BASE_URL` in `.env` (e.g. your ngrok URL).
- **Test SMS** – Enter a number and message body and click "Send test SMS".

API base URL in the dashboard defaults to the current page origin when left empty.

## Project layout

- `app/main.py` – FastAPI app, static mount for admin
- `app/voice.py` – `/webhooks/voice` → TwiML menu, Gather, Dial
- `app/sms.py` – `/webhooks/sms` → menu, connect, relay, disconnect
- `app/api.py` – `/api/*` – admin API: contacts, calls, messages, test call/SMS
- `app/contacts.py` – load contacts from JSON
- `app/sms_sessions.py` – in-memory user ↔ contact session store
- `app/twilio_client.py` – send SMS, list calls/messages, create call
- `app/config.py` – settings from env
- `data/contacts.json` – predefined contacts
- `admin/` – admin dashboard (React + TypeScript, Vite) built to `admin/dist`, served at `/admin`
