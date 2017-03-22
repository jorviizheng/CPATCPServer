import requests
import json

def post_to_yyf():
    yyf_body = '{"actionID":"147677084425623","bool":2,"cid":-1,"clientID":"900001","getVerifyCode":{"keyword":"","regularExpress":"","spnumber":""},"httpInfo":{"header":{"x-random":"1793","x-sourceid":"204001","x-macaddress":"","x-apptype":"3","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","X-Requested-With":"com.ophone.reader.ui","User-Agent":":v=900001;p=-1;c=-1;b=2","Host":"wap.cmread.com","Pragma":"no-cache","x-user-id":"00001","Accept-Encoding":"gzip, deflate","cltk":"","x-wap-profile":"http://218.249.47.94/Xianghe/MTK_LTE_Phone_L_UAprofile.xml","Cache-Control":"no-cache","terminaluniqueid":"840862000635620","isintegmediaplug":"1","Accept-Language":"zh-CN,en-US;q=0.8","Proxy-Connection":"keep-alive","client_version":"CMREADBC_Android_WH_V6.80_170214","Content-Length":"0","mmisinstall":"-1","x-imsi":"460025954594761"},"method":"GET","needResp":1,"params":"","requrl":"http://wap.cmread.com/rbc/p/mftx1.jsp?=&vt=3&timestamp=1489977119714&cm=M22X0009","respcontent":"","respheader":null,"status":0},"pid":-1,"sessionID":"0c4024becdbf4cca81821ba863b2036f","simInfo":null,"smsInfo":null}'
    r = requests.post("http://172.16.162.224:28000/proxycent/IX/ueb_ix", data=yyf_body)
    print(r.status_code)
    print(r.text)

if __name__ == '__main__':
    post_to_yyf()