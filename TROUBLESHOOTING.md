# Troubleshooting

## Error -102 (Connection Refused) when opening http://127.0.0.1:8000

This usually means your **browser** is trying to connect to port 8000 on **your own computer**, but the server is running somewhere else.

### If you're using Cursor (or VS Code) with a **remote** workspace

Your code and the server run on a **remote machine** (e.g. GitHub Codespaces, SSH host, Cursor remote). The server is listening on that machine’s port 8000. Your browser runs on your **local** machine, so `http://127.0.0.1:8000` only tries to reach your laptop—nothing is listening there, hence "Connection Refused".

**Fix: use port forwarding**

1. In Cursor/VS Code, open the **Ports** panel: **View → Ports** (or the "Ports" tab in the bottom panel).
2. If port **8000** is not in the list, click **"Forward a Port"** and enter **8000**.
3. Once 8000 appears, use **"Open in Browser"** (globe icon) next to it, or copy the **Local Address** (e.g. `http://localhost:8000`) and open it in your browser.

That way your browser talks to the forwarded port, which Cursor tunnels to the remote server.

### If you're running everything locally

1. Start the server from the project folder:
   ```bash
   cd call-directory
   ./run-admin.sh
   ```
   Or: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. Open **http://127.0.0.1:8000/** or **http://127.0.0.1:8000/admin/** in your browser.
3. If it still fails, check that nothing else is using port 8000 and that your firewall allows it.
