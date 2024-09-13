import pycurl, json, certifi
from io import BytesIO

def http_request(url, header=None, postdata=None, direct=False):
        w = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, w)
        c.setopt(c.CAINFO, certifi.where())
        if header: c.setopt(c.HTTPHEADER, header)
        if postdata: 
            if isinstance(postdata, dict):
                postdata = json.dumps(postdata)
            c.setopt(c.POSTFIELDS, postdata)
        c.perform()
        c.close()
        w.seek(0)
        return w if direct else json.loads(w.read().decode('utf-8'))
