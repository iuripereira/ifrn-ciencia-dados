"""Sobe o site_resenhas/ em http://localhost:<porta livre>/ — Ctrl+C para parar."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PASTA = Path(__file__).parent / "site_resenhas"

handler = partial(SimpleHTTPRequestHandler, directory=PASTA)
with ThreadingHTTPServer(("localhost", 0), handler) as httpd:  # porta 0: o SO escolhe uma livre
    print(f"Servidor local em http://localhost:{httpd.server_port}/", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
