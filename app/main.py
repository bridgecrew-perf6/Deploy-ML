
from keras.models import load_model
import io
import requests
from flask import Flask, request, jsonify

from PIL import Image
import numpy as np
import urllib.request
import cv2
import base64



# Load Model
eyebagmodel = load_model("eyebag_model_v1.h5")
eyelidmodel = load_model("eyelid_model_v1.h5")


app = Flask(__name__)

@app.route("/predict", methods= ['POST', 'GET'])
def predict():
    

    #Load url from json
    getjson = request.get_json()
    url = getjson['url']
    print(url)
    #Load the image from url
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1) # 'Load it as it is'
    

    '''EyeBag'''

    #Transform
    eb_img = cv2.resize(img,(224,224))
    eb_img = np.reshape(eb_img,[1,224,224,3])
    #Start Predict
    cla = eyebagmodel.predict(eb_img)
    eb_index = np.argmax(cla)
    eb_prob = np.max(cla)
    eb_prob = np.float64(eb_prob)

    '''EyeLid'''
    req = base64.b64encode(urllib.request.urlopen(url).read())
    req = base64.b64decode(req)
    el_img = Image.open(io.BytesIO(req))
    el_img = el_img.resize((150,150))
    el_img = np.array(el_img)
    el_img = np.float64(el_img)
    el_img /= 255
    el_img = np.expand_dims(el_img, axis=0)
    el_img = np.vstack([el_img])
    classes = eyelidmodel.predict(el_img, batch_size=10)
    el_prob = np.float64(classes[0][0])
    if el_prob > 0.5:
        el_index = 0
    else:
        el_index = 1
        
    if eb_index == 0:
        eb_index = 2
    elif eb_index == 1:
        eb_index = 0
    elif eb_index == 2:
        eb_index = 1

    return jsonify({
    "index_eyebag": int(eb_index),
    "index_eyelid": int(el_index),
    "prob_eyebag": eb_prob,
    "prob_eyelid": el_prob
    })

@app.route("/predict64", methods= ['POST', 'GET'])
def predict64():

    #Load url from json
    getjson = request.get_json()
    hasil = getjson['base64']

 
    #Decode the image from base64
    img = base64.b64decode(hasil)
    # print(type(img))


    '''EyeBag'''
    #Convert to array
    eb_img = np.asarray(bytearray(img), dtype=np.uint8)
    eb_img = cv2.imdecode(eb_img, -1)
    #Transform
    eb_img = cv2.resize(eb_img,(224,224))
    eb_img = np.reshape(eb_img,[1,224,224,3])
    #Start Predict
    cla = eyebagmodel.predict(eb_img)
    eb_index = np.argmax(cla)
    eb_prob = np.max(cla)
    eb_prob = np.float64(eb_prob)

    '''EyeLid'''
    el_img = Image.open(io.BytesIO(img))
    #Transform
    el_img = el_img.resize((150,150))
    el_img = np.array(el_img)
    el_img = np.float64(el_img)
    el_img /= 255
    el_img = np.expand_dims(el_img, axis=0)
    el_img = np.vstack([el_img])
    classes = eyelidmodel.predict(el_img, batch_size=10)
    el_prob = np.float64(classes[0][0])
    if el_prob > 0.5:
        el_index = 0
    else:
        el_index = 1

    if eb_index == 0:
        eb_index = 2
    elif eb_index == 1:
        eb_index = 0
    elif eb_index == 2:
        eb_index = 1

    return jsonify({
    "index_eyebag": int(eb_index),
    "index_eyelid": int(el_index),
    "prob_eyebag": eb_prob,
    "prob_eyelid": el_prob
    })
    # return 'ok'


@app.route("/", methods= ['POST', 'GET'])
def coba():
    if request.method == "POST":
        getjson = request.get_json()
        url = getjson['url']
        if url is None or url == "":
            return jsonify({"error": "no file"})
    try:
 
        return jsonify({"hasil-prediksi" : url})
    except Exception as e:
        return jsonify({"error" : str(e)})

if __name__ == "__main__":

    app.run(debug=True)
