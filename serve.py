"""Local static server with the generated 404 page and proper status."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
class Handler(SimpleHTTPRequestHandler):
 def send_error(self,code,message=None,explain=None):
  page=Path(self.directory)/'404.html'
  if code==404 and page.exists():
   data=page.read_bytes();self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers()
   if self.command!='HEAD':self.wfile.write(data)
  else:super().send_error(code,message,explain)
if __name__=='__main__':
 args=argparse.ArgumentParser();args.add_argument('--port',type=int,default=3000);args.add_argument('--host',default='0.0.0.0');a=args.parse_args()
 root=Path(__file__).resolve().parent/'dist'
 if not root.exists():raise SystemExit('Run python3 build.py first')
 print(f'Serving generated site on port {a.port}',flush=True)
 ThreadingHTTPServer((a.host,a.port),lambda *x,**kw:Handler(*x,directory=str(root),**kw)).serve_forever()
