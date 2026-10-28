#!/usr/bin/env python3
"""Print past newsletter issues sent through Resend (Step 1 memory).

Lists emails the Resend account sent from send.accotton.com whose subject
contains "WoW Forever update", newest first, and prints each one's date,
subject and plain-text body. Standard library only; the agent proxy adds
the Authorization header (RESEND_API_KEY is used instead if set).
"""
import argparse
import datetime
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.resend.com/emails"
SENDER_DOMAIN = "send.accotton.com"
SUBJECT_KEY = "wow forever update"


def get(url):
    key = os.environ.get("RESEND_API_KEY") or "proxy-injected"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {key}", "User-Agent": "forever-updates/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--days", type=int, default=30)
    args = p.parse_args()
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=args.days)

    issues, after = [], None
    try:
        while True:
            page = get(API_URL + "?limit=100" + (f"&after={after}" if after else ""))
            data = page.get("data", [])
            done = False
            for e in data:
                created = datetime.datetime.fromisoformat(e["created_at"].replace(" ", "T")[:19]).replace(
                    tzinfo=datetime.timezone.utc)
                if created < cutoff:
                    done = True
                    break
                if SENDER_DOMAIN in e.get("from", "") and SUBJECT_KEY in e.get("subject", "").lower():
                    issues.append(e)
            if done or not page.get("has_more") or not data:
                break
            after = data[-1]["id"]
        for e in issues:
            body = get(f"{API_URL}/{e['id']}").get("text") or "(no plain-text body)"
            print(f"===== {e['created_at']} | {e['subject']} =====\n{body.strip()}\n")
    except urllib.error.HTTPError as e:
        print(f"Resend error: HTTP {e.code}: {e.read().decode('utf-8', 'replace')}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Resend error: could not reach {API_URL}: {e.reason}", file=sys.stderr)
        return 1

    print(f"{len(issues)} past issue(s) found in the last {args.days} days.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
