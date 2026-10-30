## Step 1: find what was already reported
Past issues are sent through Resend, and the Gmail connector cannot see them, so check both places:

1a. Resend (main record). List sent emails (the environment replaces the "x" with the real key):
    curl -sS "https://api.resend.com/emails?limit=100" -H "Authorization: Bearer x"
    From the JSON "data" list, keep emails whose "from" contains send.accotton.com and whose "subject" contains "WoW Forever update", created in the last 30 days. Read each one's full text with:
    curl -sS "https://api.resend.com/emails/<id>" -H "Authorization: Bearer x"
    (the "text" field holds the plain-text body).

1b. Gmail (older issues and Gmail-fallback issues): use the Gmail connector to search for emails with subject containing "WoW Forever update" (sent and inbox, last 30 days) and read them.

Anything covered in either place has already been reported and must NOT be emailed again. The newest issue's date is roughly the last check time. If the Resend check fails, say so in your final summary and rely on Gmail plus the baseline below.
