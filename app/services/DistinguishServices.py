import urllib, sys, ssl
import urllib.request as urllib2
import base64, requests, json


def DistinguishServices(image_path):
    host = 'https://dm-57.data.aliyun.com'
    path = '/rest/160601/ocr/ocr_business_card.json'
    method = 'POST'
    appcode = '8ac68238be12493a93ac87cdde4eef19'
    querys = ''
    bodys = {}
    url = host + path
    with open(image_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()

    post_data = json.dumps({"image": s}).encode()
    request = urllib2.Request(url, post_data)
    request.add_header('Authorization', 'APPCODE ' + appcode)

    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib2.urlopen(request, context=ctx)
    content = response.read()
    if (content):
        return content.decode()
    else:
        return None

