import urllib.request
import urllib.error

try:
    urllib.request.urlopen("https://eznsvreplkrydhmerrzi.supabase.co/rest/v1/")
except urllib.error.HTTPError as e:
    for k, v in e.headers.items():
        print(f"{k}: {v}")
