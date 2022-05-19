# -*- coding: utf-8 -*- 

import urllib3
import json

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
accessKey = "f12232f7-c030-47d7-a554-642715ec38bf"
analysisCode = "srl"

def get_data(sentences, is_one=True):
    data = []
    if is_one == True:
        text = sentences
        text = text.replace('“', "")
        text = text.replace('”', "")
        text = text.replace("‘", "")
        text = text.replace("’", "")
        text = text.replace("'", "")
        text = text.replace('"', "")
        text = text.strip()
        requestJson = {
			"access_key": accessKey,
			"argument": {
				"text": text,
				"analysis_code": analysisCode
			}
		}

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
            )

        response = json.loads(response.data)
        data.append(response)
    else:
        for sentence in sentences:
            text = sentence
            text = text.replace('“', "")
            text = text.replace('”', "")
            text = text.replace("‘", "")
            text = text.replace("’", "")
            text = text.replace("'", "")
            text = text.replace('"', "")
            text = text.strip()
            requestJson = {
			    "access_key": accessKey,
			    "argument": {
				    "text": text,
				    "analysis_code": analysisCode
			    }
		    }
            http = urllib3.PoolManager()
            response = http.request(
                "POST",
                openApiURL,
                headers={"Content-Type": "application/json; charset=UTF-8"},
                body=json.dumps(requestJson)
                )
            response = json.loads(response.data)
            data.append(response)
    return data

if __name__ == "__main__":
    test = get_data("이것은 테스트 입니다.", True)
    return_object = test[0]
    sentence = return_object['return_object']['sentence'][0]
    print(sentence['text'])
