import requests
import urllib

def do_proxy_config_get():
    szJson = urllib.urlencode({"simInfo":{"imsi":"460023772142153","iccid":"89860027201490641653","phone":"15077240944"},"phoneInfo":{"model":"vivo+X9","osversion":"6.0.1","nettype":"1","smsc":"","firm":"vivo","screen":"1080*1920","brand":"vivo","ip":"117.136.41.108","province":"广东","city":"","sn":"21afe0c2","imei":"864278038454713","osbuild":"MMB29M+release-keys","androidid":"689568fe0d30865e"},"messageType":1,"sessionID":"1c62f1c7653a44c5b43f03519115f795","bool":0,"actionID":"110","version":"1.0"})
    args = {"sim" : szJson}

    r = requests.post("http://172.16.162.229:8548", params = args)
    print(r.status_code)
    print(r.text)

if __name__ == '__main__':
    do_proxy_config_get()