#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify a GLM vision.js dual-model 429 fallback WITHOUT hitting the real API.

Points VISION_BASE_URL at a local mock HTTP server that returns 429 for the
primary model and 200 for the fallback, then asserts the tool retried and
succeeded. Deterministic, free, repeatable.

Usage:
    python verify_vision_fallback.py <path-to-vision.js>

Adjust PRIMARY-429 / FALLBACK-OK model names and the expected stdout string to
match the tool under test. Exit 0 = all pass.
"""
import http.server, json, threading, subprocess, sys, socketserver, tempfile, os, struct, zlib

VISION_JS = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\hfhfn\.skills-manager\skills\claude-vision-skill\vision.js"

class MockHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = json.loads(self.rfile.read(length))
        model = body["model"]
        self.server.log("request model=%s" % model)
        if model == "PRIMARY-429":
            self.send_response(429)
            payload = {"error": {"code": "1305", "message": "该模型当前访问量过大，请您稍后再试"}}
        elif model == "FALLBACK-OK":
            self.send_response(200)
            payload = {"choices": [{"message": {"content": "回退模型识别成功"}}]}
        else:
            self.send_response(400)
            payload = {"error": {"message": "unknown model"}}
        data = json.dumps(payload).encode()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def log_message(self, *a):
        pass

class Server(socketserver.TCPServer):
    allow_reuse_address = True
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.requests = []
    def log(self, msg):
        self.requests.append(msg)

def make_image(tmp):
    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    idat = zlib.compress(b"\x00\xff\x7f\x00")
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")
    p = os.path.join(tmp, "px.png")
    with open(p, "wb") as f:
        f.write(png)
    return p

def run(srv, img, env_extra):
    env = dict(os.environ)
    env["VISION_BASE_URL"] = "http://127.0.0.1:%d" % srv.server_address[1]
    env["CUSTOM_GLM_API_KEY"] = "fake-key"
    env.update(env_extra)
    return subprocess.run(["node", VISION_JS, img, "测试"],
                          capture_output=True, text=True, env=env, timeout=60)

results = []
srv = None
try:
    tmp = tempfile.mkdtemp(prefix="hermes-verify-")
    img = make_image(tmp)
    srv = Server(("127.0.0.1", 0), MockHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    r = run(srv, img, {"VISION_MODEL_PRIMARY": "PRIMARY-429", "VISION_MODEL_FALLBACK": "FALLBACK-OK"})
    ok1 = r.returncode == 0 and "回退模型识别成功" in r.stdout
    models1 = [m.replace("request model=", "") for m in srv.requests]
    results.append(("primary-429 -> fallback switch", ok1, {"models_called": models1, "stdout": r.stdout.strip()}))

    srv.requests.clear()
    r2 = run(srv, img, {"VISION_MODEL_PRIMARY": "PRIMARY-429", "VISION_MODEL_FALLBACK": "BAD-400"})
    ok2 = r2.returncode != 0 and "API 400" in r2.stderr
    models2 = [m.replace("request model=", "") for m in srv.requests]
    results.append(("non-429 error no-retry", ok2, {"models_called": models2, "stderr": r2.stderr.strip()[:80]}))
finally:
    if srv:
        srv.shutdown()

print("=" * 60)
print("verify vision.js dual-model fallback")
print("=" * 60)
allok = True
for name, ok, detail in results:
    allok = allok and ok
    print("[%s] %s" % ("PASS" if ok else "FAIL", name))
    print("     %s" % detail)
print("=" * 60)
print("OVERALL: %s" % ("ALL PASS" if allok else "FAILURES PRESENT"))
sys.exit(0 if allok else 1)