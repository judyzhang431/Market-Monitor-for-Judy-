from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import sqlite3
import subprocess
from urllib.parse import urlparse

from .drafts import generate_draft, folder_for_track


class Handler(BaseHTTPRequestHandler):
    db_path: Path
    industry_dir: Path
    us_academia_dir: Path
    cn_academia_dir: Path
    timezone: str

    def _conn(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _send(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if parts[:2] == ["api", "job"] and len(parts) == 3:
            job_id = parts[2]
            with self._conn() as conn:
                row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if not row:
                self._send(404, {"message": "Not found"})
                return
            self._send(200, {k: row[k] for k in row.keys()})
            return
        if parts[:2] == ["api", "open-posting"] and len(parts) == 3:
            job_id = parts[2]
            with self._conn() as conn:
                row = conn.execute("SELECT official_url FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if not row:
                self._send(404, {"message": "Not found"})
                return
            self._send(200, {"url": row["official_url"]})
            return
        if parts[:2] == ["api", "open-folder"] and len(parts) == 3:
            job_id = parts[2]
            with self._conn() as conn:
                row = conn.execute("SELECT track FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
            if not row:
                self._send(404, {"message": "Not found"})
                return
            folder = folder_for_track(row["track"], self.industry_dir, self.us_academia_dir, self.cn_academia_dir)
            try:
                subprocess.Popen(["open", str(folder)])
                self._send(200, {"message": f"Opened {folder}"})
            except Exception:
                self._send(200, {"message": f"Destination folder: {folder}"})
            return
        self._send(404, {"message": "unknown endpoint"})

    def do_POST(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if parts == ["api", "generate-draft"]:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw or b"{}")
            job_id = payload.get("job_id", "")
            with self._conn() as conn:
                try:
                    out, content = generate_draft(
                        conn,
                        job_id,
                        self.industry_dir,
                        self.us_academia_dir,
                        self.cn_academia_dir,
                        self.timezone,
                    )
                    self._send(200, {"message": "Draft generated", "path": str(out), "content": content})
                except Exception as exc:
                    self._send(400, {"message": str(exc)})
            return
        self._send(404, {"message": "unknown endpoint"})


def run_server(db_path: Path, industry_dir: Path, us_academia_dir: Path, cn_academia_dir: Path, timezone: str, host: str = "127.0.0.1", port: int = 8765):
    Handler.db_path = db_path
    Handler.industry_dir = industry_dir
    Handler.us_academia_dir = us_academia_dir
    Handler.cn_academia_dir = cn_academia_dir
    Handler.timezone = timezone
    server = ThreadingHTTPServer((host, port), Handler)
    server.serve_forever()
