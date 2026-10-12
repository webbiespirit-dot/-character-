#!/usr/bin/env python3
"""webbiespirit outreach: today's plan, lead tracker and ready-to-send messages.

    python3 growth/ws.py today            what to do today, with every message filled in
    python3 growth/ws.py add "Kafe Nero" --channel instagram --contact @kafenero --city Limassol --lang el
    python3 growth/ws.py done 3 7 12      you sent the messages to leads 3, 7 and 12
    python3 growth/ws.py set 3 replied    they wrote back (also: preview, sent, won, lost, optout)
    python3 growth/ws.py msg 3            print the next message for one lead
    python3 growth/ws.py list [--status new]
    python3 growth/ws.py stats
    python3 growth/ws.py emails           today's emails as JSON, for turning into Gmail drafts

Standard library only. Leads live in growth/leads.csv, which opens in any spreadsheet app.
"""
import argparse
import csv
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

# ---- your details: edit these two lines ----
# Who signs each language's messages. Change the Greek spelling if you prefer, e.g. 'Παλιός'.
OWNER = {'en': 'Apollo', 'el': 'Palios'}
PHONE = ''               # optional, e.g. '+357 99 000000'

HERE = Path(__file__).resolve().parent
LEADS = HERE / 'leads.csv'
TEMPLATES = HERE / 'templates.md'
FIRST_EMAIL = HERE / 'email' / 'first-email.html'
SITE = 'https://webbiespirit.com/'
EMAIL = 'webbiespirit@gmail.com'
FIELDS = ['id', 'business', 'name', 'channel', 'contact', 'city', 'category', 'lang', 'hook', 'hook_el',
          'instagram', 'gmail_thread', 'status', 'touches', 'last_touch', 'next_touch', 'added', 'notes']
CHANNELS = ('email', 'instagram', 'call', 'walkin')
STATUSES = ('new', 'contacted', 'replied', 'preview', 'sent', 'won', 'lost', 'optout', 'cold')
# Days to wait after touch 1, 2, 3 ... before the next one. When the list runs out, the lead goes cold.
# Calls and visits: the recap message is due the same day (0), then two email nudges.
CADENCE = {'email': [3, 4, 7], 'instagram': [3, 4], 'call': [0, 4, 7], 'walkin': [0, 4, 7]}
# Tag added to the site link, so cookie-free analytics can show which channel brought each visit.
REF = {'email': 'email', 'instagram': 'dm', 'call': 'call', 'walkin': 'visit'}
# A lead whose --category matches one of these words gets the live site's page for their industry.
INDUSTRY_PAGES = {
    'tattoo-studios/': ('tattoo',),
    'barbers-beauty/': ('barber', 'beauty', 'salon', 'hair', 'nail', 'spa', 'κομμωτ', 'κουρ'),
    'restaurants-cafes/': ('restaurant', 'cafe', 'café', 'coffee', 'bar', 'bakery', 'taverna', 'καφ', 'εστιατ', 'ταβέρν'),
}
# What each status asks of you, and how many days you have.
STATUS_TASK = {
    'replied': (0, 'They replied: get a few lines about the business and start the preview.'),
    'preview': (2, 'Deliver their free preview.'),
    'sent': (3, 'Follow up on the preview you sent: what do they think?'),
}

# New first contacts per channel, by weekday (Mon=0). Matches growth/PLAN.md.
QUOTA = {
    0: {'research': 25, 'email': 15, 'instagram': 20},
    1: {'research': 10, 'call': 15, 'instagram': 20, 'email': 10},
    2: {'research': 10, 'email': 15, 'instagram': 20, 'walkin': 5},
    3: {'research': 10, 'call': 15, 'instagram': 20, 'email': 10},
    4: {'research': 10, 'instagram': 20, 'walkin': 5},
    5: {'instagram': 10},
    6: {},
}
BLOCKS = {
    0: ['09:00 Build the list: find {research} businesses (Google Maps, Instagram locations) and add them',
        '10:30 First emails', '11:30 First Instagram DMs', '12:30 Follow-ups due', '15:00 Work on free previews'],
    1: ['09:00 Follow-ups due', '09:30 Cold calls (10:00 to 12:00 is the best window)', '12:00 Instagram DMs',
        '12:45 First emails', '15:00 Work on free previews', '17:00 Add {research} new leads'],
    2: ['09:00 Follow-ups due', '09:30 First emails', '10:30 Walk-ins (10:00 to 11:30)', '12:30 Instagram DMs',
        '15:00 Work on free previews', '17:00 Add {research} new leads'],
    3: ['09:00 Follow-ups due', '09:30 Cold calls', '12:00 Instagram DMs', '12:45 First emails',
        '15:00 Work on free previews', '17:00 Add {research} new leads'],
    4: ['09:00 Follow-ups due', '09:30 Instagram DMs', '10:30 Walk-ins', '15:00 Work on free previews',
        '16:30 Weekly review: python3 growth/ws.py stats', '17:00 Add {research} new leads'],
    5: ['10:00 Content batch: film or edit 1 Reel and 3 Stories for next week', '11:30 A few Instagram DMs',
        '12:00 Schedule next week\'s posts in Metricool'],
    6: ['Rest. Reply to anyone who wrote back.'],
}
DAILY = [
    'Post 1 Story (a preview in progress, a before/after, a street in Cyprus). A Reel on Mon, Wed and Fri.',
    'Reply to every DM, comment and email within the day.',
    '15 minutes of SEO: today\'s item from the SEO list in growth/PLAN.md.',
]


def today_date(args):
    return dt.date.fromisoformat(args.date) if getattr(args, 'date', None) else dt.date.today()


def load():
    if not LEADS.exists():
        return []
    with LEADS.open(newline='', encoding='utf-8') as f:
        return [dict({k: '' for k in FIELDS}, **row) for row in csv.DictReader(f)]


def save(rows):
    with LEADS.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def find(rows, lead_id):
    for r in rows:
        if r['id'] == str(lead_id):
            return r
    sys.exit(f'No lead with id {lead_id}.')


def templates():
    text = TEMPLATES.read_text(encoding='utf-8')
    return {m.group(1): m.group(2).strip('\n')
            for m in re.finditer(r'^### ([\w.-]+)\s*\n```\n(.*?)\n```', text, re.S | re.M)}


def link(lead):
    cat = lead['category'].lower()
    page = next((p for p, words in INDUSTRY_PAGES.items() if any(w in cat for w in words)), '')
    base = SITE + ('el/' if lead['lang'] == 'el' else '') + page
    return base + f'?ref={REF.get(lead["channel"], "outreach")}'


def signature(lang):
    who = f'{OWNER[lang]}, webbiespirit' if OWNER.get(lang) else 'webbiespirit'
    lines = [who, 'webbiespirit.com · ' + EMAIL]
    if PHONE:
        lines.append(PHONE)
    return '\n'.join(lines)


def template_key(lead):
    n = int(lead['touches'] or 0) + 1
    ch = lead['channel']
    if ch == 'email':
        return f'email-{n}'
    if ch == 'instagram':
        return f'dm-{n}'
    return {1: 'script', 2: 'visit-followup'}.get(n, f'email-{n - 1}')


def render(lead, tpl=None):
    tpl = tpl or templates()
    lang = lead['lang'] if lead['lang'] in ('en', 'el') else 'en'
    key = template_key(lead)
    if key == 'script':
        kind = 'Cold call' if lead['channel'] == 'call' else 'Walk-in'
        return f'Use the {kind} script in growth/templates.md. Log it with done, then send the recap it shows you.'
    body = tpl.get(f'{key}.{lang}') or tpl.get(f'{key}.en')
    if not body:
        return '(no template left for this step)'
    name = lead['name'].strip()
    if lang == 'el':
        hi = f'Καλησπέρα {name},' if name else 'Καλησπέρα σας,'
        hook = lead['hook_el'].strip() or lead['hook'].strip() or 'στο διαδίκτυο'
    else:
        hi = f'Hi {name},' if name else 'Hello,'
        hook = lead['hook'].strip() or 'online'
    return body.format_map({
        'hi': hi, 'business': lead['business'], 'hook': hook, 'name': name or '',
        'city': lead['city'], 'link': link(lead), 'signature': signature(lang), 'owner': OWNER.get(lang, ''),
    })


# The first email goes out in both languages, the lead's own language first.
FIRST = {
    'el': {
        'label': 'Ελληνικά', 'hi': 'Καλησπέρα {name},', 'hi_anon': 'Καλησπέρα σας,',
        'found': 'Βρήκα την επιχείρησή σας {hook}.',
        'intro': 'Λέγομαι {owner} και είμαι από το webbiespirit, ένα στούντιο σχεδιασμού ιστοσελίδων στη Λάρνακα. '
                 'Δουλεύουμε ανάποδα: σας σχεδιάζουμε πρώτα δωρεάν μια μακέτα της νέας σας ιστοσελίδας, '
                 'για να τη δείτε πριν αποφασίσετε οτιδήποτε, και πληρώνετε μόνο αν σας ενθουσιάσει.',
        'steps': ['Μας λέτε δυο λόγια για την επιχείρησή σας.', 'Σχεδιάζουμε δωρεάν τη μακέτα της νέας σας ιστοσελίδας.',
                  'Τη βλέπετε και μετά αποφασίζετε.'],
        'cta': 'Δείτε τη δουλειά μας', 'packages': 'Πακέτα και τιμές',
        'ask': 'Θα θέλατε να σας φτιάξουμε μία;', 'ask_more': 'Αρκεί μια απάντηση μίας γραμμής.',
        'other_lang': 'English below',
    },
    'en': {
        'label': 'English', 'hi': 'Hi {name},', 'hi_anon': 'Hello,',
        'found': 'I came across {business} {hook}.',
        'intro': "I'm {owner}, co-founder of webbiespirit, a web design studio in Larnaca. "
                 'We work the other way round: we design a free concept preview of your new website first, '
                 'so you see it before you decide anything, and you only pay if you love it.',
        'steps': ['You tell us a few lines about your business.', 'We design a preview of your new website, free.',
                  'You see it, then you decide.'],
        'cta': 'See our work', 'packages': 'Packages and prices',
        'ask': 'Would you like one for {business}?', 'ask_more': 'A one-line reply is enough.',
        'other_lang': 'Ελληνικά παρακάτω',
    },
}
SUBJECT = {
    'el': '{business}: δωρεάν μακέτα ιστοσελίδας · A free website preview',
    'en': 'A free website preview for {business} · Δωρεάν μακέτα ιστοσελίδας',
}
OPTOUT = ('Αν δεν θέλετε να σας ξαναγράψουμε, απαντήστε «όχι, ευχαριστώ». '
          'If you would rather not hear from us, reply "no thanks".')


def site_links(lead, lang):
    cat = lead['category'].lower()
    page = next((p for p, words in INDUSTRY_PAGES.items() if any(w in cat for w in words)), '')
    root = SITE + ('el/' if lang == 'el' else '')
    ref = f'?ref={REF.get(lead["channel"], "outreach")}'
    return root + page + ref, root + 'packages/' + ref


def first_email(lead):
    """The bilingual first email: subject, plain text and branded HTML."""
    primary = 'el' if lead['lang'] == 'el' else 'en'
    order = [primary, 'en' if primary == 'el' else 'el']
    name = lead['name'].strip()
    texts, blocks = [], []
    for lang in order:
        c = FIRST[lang]
        hook = (lead['hook_el'] if lang == 'el' else lead['hook']).strip() or ('στο διαδίκτυο' if lang == 'el' else 'online')
        v = {'name': name, 'business': lead['business'], 'hook': hook, 'owner': OWNER.get(lang, '')}
        hi = (c['hi'] if name else c['hi_anon']).format(**v)
        found, intro, ask = c['found'].format(**v), c['intro'].format(**v), c['ask'].format(**v)
        work, packages = site_links(lead, lang)
        steps_txt = '\n'.join(f'{i}. {s}' for i, s in enumerate(c['steps'], 1))
        texts.append(f'{hi}\n\n{found}\n\n{intro}\n\n{steps_txt}\n\n{c["cta"]}: {work}\n{c["packages"]}: {packages}'
                     f'\n\n{ask} {c["ask_more"]}\n\n{v["owner"]}, webbiespirit')
        e = lambda s: html.escape(s, quote=True)
        p = 'margin:0 0 16px;'
        steps_html = ''.join(
            f'<tr><td width="34" valign="top" style="padding:0 0 10px;"><span style="display:inline-block;width:24px;height:24px;'
            f'line-height:24px;text-align:center;border-radius:12px;background:#163F94;color:#FFFFFF;font-size:13px;font-weight:bold;">{i}</span></td>'
            f'<td valign="top" style="padding:2px 0 10px;font-size:15px;line-height:22px;color:#0B2559;">{e(s)}</td></tr>'
            for i, s in enumerate(c['steps'], 1))
        blocks.append(
            f'<tr><td lang="{lang}" style="padding:28px 24px 12px;font-family:Helvetica,Arial,sans-serif;font-size:16px;line-height:25px;color:#0B2559;">'
            f'<div style="font-size:12px;letter-spacing:1.2px;text-transform:uppercase;color:#3A5486;padding-bottom:12px;">{e(c["label"])}</div>'
            f'<p style="{p}">{e(hi)}</p><p style="{p}">{e(found)}</p><p style="{p}">{e(intro)}</p>'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 14px;">{steps_html}</table>'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 12px;"><tr>'
            f'<td style="background:#E0E46A;"><a href="{e(work)}" style="display:inline-block;padding:13px 22px;font-size:15px;font-weight:bold;color:#0B2559;text-decoration:none;">{e(c["cta"])} &rarr;</a></td>'
            f'</tr></table><p style="margin:0 0 18px;font-size:15px;"><a href="{e(packages)}" style="color:#163F94;">{e(c["packages"])}</a></p>'
            f'<p style="{p}"><b>{e(ask)}</b> {e(c["ask_more"])}</p>'
            f'<p style="{p}">{e(v["owner"])}<br><span style="color:#3A5486;">webbiespirit</span></p></td></tr>')
    subject = SUBJECT[primary].format(business=lead['business'])
    text = f'{texts[0]}\n\n— {FIRST[primary]["other_lang"]} —\n\n{texts[1]}\n\nwebbiespirit · Larnaca, Cyprus\nwebbiespirit.com · webbiespirit@gmail.com · Instagram @webbiespirit\n{OPTOUT}'
    doc = FIRST_EMAIL.read_text(encoding='utf-8')
    for k, val in {'lang': primary, 'subject': html.escape(subject), 'block_1': blocks[0], 'block_2': blocks[1],
                   'preheader': html.escape(FIRST[primary]['intro'].format(owner=OWNER.get(primary, ''))[:110]),
                   'tagline': 'Πρώτα δωρεάν μακέτα · Free website preview first', 'site': SITE,
                   'optout': html.escape(OPTOUT)}.items():
        doc = doc.replace('{{' + k + '}}', val)
    return subject, text, doc


def due(lead, day):
    return lead['next_touch'] and dt.date.fromisoformat(lead['next_touch']) <= day


def indent(text, pad='      '):
    return '\n'.join(pad + line if line else '' for line in text.splitlines())


def show(lead, tpl, task=None):
    where = ' · '.join(x for x in (lead['contact'], lead['city'], lead['category']) if x)
    print(f'  [{lead["id"]}] {lead["business"]}  ({lead["channel"]}, {lead["lang"] or "en"})  {where}')
    if task:
        print(f'      → {task}')
    else:
        print(f'      Touch {int(lead["touches"] or 0) + 1}:')
        print(indent(render(lead, tpl)))
    print()


# ---- commands ----

def cmd_today(args):
    day = today_date(args)
    rows = load()
    tpl = templates()
    wd = day.weekday()
    quota = QUOTA[wd]
    print(f'\nwebbiespirit · {day:%A %d %B %Y}\n')
    print('PLAN')
    for b in BLOCKS[wd]:
        print('  ' + b.format(research=quota.get('research', 0)))
    for b in DAILY:
        print('  · ' + b)
    print()

    tasks = [r for r in rows if r['status'] in STATUS_TASK and due(r, day)]
    if tasks:
        print(f'CLIENTS WHO NEED YOU ({len(tasks)})  ← first, always')
        for r in tasks:
            show(r, tpl, STATUS_TASK[r['status']][1])

    follow = [r for r in rows if r['status'] == 'contacted' and due(r, day)]
    print(f'FOLLOW-UPS DUE ({len(follow)})')
    if not follow:
        print('  None today.\n')
    for r in sorted(follow, key=lambda r: r['next_touch']):
        show(r, tpl)

    for ch in CHANNELS:
        want = quota.get(ch, 0)
        if not want:
            continue
        fresh = [r for r in rows if r['status'] == 'new' and r['channel'] == ch][:want]
        print(f'NEW {ch.upper()} ({len(fresh)} of {want} today)')
        if len(fresh) < want:
            print(f'  Add {want - len(fresh)} more {ch} leads with: python3 growth/ws.py add ...\n')
        for r in fresh:
            show(r, tpl)

    print('When a message is sent:  python3 growth/ws.py done ID [ID ...]')
    print('When someone replies:    python3 growth/ws.py set ID replied\n')


def cmd_add(args):
    rows = load()
    next_id = max([int(r['id']) for r in rows if r['id'].isdigit()] or [0]) + 1
    contact = args.contact.strip().lower()
    for r in rows:
        if contact and r['contact'].strip().lower() == contact:
            sys.exit(f'Already tracked as [{r["id"]}] {r["business"]} ({r["status"]}).')
    rows.append({
        'id': str(next_id), 'business': args.business, 'name': args.name or '', 'channel': args.channel,
        'contact': args.contact, 'city': args.city or '', 'category': args.category or '',
        'lang': args.lang, 'hook': args.hook or '', 'hook_el': args.hook_el or '',
        'instagram': args.instagram or '', 'status': 'new', 'touches': '0',
        'last_touch': '', 'next_touch': '', 'added': today_date(args).isoformat(), 'notes': args.notes or '',
    })
    save(rows)
    print(f'Added [{next_id}] {args.business}.')


def cmd_done(args):
    rows = load()
    day = today_date(args)
    for lead_id in args.ids:
        r = find(rows, lead_id)
        if r['status'] in ('optout', 'won', 'lost'):
            print(f'[{r["id"]}] is {r["status"]}; not logging a touch.')
            continue
        n = int(r['touches'] or 0) + 1
        r['touches'] = str(n)
        r['last_touch'] = day.isoformat()
        if r['status'] in STATUS_TASK:
            # You acted on a client task: move it forward.
            if r['status'] == 'replied':
                r['status'] = 'preview'
            elif r['status'] == 'preview':
                r['status'] = 'sent'
            wait = STATUS_TASK.get(r['status'], (3,))[0]
            r['next_touch'] = (day + dt.timedelta(days=wait or 3)).isoformat()
        else:
            steps = CADENCE[r['channel']]
            if n <= len(steps):
                r['status'] = 'contacted'
                r['next_touch'] = (day + dt.timedelta(days=steps[n - 1])).isoformat()
            else:
                r['status'] = 'cold'
                r['next_touch'] = ''
        if args.note:
            r['notes'] = (r['notes'] + ' | ' if r['notes'] else '') + f'{day}: {args.note}'
        nxt = r['next_touch'] or 'no more follow-ups'
        print(f'[{r["id"]}] {r["business"]}: touch {n} logged, {r["status"]}, next {nxt}.')
    save(rows)


def cmd_set(args):
    rows = load()
    day = today_date(args)
    r = find(rows, args.id)
    r['status'] = args.status
    if args.next:
        r['next_touch'] = args.next
    elif args.status in STATUS_TASK:
        r['next_touch'] = (day + dt.timedelta(days=STATUS_TASK[args.status][0])).isoformat()
    elif args.status in ('won', 'lost', 'optout', 'cold'):
        r['next_touch'] = ''
    if args.thread:
        r['gmail_thread'] = args.thread
    if args.note:
        r['notes'] = (r['notes'] + ' | ' if r['notes'] else '') + f'{day}: {args.note}'
    save(rows)
    print(f'[{r["id"]}] {r["business"]} is now {r["status"]}' + (f', next {r["next_touch"]}.' if r['next_touch'] else '.'))


def cmd_msg(args):
    r = find(load(), args.id)
    print(render(r))


def cmd_list(args):
    for r in load():
        if args.status and r['status'] != args.status:
            continue
        print(f'[{r["id"]:>3}] {r["status"]:<9} {r["channel"]:<9} {r["business"]:<30} next {r["next_touch"] or "-"}')


def is_email(contact):
    return bool(re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', contact.strip()))


def cmd_emails(args):
    """Today's emails (follow-ups due, then new email leads up to the quota) as JSON."""
    day = today_date(args)
    rows = load()
    tpl = templates()
    follow = sorted((r for r in rows if r['status'] == 'contacted' and due(r, day)), key=lambda r: r['next_touch'])
    fresh = [r for r in rows if r['status'] == 'new' and r['channel'] == 'email'][:QUOTA[day.weekday()].get('email', 0)]
    out = []
    for r in follow + fresh:
        if not is_email(r['contact']) or template_key(r) == 'script':
            continue
        if r['channel'] == 'email' and int(r['touches'] or 0) == 0:
            subject, text, page = first_email(r)
            out.append({'id': r['id'], 'business': r['business'], 'to': r['contact'].strip(), 'touch': 1,
                        'subject': subject, 'body': text, 'html': page, 'follow_up': False})
            continue
        text = render(r, tpl)
        first, _, body = text.partition('\n')
        subject = re.sub(r'^(Subject|Θέμα):\s*', '', first) if re.match(r'^(Subject|Θέμα):', first) else ''
        out.append({'id': r['id'], 'business': r['business'], 'to': r['contact'].strip(),
                    'touch': int(r['touches'] or 0) + 1, 'subject': subject, 'gmail_thread': r['gmail_thread'],
                    'body': body.strip('\n') if subject else text,
                    'follow_up': int(r['touches'] or 0) > 0})
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_stats(args):
    rows = load()
    day = today_date(args)
    monday = day - dt.timedelta(days=day.weekday())
    week = [r for r in rows if r['last_touch'] and dt.date.fromisoformat(r['last_touch']) >= monday]
    reached = [r for r in rows if int(r['touches'] or 0) > 0 or r['status'] not in ('new',)]
    answered = [r for r in reached if r['status'] in ('replied', 'preview', 'sent', 'won', 'lost')]
    print(f'\nLeads: {len(rows)}')
    for s in STATUSES:
        n = sum(r['status'] == s for r in rows)
        if n:
            print(f'  {s:<10}{n}')
    target = sum(v for wd, q in QUOTA.items() for k, v in q.items() if k != 'research')
    print(f'\nLeads touched since Monday: {len(week)}   (weekly target for first contacts: {target})')
    if reached:
        print(f'Reply rate: {len(answered) / len(reached):.0%} of {len(reached)} reached')
    print('\nBy channel (reached → answered → won):')
    for ch in CHANNELS:
        c = [r for r in reached if r['channel'] == ch]
        if c:
            a = sum(r in answered for r in c)
            w = sum(r['status'] == 'won' for r in c)
            print(f'  {ch:<10}{len(c):>4} → {a:>3} → {w:>3}')
    print('\nPut more of next week into the channel with the best reply rate.\n')


def main():
    p = argparse.ArgumentParser(description='webbiespirit outreach tracker and daily plan.')
    p.add_argument('--date', help='pretend today is YYYY-MM-DD')
    sub = p.add_subparsers(dest='cmd', required=True)

    sub.add_parser('today', help="today's plan and messages")

    a = sub.add_parser('add', help='add a lead')
    a.add_argument('business')
    a.add_argument('--channel', required=True, choices=CHANNELS)
    a.add_argument('--contact', required=True, help='email, @handle, phone or street address')
    a.add_argument('--name', help='first name of the owner or manager, as you would greet them')
    a.add_argument('--city')
    a.add_argument('--category', help='e.g. cafe, salon, dentist')
    a.add_argument('--lang', choices=('en', 'el'), default='en')
    a.add_argument('--hook', help='what you noticed, in English, e.g. "on Instagram, through your new menu"')
    a.add_argument('--hook-el', help='the same in Greek, for Greek messages and the bilingual first email')
    a.add_argument('--instagram', help='their @handle, if they have one')
    a.add_argument('--notes')

    d = sub.add_parser('done', help='log a sent message / call / visit')
    d.add_argument('ids', nargs='+')
    d.add_argument('--note')

    s = sub.add_parser('set', help='change a lead status')
    s.add_argument('id')
    s.add_argument('status', choices=STATUSES)
    s.add_argument('--next', help='next date to act, YYYY-MM-DD')
    s.add_argument('--note')
    s.add_argument('--thread', help='Gmail thread id of the first email, so follow-ups reply in it')

    m = sub.add_parser('msg', help='print the next message for a lead')
    m.add_argument('id')

    l = sub.add_parser('list', help='list leads')
    l.add_argument('--status', choices=STATUSES)

    sub.add_parser('stats', help='funnel and reply rates')
    sub.add_parser('emails', help="today's emails as JSON, for Gmail drafts")

    args = p.parse_args()
    {'today': cmd_today, 'add': cmd_add, 'done': cmd_done, 'set': cmd_set,
     'msg': cmd_msg, 'list': cmd_list, 'stats': cmd_stats, 'emails': cmd_emails}[args.cmd](args)


if __name__ == '__main__':
    main()
