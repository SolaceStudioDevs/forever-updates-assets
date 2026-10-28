STEP 3: BUILD AND SEND THE EMAIL (Resend, with Gmail fallback)

Only send if Step 2 found news that has not already been reported. (Step 1 finds already-reported news by searching Gmail with the connector: search the INBOX, not only Sent, for subject "WoW Forever update", because issues now arrive from onboarding@resend.dev. Use the Gmail connector only for that search and for the fallback below.)

3a. Get the assets and template:
    git clone --depth 1 https://github.com/SolaceStudioDevs/forever-updates-assets /tmp/fu
    Read /tmp/fu/templates/newsletter-sample.html and /tmp/fu/README.md.

3b. Write the HTML to /tmp/fu-out/email.html. Copy the structure, inline styles and colors of newsletter-sample.html exactly; only the content changes:
    - Header image row (https://raw.githubusercontent.com/SolaceStudioDevs/forever-updates-assets/main/header/header.jpg, width="600"), then the dark date bar with today's date and run label (e.g. "Morning edition" / "Evening edition").
    - "Biggest news" dark box: 1-3 sentences on the most important change.
    - One white card per topic: gold-bordered heading ("Class: short summary"), bullet list of changes written "old -> new" with the new value in bold, unconfirmed claims marked "Unconfirmed (guide claim):".
    - Each card ends with a "How this affects you" callout (light gold box) showing the class icon of the character it applies to, linked from https://raw.githubusercontent.com/SolaceStudioDevs/forever-updates-assets/main/icons/ :
        shaman.png = Totes Alot (Tauren Shaman), warlock.png = Summons Alot (Orc Warlock), druid.png = Growlz Alot (Skyborne Druid).
      If a change affects all three, stack the three icons at 36px like the sample's name-reservation card.
    - News photos: 1 to 3 per email in total, at most one per card, picked from the README.md table by topic and linked from https://raw.githubusercontent.com/SolaceStudioDevs/forever-updates-assets/main/images/<file>. Place it right under the card heading:
        <img src="<url>" alt="<what it shows>" width="560" style="display:block;width:100%;max-width:560px;height:auto;border:0;border-radius:4px;margin:0 0 12px 0;">
      Only use file names that are listed in README.md.
    - Each card ends with a "Source:" link line.
    - Dark footer: "Sources" list of every link used, then the grey note listing hosts that were blocked from this run's network (or "none").
    - Every image must be a full https://raw.githubusercontent.com/... URL. No base64, no attachments, no cid: images.

3c. Write a plain-text version of the same content to /tmp/fu-out/email.txt (headings in caps, "-" bullets, "How this affects you - <character>: ..." lines, source URLs at the end).

3d. Send with Resend:
    python3 /tmp/fu/scripts/send_resend.py --subject "WoW Forever update: <short summary>" --html-file /tmp/fu-out/email.html --text-file /tmp/fu-out/email.txt --to thefeelofcotton383@gmail.com
    The subject MUST start with "WoW Forever update". The script prints "Sent. Resend email id: ..." and exits 0 on success. No API key is needed; the environment adds it.

3e. Fallback: if the script exits non-zero (any error, including HTTP 403 or the host being blocked), send the same email through the Gmail connector instead: to thefeelofcotton383@gmail.com, same subject, the HTML from /tmp/fu-out/email.html as an HTML body (hosted images may not show there; that is expected). Add one line at the top of the footer's grey note: "Sent via Gmail fallback: Resend failed with <the error message the script printed>."

3f. In your final summary, say which path sent the email (Resend id, or Gmail fallback and why).
