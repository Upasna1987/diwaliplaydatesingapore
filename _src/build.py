"""Builds the multi-page site from _src/site.html. Run: python3 _src/build.py"""
import re, os, json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=open(os.path.join(ROOT,'_src/site.html')).read()
src=src.replace('src="images/','src="/images/').replace('url(images/','url(/images/')
head_end=src.index('<body>')+len('<body>')
head=src[:head_end]
body=src[head_end:]
nav=body[:body.index('<header')]
footer=body[body.index('<footer>'):]
blocks=re.findall(r'<header class="hero".*?</header>|<section.*?</section>',body,re.S)
def bid(b):
    m=re.match(r'<(?:section|header)[^>]*id="([^"]+)"',b); return m.group(1) if m else None
named={}; unnamed=[]
for b in blocks:
    i=bid(b)
    if i: named[i]=b
    else: unnamed.append(b)
why,village=unnamed[0],unnamed[1]
LINKS={'#activities':'/activities/','#itinerary':'/activities/#itinerary','#2026-highlights':'/2026/','#talent-show':'/talent-show/','#volunteer':'/volunteer/','#faq':'/faq/','#join-waitlist':'/waitlist/','#partner':'/partner/','#organisers':'/about/'}
cta='''<section style="padding:30px 0 70px"><div class="wrap center">
  <span class="ribbon">2027 waitlist open</span>
  <h2>Be the first to <span class="script">know</span></h2>
  <p class="lead">Tickets open as soon as our 2027 venue is confirmed. Waitlist families get first access and early-bird pricing.</p>
  <p style="margin-top:22px"><a href="/waitlist/" class="btn btn-rose">Join the 2027 waitlist</a> <a href="/activities/" class="btn btn-ghost">See the activities</a></p>
</div></section>'''
PAGES=[
 ('', 'Diwali Playdate Singapore | Deepavali Activities &amp; Event for Kids 2027', None, [named['home'],named['kids-activities'],why,village,named['deepavali-singapore'],cta]),
 ('activities','Deepavali Activities for Kids in Singapore | Diwali Playdate','Rangoli, diya painting, henna, puja thali, Knock the Raavan, Ramayan storytime, a kids fashion show and Bollywood dance: see every activity and the evening itinerary.',[named['activities'],named['itinerary'],cta]),
 ('2026','Diwali Playdate 2026 Photos | Deepavali Event for Kids Singapore','Highlights from Diwali Playdate 2026 at Vida Lounge, Vidacity, Pasir Ris: rangoli, crafts, the fashion show and the Bollywood dance party.',[named['2026-highlights'],cta]),
 ('about','Meet the Organisers | Diwali Playdate Singapore','Diwali Playdate Singapore is organised by two Singapore mums and entrepreneurs, Rinie Gupta of Yawn to Dawn and Sana of SympleHost.',[named['organisers'],why,cta]),
 ('talent-show','Kids Talent Show Nominations | Diwali Playdate Singapore','Nominate your child (ages 1–10) for the Diwali Playdate 2027 talent show. Every performer gets a certificate.',[named['talent-show']]),
 ('volunteer','Volunteer at Diwali Playdate Singapore','Run a craft or activity station at Diwali Playdate 2027. Pick your station and send us a short role-play video.',[named['volunteer']]),
 ('partner','Sponsor or Partner with Diwali Playdate Singapore','Sponsors, vendors, goodie-bag partners and community groups: reach families celebrating Deepavali in Singapore.',[named['partner']]),
 ('faq','FAQ | Diwali Playdate Singapore','Ages, tickets, refunds, food, what to wear and more: answers to common questions about Diwali Playdate Singapore.',[named['faq'],cta]),
 ('waitlist','Join the 2027 Waitlist | Diwali Playdate Singapore','Join the Diwali Playdate Singapore 2027 waitlist for first access to tickets and early-bird pricing.',[named['join-waitlist']]),
]
navhtml='''<nav>
  <div class="wrap">
    <a class="logo" href="/"><span class="script">Diwali</span><b>Playdate SG</b></a>
    <ul>
      <li><a href="/activities/">Activities</a></li>
      <li><a href="/2026/">2026</a></li>
      <li><a href="/about/">About us</a></li>
      <li><a href="/talent-show/">Talent show</a></li>
      <li><a href="/volunteer/">Volunteer</a></li>
      <li><a href="/faq/">FAQ</a></li>
      <li><a href="/waitlist/" class="btn btn-rose">Join waitlist</a></li>
    </ul>
  </div>
</nav>
'''
def ld_blocks(h): return re.findall(r'<script type="application/ld\+json">.*?</script>\n?',h,re.S)
for slug,title,desc,parts in PAGES:
    h=head
    url='https://diwaliplaydatesingapore.com/'+(slug+'/' if slug else '')
    h=re.sub(r'<title>.*?</title>',f'<title>{title}</title>',h)
    if desc:
        h=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{desc}">',h)
        h=re.sub(r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{desc}">',h)
    h=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{title}">',h)
    h=h.replace('<link rel="canonical" href="https://diwaliplaydatesingapore.com/">',f'<link rel="canonical" href="{url}">')
    h=h.replace('<meta property="og:url" content="https://diwaliplaydatesingapore.com/">',f'<meta property="og:url" content="{url}">')
    for b in ld_blocks(h):
        t=json.loads(re.search(r'>(.*)</script>',b,re.S).group(1))['@type']
        keep=(slug=='' and t in('Organization','Event')) or (slug=='faq' and t=='FAQPage') or (slug=='2026' and t=='Event')
        if not keep: h=h.replace(b,'')
    content='\n\n'.join(parts)
    if slug and slug!='waitlist': content='<div style="height:30px"></div>\n'+content
    page=h+'\n'+navhtml+'\n'+content+'\n\n'+footer
    for a,b in LINKS.items(): page=page.replace(f'href="{a}"',f'href="{b}"')
    out=os.path.join(ROOT,slug,'index.html') if slug else os.path.join(ROOT,'index.html')
    os.makedirs(os.path.dirname(out),exist_ok=True); open(out,'w').write(page)
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://diwaliplaydatesingapore.com/{s+"/" if s else ""}</loc></url>\n' for s,*_ in PAGES)+'</urlset>\n'
open(os.path.join(ROOT,'sitemap.xml'),'w').write(sm)
print('built',len(PAGES),'pages')
