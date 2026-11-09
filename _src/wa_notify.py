#!/usr/bin/env python3
"""Posts each new website sign-up to the Diwali Playdate Planning WhatsApp group.

Reads new rows from the Apps Script inbox (see apps-script.gs) and sends a summary
through the local WhatsApp bridge. Run every few minutes by launchd
(com.upasna.diwali-wa-notify). Config lives in ~/.diwali-wa-notify.json:
  {"url": "<apps script /exec url>", "key": "<READ_KEY>"}
"""
import json, os, sys, urllib.parse, urllib.request

GROUP = os.environ.get('WA_TO', '120363429847512931@g.us')  # Diwali Playdate Planning
BRIDGE = 'http://localhost:8080/api/send'
CONF = os.path.expanduser('~/.diwali-wa-notify.json')
STATE = os.path.expanduser('~/.diwali-wa-notify-state.json')
SKIP = {'_row', 'Submitted at'}
LABELS = {'Waitlist': '🪔 New waitlist sign-up', 'Volunteers': '🙋 New volunteer',
          'Talent show': '🎤 New talent show nomination'}


def clean(v):
    # One line, no WhatsApp formatting, capped, so a form entry can't fake a message layout.
    v = ' '.join(str(v).split())
    for ch in '*_~`':
        v = v.replace(ch, '')
    return v[:300]


def main():
    conf = json.load(open(CONF))
    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    for tab in LABELS:
        after = state.get(tab, 1)
        qs = urllib.parse.urlencode({'key': conf['key'], 'tab': tab, 'after': after})
        rows = json.load(urllib.request.urlopen(f"{conf['url']}?{qs}", timeout=30)).get(tab, [])
        for r in rows:
            row = r.get('_row')
            if not isinstance(row, int) or row <= after:
                continue
            lines = [f"*{LABELS[tab]}*"]
            lines += [f"{k.replace('_', ' ').capitalize()}: {clean(v)}" for k, v in r.items() if k not in SKIP and clean(v)]
            body = json.dumps({'recipient': GROUP, 'message': '\n'.join(lines)}).encode()
            req = urllib.request.Request(BRIDGE, body, {'Content-Type': 'application/json'})
            res = json.load(urllib.request.urlopen(req, timeout=30))
            if not res.get('success'):
                sys.exit(f'bridge send failed: {res}')  # retry next run, keep state
            state[tab] = after = row
            json.dump(state, open(STATE, 'w'))


if __name__ == '__main__':
    main()
