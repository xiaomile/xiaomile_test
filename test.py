from flask import Flask 
from flask import request,Response 
from time import time
import xml.etree.ElementTree as et
import muban
import hashlib

app = Flask(__name__) 
app.debug = True

@app.route('/index')
def index():
    response = Response()
    response.data = "this is xmile's website!"
    return response
 
@app.route('/wx_flask',methods=['GET','POST']) 
def wechat(): 
    if request.method == 'GET': #这里改写你在微信公众平台里输入的token 
        token = 'xiaomiletushare' #获取输入参数 
        data = request.args 
        signature = data.get('signature','') 
        timestamp = data.get('timestamp','') 
        nonce = data.get('nonce','') 
        echostr = data.get('echostr','') #字典排序 
        list = [token, timestamp, nonce] 
        list.sort() 
        s = list[0] + list[1] + list[2] #sha1加密算法        
        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest() 
        #如果是来自微信的请求，则回复echostr 
        if hascode == signature: 
            return echostr 
        else: 
            return "" 

    if request.method == 'POST': 
        #xmldata = request.args.to_dict()
        xmldata = request.stream.read()
        #print(xmldata)
        xml_rec = et.fromstring(xmldata) 
        ToUserName = xml_rec.find('ToUserName').text 
        #ToUserName = xmldata['ToUserName']
        fromUser = xml_rec.find('FromUserName').text 
        #fromUser = xmldata['FromUserName']
        MsgType = xml_rec.find('MsgType').text 
        #MsgType = xmldata['MsgType']
        Content = xml_rec.find('Content').text 
        #Content = xmldata['Conetent']
        MsgId = xml_rec.find('MsgId').text
        #MsgId = xmldata['MsgId'] 
        return muban.reply_muban(MsgType) % (fromUser, ToUserName, int(time()), Content)

if __name__ == '__main__': 
    app.run(debug=True,host='0.0.0.0',port=80)

