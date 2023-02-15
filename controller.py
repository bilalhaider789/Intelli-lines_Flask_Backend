from app import app
from flask import request,jsonify
import json
from gensim.summarization import summarize
import re
from googletrans import Translator

def BalanceSummarize(text, ratio):
    sum= summarize(text,ratio)
    sum_list=sum.split(".")
    sum_list = [item for item in sum_list if item and item.strip()]
    sum_len=len(sum_list)
    prev_len=0
    prev_list=[]
    if(ratio != 0.05):
        prev_sum= summarize(text,ratio-0.05)
        prev_list=prev_sum.split(".")
        prev_list=[item for item in prev_list if item and item.strip()]
        prev_len=len(prev_list)

    next_sum=summarize(text,ratio+0.05)
    next_list=next_sum.split(".")
    next_list=[item for item in next_list if item and item.strip()]
    next_len=len(next_list)
    
    print("length prev =", prev_len)
    print("length prev =", sum_len)
    print("length prev =",next_len)

    if(sum_len>prev_len and sum_len<next_len):
        # data={"sum":sum,"total":str(len(text.split("."))),"sumlen":str(sum_len),"prelen":str(prev_len),"nextlen":str(next_len), "success": "1"}
        return (sum)

    if(sum_len == prev_len):
        next_split=next_sum.split(".")
        difference=next_len-sum_len
        # if(difference >=2):
        
        for i in range(sum_len, sum_len+(difference//2)+1):
            sum=sum+next_list[i]+"."
    sum_list=sum.split(".")
    sum_list = [item for item in sum_list if item and item.strip()]
    sum_len=len(sum_list)
    # data={"sum":sum,"total":str(len(text.split("."))),"sumlen":str(sum_len),"prelen":str(prev_len),"nextlen":str(next_len), "success": "1"}
    return sum
    
    




@app.route("/text_summary",methods=["POST"])
def text_summary():
    
    request_data = request.data
    request_data = request_data.decode("utf-8")
    request_data = json.loads(request_data)
    sumtype=request_data.get("sumtype")
    sumRatio=float(request_data.get("sumRatio"))/100
    language=request_data.get("language")
    content=request_data.get("content")
    print(sumtype, sumRatio,language)

    translator = Translator()
    lang_detect=translator.detect(content)
    source_lang=lang_detect.lang
    if(source_lang != "en" and source_lang != "ur"):
        return {"success": "0"}
    
    if(source_lang == "ur"):
        content=(translator.translate(content,dest="en")).text
    
    print(content)
    summarization_data=BalanceSummarize(content,sumRatio)
    if (sumtype=="abstractive"):
        if(language=="en"):
            return {"sum": summarization_data, "lang":"en","success": "1", "type": "para"}
        if(language=="ur"):
            summarization_data=(translator.translate(summarization_data, dest="ur")).text
            return {"sum": summarization_data, "lang": "ur","success": "1", "type": "para"}
    if (sumtype=="key"):
        if(language=="en"):
            summarization_data= summarization_data.split(".")
            print(summarization_data)
            return {"sum": str(summarization_data), "lang":"en","success": "1", "type": "key"}
        if(language=="ur"):
            print(123)

    return {"sum": "abc", "success": "1"}


@app.route("/")
def home():
    print("slash rrequested")
    return {"sum":"summarizaion"}



@app.route("/post",methods=["POST"])
def sumtext():
    request_data = request.data
    request_data = request_data.decode("utf-8")
    request_data = json.loads(request_data)
    text=request_data.get("text")
    ratio=request_data.get("ratio")
    
    sum= summarize(text,float(ratio))
    data={"sum":sum}

    return jsonify(data)



@app.route("/eng_eng",methods=["POST"])
def generatebalance():
    request_data = request.data
    request_data = request_data.decode("utf-8")
    request_data = json.loads(request_data)
    text=request_data.get("text")
    ratio=float(request_data.get("ratio"))
    
    sum= summarize(text,ratio)
    sum_list=sum.split(".")
    sum_list = [item for item in sum_list if item and item.strip()]
    sum_len=len(sum_list)
    prev_len=0
    prev_list=[]
    if(ratio != 0.05):
        prev_sum= summarize(text,ratio-0.05)
        prev_list=prev_sum.split(".")
        prev_list=[item for item in prev_list if item and item.strip()]
        prev_len=len(prev_list)

    next_sum=summarize(text,ratio+0.05)
    next_list=next_sum.split(".")
    next_list=[item for item in next_list if item and item.strip()]
    next_len=len(next_list)
    
    print(prev_len, prev_list)
    print(sum_len, sum_list)
    print(next_len, next_list)
    if(sum_len>prev_len and sum_len<next_len):
        data={"sum":sum,"total":str(len(text.split("."))),"sumlen":str(sum_len),"prelen":str(prev_len),"nextlen":str(next_len)}
        return jsonify(data)

    if(sum_len == prev_len):
        print(123)
        next_split=next_sum.split(".")
        difference=next_len-sum_len
        # if(difference >=2):
        
        for i in range(sum_len, sum_len+(difference//2)+1):
            print(i)
            sum=sum+next_list[i]+"."
    sum_list=sum.split(".")
    sum_list = [item for item in sum_list if item and item.strip()]
    sum_len=len(sum_list)
    data={"sum":sum,"total":str(len(text.split("."))),"sumlen":str(sum_len),"prelen":str(prev_len),"nextlen":str(next_len)}
    return jsonify(data)



@app.route("/urdu",methods=["POST"])
def urducheck():
    request_data = request.data
    request_data = request_data.decode("utf-8")
    request_data = json.loads(request_data)
    text=request_data.get("text")
    print(text)
    pattern = re.compile(r'[^\x00-\x7F]+')
    ctext=pattern.sub("", text)
    print(ctext)
    return ctext




@app.route("/translate",methods=["POST"])
def translate():
    request_data = request.data
    request_data = request_data.decode("utf-8")
    request_data = json.loads(request_data)
    text=request_data.get("text")
    translator = Translator()
    a=translator.translate("my name is bilal",dest='ur')
    print(a.text)
    
    return a.text