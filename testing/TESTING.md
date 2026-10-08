# How this workflow was tested
1. Run n8n locally and the SMTP sink: `pip install aiosmtpd && python smtp_sink.py mail.jsonl` (listens on 127.0.0.1:2525). Create an SMTP credential for it (host `127.0.0.1`, port `2525`, TLS off).
2. `heartbeat-watchdog-TEST-COPY.json` is the shipped workflow with: a 1-minute schedule, jobs `job-a` and `job-b` limited to 0.01 h (36 s), webhook path `hbtest`, and the sink credential. Import, select the credential, publish.
3. Ping `job-a` every 20 s for ~4 minutes (`curl "http://127.0.0.1:5678/webhook/hbtest?job=job-a"`): `mail.jsonl` gains one "Heartbeat missing" email, for `job-b`, and no more.
4. Stop pinging: one email for `job-a`, none repeated.
5. Ping `job-b` once, stop: one more email for `job-b`.
Stored ping times only update in production (published) executions, so manual "Execute workflow" runs prove nothing here.
