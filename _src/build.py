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
LINKS={'#activities':'/activities/','#itinerary':'/activities/#itinerary','#2026-highlights':'/2026/','#talent-show':'/talent-show/','#volunteer':'/volunteer/','#faq':'/faq/','#join-waitlist':'/waitlist/','#partner':'/partner/','#organisers':'/about/','#printables-page':'/printables/'}
cta='''<section style="padding:30px 0 70px"><div class="wrap center">
  <span class="ribbon">2027 waitlist open</span>
  <h2>Be the first to <span class="script">know</span></h2>
  <p class="lead">Tickets open as soon as our 2027 venue is confirmed. Waitlist families get first access and early-bird pricing.</p>
  <p style="margin-top:22px"><a href="/waitlist/" class="btn btn-rose">Join the 2027 waitlist</a> <a href="/activities/" class="btn btn-ghost">See the activities</a></p>
</div></section>'''
printables='''<section id="printables" style="padding-top:20px">
  <style>#printables .acts{grid-template-columns:repeat(2,1fr);max-width:860px;margin-left:auto;margin-right:auto}@media(max-width:560px){#printables .acts{grid-template-columns:1fr}}</style>
  <div class="wrap center">
    <span class="ribbon teal">Free downloads</span>
    <h2>Diwali <span class="script">printables</span> for kids</h2>
    <p class="lead">The same activities our kids loved at Diwali Playdate, ready to print at home or in class. Free for families, teachers and playgroups.</p>
  </div>
  <div class="wrap">
    <div class="acts" style="margin-top:34px">
      <div class="act"><img class="ph" src="/images/dl-ramayan.jpg" alt="Cover of the Ramayan and the story of Diwali picture story" style="object-position:50% 40%"><h3>The <em>Ramayan</em> story</h3><p>The picture story we tell at the playdate: 15 illustrated scenes with a short read-aloud line under each, from Ayodhya to the diyas that welcomed Ram home. About 5 minutes, ages 2–10.</p><p style="margin-top:12px"><a class="btn btn-rose" href="/downloads/ramayan-story-diwali-playdate.pdf" download>Download PDF (6 MB)</a></p></div>
      <div class="act"><img class="ph" src="/images/dl-rangoli.jpg" alt="A rangoli mandala colouring sheet" style="object-position:50% 45%"><h3>Rangoli <em>colouring sheets</em></h3><p>7 designs from a chunky toddler flower to a detailed mandala, plus a finish-the-half page and a dot-rangoli grid. Colour them, or fill them with coloured rice and petals.</p><p style="margin-top:12px"><a class="btn btn-rose" href="/downloads/rangoli-colouring-sheets-diwali-playdate.pdf" download>Download PDF (0.2 MB)</a></p></div>
      <div class="act"><img class="ph" src="/images/dl-raavan.jpg" alt="Sheet of Raavan cup faces to cut out" style="object-position:50% 40%"><h3>Knock the <em>Raavan</em></h3><p>Our most popular game. Print the ten Raavan heads, stick them on paper cups, stack a pyramid and knock it down. Includes a colour-your-own sheet and a scorecard.</p><p style="margin-top:12px"><a class="btn btn-rose" href="/downloads/knock-the-raavan-game-diwali-playdate.pdf" download>Download PDF (1.6 MB)</a></p></div>
      <div class="act"><img class="ph" src="/images/dl-magnatile.jpg" alt="Ram and Sita picture puzzle pieces for magnetic tiles" style="object-position:50% 40%"><h3>Magnetic tile <em>puzzles</em></h3><p>Ram, Sita, Lakshman, Hanuman, Raavan and the golden deer as 2-piece puzzles for toddlers and 4-piece puzzles for older kids. Print, cut, stick on your Magna-Tiles and the puzzle is ready.</p><p style="margin-top:12px"><a class="btn btn-rose" href="/downloads/ramayan-magnetic-tile-puzzles-diwali-playdate.pdf" download>Download PDF (1.9 MB)</a></p></div>
    </div>
    <p class="lead center" style="margin:34px auto 0">Made something lovely? Tag us on Instagram <a href="https://www.instagram.com/diwaliplaydate.singapore/">@diwaliplaydate.singapore</a>.</p>
  </div>
</section>'''
PAGES=[
 ('', 'Diwali Playdate Singapore | Deepavali Events for Kids 2027', None, blocks),
 ('activities','Deepavali Activities &amp; Crafts for Kids, Toddlers &amp; Preschoolers | Singapore','Rangoli, diya painting, henna, puja thali, Knock the Raavan, Ramayan storytime, a kids fashion show and Bollywood dance: see every activity and the evening itinerary.',[named['activities'],named['itinerary'],cta]),
 ('2026','Diwali Playdate 2026 Photos | Deepavali Event for Kids Singapore','Highlights from Diwali Playdate 2026 at Vida Lounge, Vidacity, Pasir Ris: rangoli, crafts, the fashion show and the Bollywood dance party.',[named['2026-highlights'],cta]),
 ('about','Meet the Organisers | Diwali Playdate Singapore','Diwali Playdate Singapore is organised by two Singapore mums and entrepreneurs, Rinie Gupta of Yawn to Dawn and Sana of SympleHost.',[named['organisers'],named['reviews'],why,cta]),
 ('talent-show','Kids Talent Show Nominations | Diwali Playdate Singapore','Nominate your child (ages 1–10) for the Diwali Playdate 2027 talent show. Every performer gets a certificate.',[named['talent-show']]),
 ('volunteer','Volunteer at Diwali Playdate Singapore','Run a craft or activity station at Diwali Playdate 2027. Pick your station and send us a short role-play video.',[named['volunteer']]),
 ('partner','Sponsor or Partner with Diwali Playdate Singapore','Sponsors, vendors, goodie-bag partners and community groups: reach families celebrating Deepavali in Singapore.',[named['partner']]),
 ('printables','Free Diwali Printables for Kids: Ramayan Story, Rangoli Colouring &amp; Games | Singapore','Free Diwali printables for kids: a read-aloud Ramayan picture story, rangoli colouring sheets, Ramayan magnetic tile puzzles and the Knock the Raavan cup game. Print at home or in class.',[printables,cta]),
 ('faq','Diwali Party for Kids in Singapore: FAQ | Diwali Playdate','Ages, tickets, refunds, food, what to wear and more: answers to common questions about Diwali Playdate Singapore.',[named['faq'],cta]),
 ('waitlist','Join the 2027 Waitlist | Diwali Playdate Singapore','Join the Diwali Playdate Singapore 2027 waitlist for first access to tickets and early-bird pricing.',[named['join-waitlist']]),
]

# ---- Guides (blog) ----
GUIDE_CSS='''<style>
.guide{max-width:760px;margin:0 auto;padding:20px 24px 10px}
.guide h1{font-size:clamp(32px,4.4vw,46px);margin:14px 0 18px}
.guide .crumbs{font-size:14px;color:var(--muted)} .guide .crumbs a{color:var(--teal)}
.guide .intro{font-size:18.5px;color:var(--ink)}
.guide h2{font-size:clamp(24px,3vw,30px);margin:38px 0 12px}
.guide p,.guide li{font-size:17px;margin-bottom:12px}
.guide ul,.guide ol{padding-left:22px}
.guide a{color:var(--rose);font-weight:700}
.guide figure{margin:26px 0}.guide figure img{width:100%;border-radius:20px;border:4px solid #fff;box-shadow:0 8px 22px rgba(31,59,56,.13)}
.guide figcaption{font-size:14px;color:var(--muted);margin-top:8px;text-align:center}
.guide .short{background:var(--cream);border:2px solid var(--line);border-radius:20px;padding:18px 22px;margin:24px 0}
.guide .short > b{font-family:Fraunces,serif;font-size:19px;color:var(--teal-d);display:block;margin-bottom:8px}
.guide .short li{margin-bottom:6px}
.guide .more{background:var(--pink);border-radius:20px;padding:18px 22px;margin:34px 0 10px;font-size:17px}
.guide .story li{margin-bottom:10px}
.glist{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;max-width:900px;margin:34px auto 0}
@media(max-width:640px){.glist{grid-template-columns:1fr}}
.glist a{text-decoration:none;color:inherit}
</style>'''
GUIDES=[]
gdir=os.path.join(ROOT,'_src/guides')
for fn in sorted(os.listdir(gdir)):
    if not fn.endswith('.html'): continue
    raw=open(os.path.join(gdir,fn)).read()
    meta=dict(re.findall(r'^(\w+): (.*)$',raw.split('-->')[0],re.M))
    meta['body']=raw.split('-->',1)[1]
    GUIDES.append(meta)
GUIDE_META={}
for g in GUIDES:
    gslug='guides/'+g['slug']
    sec=(f'<section style="padding-top:20px">{GUIDE_CSS}<article class="guide">'
         f'<p class="crumbs"><a href="/guides/">Guides</a> · Diwali Playdate Singapore</p>'
         f'<h1>{g["h1"]}</h1>{g["body"]}</article></section>')
    PAGES.append((gslug,g['title'],g['desc'],[sec,cta]))
    GUIDE_META[gslug]=g
cards=''.join(f'<a class="act" href="/guides/{g["slug"]}/"><img class="ph" src="/images/{g["image"]}" alt="" loading="lazy"><h3>{re.sub(r"<[^>]+>","",g["h1"])}</h3><p>{g["desc"]}</p></a>' for g in GUIDES)
gindex=(f'<section style="padding-top:20px">{GUIDE_CSS}<div class="wrap center"><span class="ribbon orange">Guides</span>'
        f'<h2>Deepavali with <span class="script">kids</span></h2><p class="lead">Ideas, stories and activities for celebrating Deepavali with babies, toddlers and kids in Singapore, from two mums who run Diwali Playdate.</p></div>'
        f'<div class="wrap"><div class="glist">{cards}</div><p class="lead center" style="margin:30px auto 0">Looking for printables? <a href="/printables/" style="color:var(--rose);font-weight:700">Free Diwali printables for kids</a>.</p></div></section>')
PAGES.append(('guides','Deepavali with Kids: Guides, Stories &amp; Activities | Diwali Playdate Singapore','Guides for celebrating Deepavali with kids in Singapore: rangoli ideas for toddlers, the Ramayana story for kids, crafts and activities.',[gindex,cta]))

navhtml='''<nav>
  <div class="wrap">
    <a class="logo" href="/"><span class="script">Diwali</span><b>Playdate SG</b></a>
    <ul>
      <li><a href="/activities/">Activities</a></li>
      <li><a href="/2026/">2026</a></li>
      <li><a href="/about/">About us</a></li>
      <li><a href="/talent-show/">Talent show</a></li>
      <li><a href="/volunteer/">Volunteer</a></li>
      <li><a href="/printables/">Printables</a></li>
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
    h=h.replace('<link rel="canonical" href="'+url+'">','<link rel="canonical" href="'+url+'">\n<link rel="alternate" hreflang="en-SG" href="'+url+'">\n<link rel="alternate" hreflang="x-default" href="'+url+'">')
    h=h.replace('<meta property="og:url" content="https://diwaliplaydatesingapore.com/">',f'<meta property="og:url" content="{url}">')
    for b in ld_blocks(h):
        t=json.loads(re.search(r'>(.*)</script>',b,re.S).group(1))['@type']
        keep=(slug=='' and t in('Organization','Event')) or (slug=='faq' and t=='FAQPage') or (slug=='2026' and t=='Event')
        if not keep: h=h.replace(b,'')
    if slug in GUIDE_META:
        g=GUIDE_META[slug]; img='https://diwaliplaydatesingapore.com/images/'+g['image']
        h=re.sub(r'<meta property="og:image" content="[^"]*">',f'<meta property="og:image" content="{img}">',h)
        h=h.replace('<meta property="og:type" content="website">','<meta property="og:type" content="article">')
        art={"@context":"https://schema.org","@type":"Article","headline":re.sub(r"<[^>]+>","",g['h1']),"description":g['desc'],"image":img,"datePublished":g['date'],"dateModified":g['date'],"mainEntityOfPage":url,"author":[{"@type":"Person","name":"Rinie Gupta"},{"@type":"Person","name":"Sana"}],"publisher":{"@type":"Organization","name":"Diwali Playdate Singapore","logo":{"@type":"ImageObject","url":"https://diwaliplaydatesingapore.com/images/deco-diya.png"}}}
        h=h.replace('</head>','<script type="application/ld+json">'+json.dumps(art,ensure_ascii=False)+'</script>\n</head>')
    content='\n\n'.join(parts)
    if slug and slug!='waitlist': content='<div style="height:30px"></div>\n'+content
    page=h+'\n'+navhtml+'\n'+content+'\n\n'+footer
    for a,b in LINKS.items(): page=page.replace(f'href="{a}"',f'href="{b}"')
    out=os.path.join(ROOT,slug,'index.html') if slug else os.path.join(ROOT,'index.html')
    os.makedirs(os.path.dirname(out),exist_ok=True); open(out,'w').write(page)
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://diwaliplaydatesingapore.com/{s+"/" if s else ""}</loc></url>\n' for s,*_ in PAGES)+'</urlset>\n'
open(os.path.join(ROOT,'sitemap.xml'),'w').write(sm)
print('built',len(PAGES),'pages')
