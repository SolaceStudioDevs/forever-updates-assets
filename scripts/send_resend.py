#!/usr/bin/env python3
"""Send one newsletter email through Resend's API.

Standard library only. The agent proxy adds the Authorization header for
api.resend.com, so no API key is read here. If RESEND_API_KEY is set (for
running outside that environment), it is sent instead.

Prints the Resend email id on success (exit 0), or the HTTP status and
error body on failure (exit 1).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.resend.com/emails"
DEFAULT_FROM = "Forever Updates <updates@send.accotton.com>"
DEFAULT_TO = "thefeelofcotton383@gmail.com"


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--subject", required=True)
    p.add_argument("--html-file", required=True)
    p.add_argument("--text-file", help="plain-text alternative body")
    p.add_argument("--to", action="append", help="recipient (repeatable)")
    p.add_argument("--from", dest="sender", default=DEFAULT_FROM)
    args = p.parse_args()

    with open(args.html_file, encoding="utf-8") as f:
        payload = {
            "from": args.sender,
            "to": args.to or [DEFAULT_TO],
            "subject": args.subject,
            "html": f.read(),
        }
    if args.text_file:
        with open(args.text_file, encoding="utf-8") as f:
            payload["text"] = f.read()

    headers = {"Content-Type": "application/json", "User-Agent": "forever-updates/1.0"}
    key = os.environ.get("RESEND_API_KEY")
    headers["Authorization"] = f"Bearer {key or 'proxy-injected'}"

    req = urllib.request.Request(
        API_URL, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        print(f"Resend error: HTTP {e.code}: {e.read().decode('utf-8', 'replace')}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Resend error: could not reach {API_URL}: {e.reason}", file=sys.stderr)
        return 1

    if not body.get("id"):
        print(f"Resend error: no id in response: {body}", file=sys.stderr)
        return 1
    print(f"Sent. Resend email id: {body['id']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
