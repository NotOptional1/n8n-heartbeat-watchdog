"""Local SMTP sink for testing n8n email workflows without sending real mail.

Usage: pip install aiosmtpd && python smtp_sink.py mail.jsonl
Then point an n8n SMTP credential at host 127.0.0.1, port 2525, no user auth, TLS off.
Every email n8n sends is appended to mail.jsonl as {"to": [...], "data": "<raw message>"}.
Note: n8n Cloud cannot reach your localhost; use a self-hosted/local n8n.
"""
import asyncio, json, sys
from aiosmtpd.controller import Controller

OUT = sys.argv[1] if len(sys.argv) > 1 else "mail.jsonl"


class Sink:
    async def handle_DATA(self, server, session, envelope):
        with open(OUT, "a") as f:
            f.write(json.dumps({"to": envelope.rcpt_tos, "data": envelope.content.decode("utf8", "replace")}) + "\n")
        return "250 OK"


async def main():
    Controller(Sink(), hostname="127.0.0.1", port=2525).start()
    print(f"SMTP sink on 127.0.0.1:2525, writing to {OUT}", flush=True)
    await asyncio.Event().wait()


asyncio.run(main())
