from pathlib import Path
from html.parser import HTMLParser
import json, xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.h1=0;self.title=False;self.description=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='title':self.title=True
  if a.get('name')=='description':self.description=True
  if 'id'in a:self.ids.append(a['id'])
  if tag=='a':self.links.append(a.get('href',''))
  if tag=='script' and a.get('src','').startswith('https://'):raise AssertionError('External script in static HTML')
pages={}
for f in root.rglob('*.html'):
 p=Page();p.feed(f.read_text());pages[f]=p
 assert p.h1==1 and p.title and p.description,f
 assert len(set(p.ids))==len(p.ids),f
for f,p in pages.items():
 for link in p.links:
  assert link and link!='#',(f,link)
  if link.startswith('https://'):continue
  path,_,fragment=link.partition('#')
  target=(root/path.lstrip('/')) if path.startswith('/') else (f.parent/path if path else f)
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(f,link)
  if fragment:assert fragment in pages[target].ids,(f,link)
ET.parse(root/'sitemap.xml')
print(f'PASS: {len(pages)} HTML pages, all internal links and fragments, unique IDs, metadata, sitemap XML.')
