import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse
from uuid import uuid4

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.pay.order_manager import order_manager
from core.report import build_preview_report, pay_unlock
from core.structure import build_life_structure_model, classify_structure
from core.viral_content import generate_viral_content, generate_viral_content_batch


CONTENT_ADMIN_KEY = os.getenv("CONTENT_ADMIN_KEY", "life29")


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in {"/api/index.py", "/api", "/health"}:
            return self._json({"status": "ok", "service": "life-structure-ai"})

        if path in {"/content-generator", "/content_generator.html"}:
            key = _first(query, "key")
            if key == CONTENT_ADMIN_KEY:
                return self._file(ROOT_DIR / "frontend" / "content_generator.html", "text/html; charset=utf-8")
            return self._html(_content_generator_lock_page())

        if path in {"/pay", "/pay/h5"}:
            order_id = _first(query, "order_id") or uuid4().hex
            return_url = _first(query, "return_url")
            return self._html(_pay_h5_page(order_id, return_url))

        return self._json({"detail": "not found"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        payload = self._read_payload()

        try:
            if path == "/analyze":
                return self._handle_analyze(payload)

            if path == "/unlock_report":
                return self._handle_unlock_report(payload)

            if path == "/content/generate":
                return self._json(generate_viral_content(
                    structure=payload.get("structure", "波动成长型"),
                    emotion=payload.get("emotion", "迷茫"),
                    platform=payload.get("platform", "小红书"),
                    audience=payload.get("audience", "正在经历人生转折的人"),
                ))

            if path == "/content/batch_generate":
                return self._json(generate_viral_content_batch(
                    structure=payload.get("structure", "波动成长型"),
                    emotions=payload.get("emotions"),
                    platform=payload.get("platform", "小红书"),
                    audience=payload.get("audience", "正在经历人生转折的人"),
                ))

            if path in {"/create_order", "/pay/create_order", "/wxpay/create_order"}:
                return self._handle_create_order(payload)

            if path in {"/pay/confirm", "/confirm_pay"}:
                return self._handle_confirm_pay(payload)

            if path in {"/pay/notify", "/wxpay/notify"}:
                order_id = str(payload.get("order_id", ""))
                if order_id:
                    order_manager.update_status(order_id, "paid")
                return self._json({"status": "success" if order_id else "failed"})

        except ValueError as exc:
            return self._json({"detail": str(exc)}, status=400)
        except Exception as exc:
            return self._json({"detail": str(exc)}, status=500)

        return self._json({"detail": "not found"}, status=404)

    def _handle_analyze(self, payload):
        life_model = build_life_structure_model(
            str(payload.get("birth_time", "")),
            str(payload.get("gender", "")),
        )
        structure = str(life_model["structure_type"])
        return self._json({
            "structure": structure,
            "stage_model": life_model["stage_model"],
            "current_stage": life_model["current_stage"],
            "behavior_tendency": life_model["behavior_tendency"],
            "preview_report": build_preview_report(
                structure=structure,
                psychology_state=payload.get("psychology_state") or {},
                life_model=life_model,
            ),
            "locked_hint": "你的完整人生结构中，还存在更深层的变化节点分析（需付费解锁）",
            "locked_sections": True,
        })

    def _handle_unlock_report(self, payload):
        if payload.get("payment_status") != "paid":
            return self._json({"full_report": "请先完成微信支付解锁完整报告"})

        birth_time = str(payload.get("birth_time", ""))
        gender = str(payload.get("gender", ""))
        life_model = build_life_structure_model(birth_time, gender) if birth_time else None
        structure = str(payload.get("structure") or (
            life_model["structure_type"] if life_model else classify_structure(birth_time)
        ))

        return self._json({
            "full_report": pay_unlock(
                structure=structure,
                birth_time=birth_time,
                gender=gender,
                psychology_state=payload.get("psychology_state") or {},
                life_model=life_model,
            )
        })

    def _handle_create_order(self, payload):
        order = order_manager.create_order(amount=29, pay_type="wechat")
        return_url = payload.get("return_url")
        pay_url = f"/pay/h5?order_id={order.order_id}"
        if return_url:
            pay_url += f"&return_url={quote(str(return_url), safe='')}"
        return self._json({
            "order_id": order.order_id,
            "pay_url": pay_url,
            "pay_type": order.pay_type,
        })

    def _handle_confirm_pay(self, payload):
        order_id = str(payload.get("order_id", ""))
        if order_id:
            order_manager.update_status(order_id, "paid")
        return self._json({"status": "paid"})

    def _read_payload(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        content_type = self.headers.get("Content-Type", "")

        if "application/json" in content_type:
            return json.loads(raw or "{}")

        data = parse_qs(raw)
        return {key: values[0] if values else "" for key, values in data.items()}

    def _json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html(self, html, status=200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, file_path, content_type):
        body = Path(file_path).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _first(query, key):
    values = query.get(key) or []
    return values[0] if values else ""


def _pay_h5_page(order_id, return_url):
    return f"""
    <!doctype html>
    <html lang="zh-CN">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>模拟支付</title>
        <style>
          body {{
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: Arial, "Microsoft YaHei", sans-serif;
            background: #f8f5ee;
            color: #171411;
          }}
          .card {{
            width: min(420px, calc(100% - 32px));
            padding: 28px;
            border: 1px solid #d9c99f;
            border-radius: 8px;
            background: #fffdf8;
            text-align: center;
          }}
          button {{
            width: 100%;
            padding: 13px 18px;
            border: 1px solid #d9b769;
            border-radius: 6px;
            background: #171411;
            color: #fff7df;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
          }}
        </style>
      </head>
      <body>
        <main class="card">
          <h1>支付29元解锁完整报告</h1>
          <p>订单号：{order_id}</p>
          <form method="post" action="/pay/confirm">
            <input type="hidden" name="order_id" value="{order_id}" />
            <input type="hidden" name="return_url" value="{return_url or ''}" />
            <button type="submit">已完成支付</button>
          </form>
        </main>
      </body>
    </html>
    """


def _content_generator_lock_page():
    return """
    <!doctype html>
    <html lang="zh-CN">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>内容后台</title>
        <style>
          * { box-sizing: border-box; }
          body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
            font-family: "Microsoft YaHei", Arial, sans-serif;
            background:
              radial-gradient(circle at top, rgba(217, 183, 105, 0.22), transparent 34%),
              linear-gradient(135deg, #080706 0%, #17120c 52%, #050504 100%);
            color: #fff7df;
          }
          .card {
            width: min(420px, 100%);
            padding: 28px;
            border: 1px solid rgba(217, 183, 105, 0.58);
            border-radius: 14px;
            background: rgba(20, 17, 13, 0.96);
          }
          h1 {
            margin: 0 0 10px;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 30px;
          }
          p {
            margin: 0 0 18px;
            color: #d9c99f;
            line-height: 1.7;
          }
          input {
            width: 100%;
            padding: 14px 15px;
            border: 1px solid rgba(217, 183, 105, 0.56);
            border-radius: 10px;
            background: #fffaf0;
            color: #171411;
            font-size: 16px;
            outline: none;
          }
          button {
            width: 100%;
            margin-top: 14px;
            padding: 14px 18px;
            border: 1px solid #d9b769;
            border-radius: 999px;
            background: linear-gradient(135deg, #f0d58a, #b88c37);
            color: #18130d;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
          }
        </style>
      </head>
      <body>
        <main class="card">
          <h1>内容后台</h1>
          <p>请输入后台口令后进入内容生成器。</p>
          <form id="gateForm">
            <input id="keyInput" type="password" placeholder="后台口令" autofocus />
            <button type="submit">进入后台</button>
          </form>
        </main>
        <script>
          document.getElementById("gateForm").addEventListener("submit", (event) => {
            event.preventDefault();
            const key = document.getElementById("keyInput").value.trim();
            window.location.href = "/content-generator?key=" + encodeURIComponent(key);
          });
        </script>
      </body>
    </html>
    """
