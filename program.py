import xgboost as xgb
from URL_stats import features
from dynamic_stats import features1, connection, whois_connect, connection_1
import pandas as pd
import tldextract
from colorama import init, Fore, Style
import pickle

free_hosts = [
    "weebly.com", "wixsite.com", "wix.com", "wordpress.com", "wordpress.org",
    "squarespace.com", "jimdo.com", "jimdosite.com", "jimdofree.com",
    "webnode.com", "webflow.io", "strikingly.com", "yolasite.com",
    "site123.me", "mystrikingly.com", "bravesites.com", "simplesite.com",
    "lovable.app", "framer.app", "framer.site",
    "github.io", "gitlab.io", "vercel.app", "netlify.app", "netlify.com",
    "herokuapp.com", "onrender.com", "render.com", "railway.app",
    "glitch.me", "replit.dev", "repl.co", "pages.dev", "workers.dev",
    "web.app", "firebaseapp.com", "azurewebsites.net", "azurestaticapps.net",
    "pythonanywhere.com", "fly.dev", "deta.app", "surge.sh",
    "000webhostapp.com", "freehostia.com", "infinityfree.net",
    "blogspot.com", "sites.google.com", "forms.gle", "docs.google.com",
    "typeform.com", "jotform.com", "surveysparrow.com", "cognito.com",
    "survey-smiles.com", "paperform.co", "tally.so",
    "s3.amazonaws.com", "storage.googleapis.com", "blob.core.windows.net",
    "sharepoint.com", "onedrive.live.com", "dropbox.com",
    "ddns.net", "dyndns.org", "no-ip.com", "noip.com", "changeip.com",
    "freedns.afraid.org", "dynv6.com", "eu.org",
    "000webhost.com", "byethost.com", "freehosting.com", "awardspace.com",
    "t35.com", "ripway.com", "xtgem.com", "ucoz.com", "ucoz.net",
    "hostinger.com", "x10host.com", "biz.nf", "co.nf","mytemp.website", 
    "000webhost.com", "bit.ly", "bitly.kr", "bl.ink", "buff.ly", "clicky.me", "cutt.ly", 
    "dub.co", "fox.ly", "gg.gg", "han.gl", "is.gd", "kurzelinks.de", 
    "kutt.it", "lstu.fr", "oe.cd", "ow.ly", "rebrandly.com", "reduced.to", 
    "rip.to", "san.aq", "short.io", "shorten-url.com", "shorturl.at", 
    "spoo.me", "switchy.io", "tinu.be", "tinyurl.com", "t.ly", "urlr.me", 
    "v.gd", "vo.la", "yaso.su", "zlnk.com", "sor.bz", "73.nu", "lyn.bz",
    "shlink.io", "yourls.org", "polr.me",
    "git.io", "goo.gl", "me2.do", "cutit.org", "s2r.co", "soo.gd", "hoy.kr", "tr.ee", "bounceme.net", "ddnsking.com", "myftp.biz", "myftp.org", 
"myvnc.com", "onthewifi.com", "redirectme.net", "servebeer.com",
"serveftp.com", "servegame.com", "servehttp.com", "serveminecraft.net",
"servemp3.com", "servepics.com", "servequake.com", "sytes.net",
"viewdns.net", "webhop.me", "zapto.org", "hopto.org",
    "bounceme.net", "ddnsking.com", "myftp.biz", "myftp.org",
    "myvnc.com", "onthewifi.com", "redirectme.net", "servebeer.com",
    "serveftp.com", "servegame.com", "servehttp.com", "serveminecraft.net",
    "servemp3.com", "servepics.com", "servequake.com", "sytes.net",
    "viewdns.net", "webhop.me", "zapto.org", "hopto.org",
    "gotdns.ch", "gotdns.com", "homelinux.com", "homelinux.net",
    "homelinux.org", "homesecuritymac.com", "homesecuritypc.com",
    "homeunix.com", "homeunix.net", "homeunix.org", "isgre.at",
    "kicks-ass.net", "kicks-ass.org", "misecure.com", "myfirewall.org",
    "mysecuritycamera.com", "mysecuritycamera.net", "mysecuritycamera.org",
    "net-freaks.com", "nflfan.org", "nhely.hu", "no-ip.biz", "no-ip.info",
    "no-ip.org", "noip.me", "onthewifi.com", "point2this.com",
    "prettydns.com", "rab.la", "readmy.cf", "rebatesrule.net",
    "selfip.biz", "selfip.com", "selfip.info", "selfip.net", "selfip.org",
    "sellclassics.com", "serveblog.net", "servecounterstrike.com",
    "serveexchange.com", "servehalflife.com", "servehumour.com",
    "serveirc.com", "serveminister.com", "servep2p.com", "serveporn.com",
    "serverminecraft.net", "servequake.com",
    "static-access.net", "strangled.net", "struny.cz",
    "supported.nl", "sysadmin.pl", "system-ns.com",
    "tftpd.net", "theworkpc.com", "tplink.net",
    "tvmobili.com", "twilightparadox.com", "two-step.net",
    "ukluton.com", "undo.it", "unix-lovers.net",
    "urze.pl", "vc.land", "vlexo.net",
    "wdprecords.com", "wikaba.com", "www.dnsalias.com",
    "xxuz.com", "youdontcare.com", "ywcm.pl", "zbomb.de",
    "000space.com", "2freehosting.com", "atwebpages.com",
    "cjb.net", "dno.ru", "ezyro.com",
    "freevar.com", "gigazu.com", "heliohost.org",
    "hol.es", "hostico.ro", "hostoi.com",
    "hphost.co", "iblogger.org", "id.ly",
    "justfree.com", "kwikphp.com", "land.ru",
    "ml", "mypressonline.com", "narod.ru",
    "nazuka.net", "netai.net", "new.tf",
    "nichost.nl", "nx.tc", "openhost.net.nz",
    "orgfree.com", "pixub.com", "pro.tc",
    "prohosts.org", "rf.gd", "s3-website.amazonaws.com",
    "smart-pages.com", "smarterasp.net", "talk.to",
    "tekcities.com", "the-free-site.com", "totalh.com",
    "uhostall.com", "unaux.com", "url.ph",
    "vistanet.co.za", "vv.cc", "web.fc2.com",
    "webng.com", "webs.com", "webselfsite.net",
    "website.pl", "webuda.com", "wink.ws",
    "withtank.com", "xcphost.com", "xzx.ro",
    "zymic.com",
    "adf.ly", "bc.vc", "budurl.com", "chilp.it",
    "cli.gs", "cur.lv", "db.tt", "dlvr.it",
    "doiop.com", "filoops.info", "flip.it",
    "fur.ly", "goo.su", "href.li",
    "ity.im", "j.mp", "kl.am",
    "liip.to", "link.zip.net", "linkbee.com",
    "lnkd.in", "lnk.ms", "lru.jp",
    "mcaf.ee", "migre.me", "minurl.fr",
    "moourl.com", "multiurl.com", "ne1.net",
    "njx.me", "notlong.com", "nu.ms",
    "o-x.fr", "om.ly", "onforb.es",
    "pd.am", "ping.fm", "pnt.me",
    "po.st", "poprl.com", "post.ly",
    "prettylinkpro.com", "profile.to", "qr.cx",
    "qr.net", "rb.gy", "rdd.me",
    "shorl.com", "simurl.com", "snipurl.com",
    "snurl.com", "sp2.ro", "spedr.com",
    "su.pr", "t.co", "ta.gd",
    "tighturl.com", "tiny.cc", "tiny.pl",
    "tinysong.com", "to.ly", "togoto.us",
    "tr.im", "trunc.it", "twit.ac",
    "u.bb", "u.nu", "u6e.de",
    "ul.my", "ur1.ca", "url.co.uk",
    "url4.eu", "urlcut.com", "urlhawk.com",
    "urlx.ie", "urlx.org", "urlzen.com",
    "vgn.am", "vl.am", "w3t.org",
    "wapurl.co.uk", "wipi.es", "wp.me",
    "x.co", "xeeurl.com", "xrl.in",
    "xrl.us", "xurl.es", "xurl.jp",
    "yep.it", "yfrog.com", "yli.fi",
    "youtu.be", "yweb.com", "zi.pe",
    "zipmyurl.com", "zud.me", "zurl.ws",
    "zz.gd",
    "pages.github.com", "raw.github.com", "raw.githubusercontent.com",
    "gist.github.com", "codepen.io", "codesandbox.io",
    "stackblitz.com", "jsfiddle.net", "jsbin.com",
    "plnkr.co", "runkit.com", "observablehq.com",
    "mybinder.org", "deepnote.com", "kaggle.com",
    "huggingface.co", "streamlit.app", "gradio.app",
    "spaces.huggingface.tech",
    "pastebin.com", "paste.ee", "hastebin.com",
    "pastie.org", "dpaste.com", "ghostbin.com",
    "rentry.co", "paste.gg", "privatebin.net",
    "transfer.sh", "file.io", "gofile.io",
    "anonfiles.com", "bayfiles.com", "fileditch.com",
    "tempfile.in", "uploadfiles.io","scanned.page", "urlscan.io", "scanurl.net", "isitphishing.ai",
"safeweb.norton.com", "sitecheck.sucuri.net", "quttera.com",
"transparencyreport.google.com", "redirect.notice.google.com",
"linkredirect.io", "safelinks.protection.outlook.com",
"l.facebook.com", "lm.facebook.com", "l.instagram.com",
"out.reddit.com", "links.twitter.com",
]


whitelist = pd.read_csv("majestic_million.csv", usecols=["Domain"])
whitelist_domains = set(whitelist['Domain'])


with open("spam.txt", "r", encoding="utf-8") as f:
        keywords = f.read()
driver = connection_1()
dd = pd.read_csv("top500Domains.csv", usecols=["Root Domain"])
popular_domains = set(dd["Root Domain"])

url = input("Enter URL:")

ext = tldextract.extract(url)
root_domain = (ext.domain + "." + ext.suffix).lower()

if ext.subdomain:
       domain = ext.subdomain + "." + ext.domain + "." + ext.suffix
else:
       domain = root_domain

is_whitelist = False
if (domain in whitelist_domains or root_domain in whitelist_domains):
        is_whitelist = True
for element in free_hosts:
        if element in domain or element in root_domain:
                is_whitelist = False

if is_whitelist:
        print(Fore.GREEN + "URL is on whitelist: 0% PHISH" + Style.RESET_ALL)
else:
    #static
    static_model = xgb.XGBClassifier()
    static_model.load_model("static_model.json")
    static_results = features(url, popular_domains)
    static_data = pd.DataFrame([static_results])
    y_predict = static_model.predict(static_data)
    y_proba = static_model.predict_proba(static_data)[:,1]
    print(f"STATIC: This site is {y_proba[0] * 100:.2f}% phishing")

    #dynamic
    response, score = connection(url)
    w,  available = whois_connect(url)
    driver.get(url)
    dynamic_results = features1(url, response, driver, w, score, keywords,  available)
    results = static_results | dynamic_results
    data = pd.DataFrame([results])
    data = data.apply(pd.to_numeric, errors='coerce')
    dynamic_model = xgb.XGBClassifier()
    dynamic_model.load_model("dynamic_model.json")
    data = pd.DataFrame([dynamic_results])
    data = data.apply(pd.to_numeric, errors='coerce')
    y_proba2 = dynamic_model.predict_proba(data)[:,1]
    print(f"DYNAMIC: This site is {y_proba2[0] * 100:.2f}% phishing")

    #meta model
    model_xgb = xgb.XGBClassifier()
    model_xgb.load_model("meta_model_1.json")
    with open("meta_model_lr.pkl", "rb") as f:
        model = pickle.load(f)
    X = pd.DataFrame({
        "static_model": y_proba,
        "dynamic_model": y_proba2
    })
    meta_proba = model.predict_proba(X)[:,1]
    meta_proba_xgb = model_xgb.predict_proba(X)[:,1]
    print(f"META MODEL LR: This site is {meta_proba[0] * 100:.2f}% phishing")
    print(f"META MODEL XGB: This site is {meta_proba_xgb[0] * 100:.2f}% phishing")
