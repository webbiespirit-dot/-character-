# webbiespirit growth plan

The goal is paying clients. The offer that gets them is the one the studio already makes: **a free concept preview of their new website**. Every channel below has one job, which is to get a business owner to say "yes, make me one". The preview then makes the sale.

```
find businesses → first message → follow-ups → they reply → free preview → they see it → client
     (daily)        (ws.py today)   (automatic)   (ws.py set)   (48 h)        (follow up)
```

## The daily program

Run this every morning:

```sh
python3 growth/ws.py today
```

It prints today's time blocks, everyone who needs a follow-up, and the next new leads per channel, each with its message already written. Send them, then log them with `ws.py done ID`. The follow-up dates are set for you. Full command list: `python3 growth/ws.py -h`.

| Day | Focus | First contacts | Also |
| --- | --- | --- | --- |
| Mon | Build the list | 15 emails, 20 DMs | Find 25 new businesses |
| Tue | Phone | 15 calls, 20 DMs, 10 emails | Find 10 |
| Wed | Street | 5 walk-ins, 20 DMs, 15 emails | Find 10 |
| Thu | Phone | 15 calls, 20 DMs, 10 emails | Find 10 |
| Fri | Street + review | 5 walk-ins, 20 DMs | `ws.py stats`, then shift effort to the best channel |
| Sat | Content | 10 DMs | Film 1 Reel + 3 Stories, schedule the week |
| Sun | Rest | | Reply to anyone who wrote |

Every day: follow-ups first, anyone who replied before everything else, one Story, one 15-minute SEO task, and every reply answered the same day. The afternoons go to building previews, because a fast, good preview is what turns a reply into a client.

### Weekly numbers to watch

These are starting targets, not promises. Adjust them from your own `ws.py stats` after two weeks.

| | Per week |
| --- | --- |
| First contacts | about 200 |
| Replies (expect a few percent at first) | 6 to 15 |
| Previews delivered | 3 to 5 |
| New clients | the first one is the goal of month one |

Rule of thumb: if a channel gets no replies after about 60 contacts, change the message (a sharper hook), not the volume.

## Who to contact

Best fits are businesses that rely on people finding them, with no website, a broken or very old one, or only a Facebook or Instagram page: cafés, restaurants, beauty and hair salons, clinics and dentists, gyms and studios, tradespeople, holiday rentals, tour operators, real-estate agents, shops.

Where to find them:

- **Google Maps.** Search "κομμωτήριο Λεμεσός", "dentist Larnaca", and so on. Look for listings with no website link, or open the site on your phone and note what's wrong (slow, not mobile-friendly, last updated years ago). That note becomes the `--hook`.
- **Instagram.** Browse location tags (Limassol, Paphos, Nicosia, Larnaca, Ayia Napa) and local hashtags. Businesses with an active account and no link in bio are ideal.
- **Walking.** Shopping streets and new openings. A new business needs a site most.
- **Outside Cyprus.** The same scripts work in English for remote clients. Start once the local routine is running.

Add each one as you find it:

```sh
python3 growth/ws.py add "Name of business" --channel instagram --contact @handle --city Limassol --category salon --lang el --hook "στο Instagram, μέσα από τις φωτογραφίες σας"
```

## Instagram and the website, connected

This is the part that runs on its own once set up.

1. **Bio link** on [@webbiespirit](https://www.instagram.com/webbiespirit/): `https://webbiespirit.com/?utm_source=instagram`. The site remembers where the visitor came from and adds it to the subject of their enquiry email ("Free concept preview · instagram"). Visitors who open the site inside Instagram's own browser are tagged too, even without the link. Outreach messages from `ws.py` carry their own tags (`dm`, `email`, `call`, `visit`), so every enquiry in the inbox shows which channel brought it.
2. **Professional account:** switch to a Business or Creator account, category "Web designer", add the email contact button and the location (Cyprus).
3. **Scheduling posts:** connect Instagram to Meta Business Suite (free) and schedule a week of Reels and posts every Saturday. That is Instagram's own automation, and it is safe.
4. **Auto-replies to incoming DMs:** in Instagram's professional settings, set up **Saved replies** with the `dm-` texts from `templates.md`, and **FAQ** questions such as "How does the free preview work?" and "Where are you based?".
5. **Highlights:** "Free preview" (how it works, 3 Stories), "Process", "Contact".
6. **What not to automate:** no bots for DMs, follows or likes. Instagram restricts or bans accounts that use them, and it would put the whole channel at risk.

The two ready-made Reels and their captions are in `social/instagram-reels.md`.

### Content that sells the preview

- "Before and after": a real business's current site next to the preview you designed (ask permission first).
- Screen recordings of a preview being built.
- The presenter Reels, re-cut into 3 or 4 short clips.
- Quick tips: "3 things your café's website needs" and similar.

Do not post invented testimonials, results or client logos. Once a real client agrees, their words become your best post.

## Search engines (SEO)

Already done in this change:

- Titles and descriptions now name the service and place: "Web design in Cyprus" and «Κατασκευή ιστοσελίδων στην Κύπρο».
- Structured data tells Google this is a web design studio in Cyprus offering a free preview.
- `robots.txt` and `sitemap.xml`, with English and Greek versions linked to each other.

Your list, one 15-minute task a day until it's done:

1. Upload `robots.txt` and `sitemap.xml` to the site's root, next to `index.html`.
2. **Google Search Console**: add webbiespirit.com, verify it, submit `sitemap.xml`, request indexing for `/` and `/?lang=el`.
3. **Google Business Profile**: create it as a service-area business covering Cyprus, category "Website designer", with the site and email. This is the biggest single win for local searches like "web design Limassol".
4. **Bing Webmaster Tools**: import from Search Console in one click.
5. Instagram (@webbiespirit, already linked from the site's footer and its structured data), Facebook page and LinkedIn: all link to the site with the same name and description.
6. List the studio in Cyprus business directories and chamber listings, using exactly the same name, email and site everywhere.
7. Once you have real work: add each finished site as a short project page or a section on the home page. Real work is the content that ranks and convinces.
8. Ask every happy client for a Google review.

Next step on the site when there's time: give the Greek version its own address (`/el/`) with the Greek text in the HTML itself. Google ranks a page it can read without running JavaScript more reliably.

## Rules that keep this legal and keep the reputation clean

- **Email:** write one-to-one to business addresses (info@, the owner's work address), say who you are, keep it relevant to their business, and include the opt-out line that the templates already have. Anyone who says no gets `ws.py set ID optout` and never hears from you again. Cyprus follows EU privacy rules (GDPR and the e-privacy law), so don't buy email lists and don't send bulk mail.
- **Calls:** call business numbers in business hours, stop if they ask, and check the Cyprus data protection commissioner's guidance on unsolicited calls.
- **Gmail limits:** send at most about 30 to 40 cold emails a day from a personal Gmail. An address on your own domain (for example hello@webbiespirit.com) looks more professional and protects the main inbox.
- **Claims:** only the confirmed offer. No prices, timelines, guarantees or results in any message until they are real.
