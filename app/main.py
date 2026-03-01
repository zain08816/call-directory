"""FastAPI app: webhooks for Twilio voice and SMS."""
from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.voice import router as voice_router
from app.sms import router as sms_router
from app.api import router as api_router

app = FastAPI(title="Call/SMS Directory", version="0.1.0")

VITE_ORIGIN = "http://127.0.0.1:5173"


BASE_DIR = Path(__file__).resolve().parent.parent
LEGAL_DIR = BASE_DIR / "legal"


@app.get("/")
def root():
    """Redirect to the admin dashboard."""
    return RedirectResponse(url="/admin/", status_code=302)


@app.get("/privacy")
def privacy():
    """Privacy policy (for A2P 10DLC and compliance)."""
    path = LEGAL_DIR / "privacy.html"
    if not path.is_file():
        return Response(content="Privacy policy not found.", status_code=404)
    return FileResponse(path, media_type="text/html")


@app.get("/terms")
def terms():
    """Terms and conditions."""
    path = LEGAL_DIR / "terms.html"
    if not path.is_file():
        return Response(content="Terms not found.", status_code=404)
    return FileResponse(path, media_type="text/html")


admin_dir = BASE_DIR / "admin"
admin_dist = admin_dir / "dist"

if settings.admin_dev_proxy:
    # Proxy /admin to Vite dev server so one address (8000) serves both API and frontend
    @app.api_route("/admin", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
    @app.api_route("/admin/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
    async def proxy_admin(request: Request, path: str = ""):
        url = httpx.URL(f"{VITE_ORIGIN}/admin/{path}")
        if request.url.query:
            url = url.copy_merge_params(request.query_params)
        headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "connection")}
        try:
            async with httpx.AsyncClient() as client:
                r = await client.request(
                    request.method,
                    url,
                    headers=headers,
                    content=await request.body(),
                    timeout=30.0,
                )
        except httpx.ConnectError:
            return Response(
                "Vite dev server not running. Start it with: cd admin && npm run dev",
                status_code=502,
            )
        return Response(
            content=r.content,
            status_code=r.status_code,
            headers={k: v for k, v in r.headers.items() if k.lower() not in ("transfer-encoding", "connection")},
        )
else:
    if admin_dist.is_dir():
        app.mount("/admin", StaticFiles(directory=str(admin_dist), html=True), name="admin")
    elif admin_dir.is_dir():
        app.mount("/admin", StaticFiles(directory=str(admin_dir), html=True), name="admin")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voice_router, prefix="/webhooks", tags=["voice"])
app.include_router(sms_router, prefix="/webhooks", tags=["sms"])
app.include_router(api_router)
