from keras.models import load_model

from flask import Flask, request, jsonify
import numpy as np
import urllib.request
import cv2

# Load Model
model = load_model("my_model.h5")


app = Flask(__name__)

@app.route("/predict", methods= ['POST', 'GET'])
def predict():
    

    #Load url from json
    getjson = request.get_json()
    url = getjson['url']
    #Load the image from url
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(arr, -1) # 'Load it as it is'
    #Transform the image
    image = cv2.resize(image,(150,150))
    image = np.reshape(image,[1,150,150,3])
    #Start Predict
    cla = model.predict(image)
    classes = np.argmax(cla)

    return jsonify({"hasil-prediksi" : int(classes)})

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
