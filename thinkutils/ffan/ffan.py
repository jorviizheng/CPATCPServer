
import requests

def load_page():
    cookie = {"U_UID":"08c42273-56f2-47df-894b-c8d99953eb78"
        , "Hm_lvt_fb34770140e482faedf95446b0f6f575":"1485248992"
        , "CNZZDATA5941576":"cnzz_eid%3D442081799-1485245783-%26ntime%3D1485245783"}

    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; STV100-1 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
        , "Accept-Encoding":"gzip, deflate, sdch"
        , "Host":"h5.ffan.com"
        , "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

    response = requests.get("http://h5.ffan.com/newactivity/161225_promotion_H4.html?promotion_from=70-7-1-1", headers=headers, cookies=cookie)
    print(response.content)
