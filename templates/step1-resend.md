## Step 1: find what was already reported
Past issues are sent through Resend, and the Gmail connector cannot see them, so check both places:

1a. Resend (main record):
    git clone --depth 1 https://github.com/SolaceStudioDevs/forever-updates-assets /tmp/fu
    python3 /tmp/fu/scripts/list_reported.py --days 30
    It prints every past "WoW Forever update" issue sent from send.accotton.com (date, subject, full plain-text body), newest first. No API key is needed; the environment adds it.

1b. Gmail (older issues and Gmail-fallback issues): use the Gmail connector to search for emails with subject containing "WoW Forever update" (sent and inbox, last 30 days) and read them.

Anything covered in either place has already been reported and must NOT be emailed again. The newest issue's date is roughly the last check time. If list_reported.py fails, say so in your final summary and rely on Gmail plus the baseline below.
