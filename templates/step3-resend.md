STEP 3: BUILD AND SEND THE EMAIL (Resend, with Gmail fallback)

Only send if Step 2 found news that has not already been reported (new changes for other classes or systems count too). (Use the Gmail connector only for the Step 1b search and for the fallback below.) Do not clone the assets repo or run any code from it; download the two files below as reference text only.

3a. Get the template and image list:
    mkdir -p /tmp/fu-out
    curl -sS -o /tmp/fu-out/sample.html https://raw.githubusercontent.com/SolaceStudioDevs/forever-updates-assets/main/templates/newsletter-sample.html
    curl -sS -o /tmp/fu-out/README.md https://raw.githubusercontent.com/SolaceStudioDevs/forever-updates-assets/main/README.md
    Read both files.

3b. Write the HTML to /tmp/fu-out/email.html. Copy the structure, inline styles and colors of /tmp/fu-out/sample.html exactly; only the content changes:
    - Header image row (https://raw.githubusercontent.com/SolaceStudioDevs/forever-updates-assets/main/header/banner-forever.jpg, width="600"), then the dark date bar with today's date and run label (e.g. "Morning edition" / "Evening edition").
    - "Biggest news" dark box: 1-3 sentences on the most important change.
    - One white card per topic: gold-bordered heading ("Class: short summary"), bullet list of changes written "old -> new" with the new value in bold, unconfirmed claims marked "Unconfirmed (guide claim):".
    - Each card ends with a "How this affects you" callout (light gold box) showing the class icon of the character it applies to, linked from https://raw.githubusercontent.com/SolaceStudioDevs/forever-updates-assets/main/icons/ :
        shaman.png = Totes Alot (Tauren Shaman), warlock.png = Summons Alot (Orc Warlock), druid.png = Growlz Alot (Skyborne Druid).
      If a change affects all three, stack the three icons at 36px like the sample's name-reservation card.
    - News photos: 1 to 3 per email in total, at most one per card, picked from the /tmp/fu-out/README.md table by topic and linked from https://raw.githubusercontent.com/SolaceStudioDevs/forever-updates-assets/main/images/<file>. Place it right under the card heading:
        <img src="<url>" alt="<what it shows>" width="560" style="display:block;width:100%;max-width:560px;height:auto;border:0;border-radius:4px;margin:0 0 12px 0;">
      Only use file names that are listed in README.md.
    - Each card ends with a "Source:" link line.
    - "What else changed?" section, placed after the last card and before the footer, built exactly like the one in sample.html (a <details> block with a dark <summary> bar, then a white panel). It lists every new change that is NOT already covered by the cards above, grouped under small gold labels in this order, including only groups that have changes: General & systems, Races, then each other class alphabetically (Hunter, Mage, Paladin, Priest, Rogue, Warrior; plus any Shaman/Warlock/Druid items not in the cards), Dungeons, Raids, PvP, Professions, Items, Bug fixes. One short bullet per change, "old -> new" with the new value in bold, unconfirmed items marked. No icons or photos in this section. End it with a small "Sources:" line. If there is nothing extra, leave the section out.
    - Dark footer: "Sources" list of every link used, then the grey note listing hosts that were blocked from this run's network (or "none").
    - Every image must be a full https://raw.githubusercontent.com/... URL. No base64, no attachments, no cid: images.

3c. Write a plain-text version of the same content to /tmp/fu-out/email.txt (headings in caps, "-" bullets, "How this affects you - <character>: ..." lines, then a "WHAT ELSE CHANGED?" part with the same groups, source URLs at the end). Write the subject line to /tmp/fu-out/subject.txt; it MUST start with "WoW Forever update: ".

3d. Send with Resend using exactly these two commands (the first only packages your files as JSON; the environment replaces the "x" with the real key):
    cd /tmp/fu-out && python3 -c 'import json; print(json.dumps({"from":"Forever Updates <updates@send.accotton.com>","to":["thefeelofcotton383@gmail.com"],"subject":open("subject.txt").read().strip(),"html":open("email.html").read(),"text":open("email.txt").read()}))' > payload.json
    curl -sS -w "\nHTTP %{http_code}\n" -X POST https://api.resend.com/emails -H "Authorization: Bearer x" -H "Content-Type: application/json" --data @/tmp/fu-out/payload.json
    Success = "HTTP 200" and an "id" in the response.

3e. Fallback: if the Resend send fails OR cannot be done for any reason (non-200 response, host blocked, a command denied, files missing), send the email through the Gmail connector instead: to thefeelofcotton383@gmail.com, same subject, the HTML from /tmp/fu-out/email.html as an HTML body (hosted images may not show there; that is expected). If you could not download the template, build the same layout from the description in 3b. Add one line at the top of the footer's grey note: "Sent via Gmail fallback: <what failed>." Never end a run that found new news without sending an email one way or the other.

3f. In your final summary, say which path sent the email (Resend id, or Gmail fallback and why).
