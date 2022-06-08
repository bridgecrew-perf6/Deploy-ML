from keras.models import load_model

import cv2
import numpy as np
import base64
import re


from flask import Flask, request, jsonify

# Load Model
model = load_model("my_model.h5")
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

def transform_img(x):
    img = cv2.imread(x)
    img = cv2.resize(img,(150,150))
    img = np.reshape(img,[1,150,150,3])
    return img

def convertToImg(x):
    with open('img.jpg', 'wb') as output:
        output.write(base64.b64decode(x))


app = Flask(__name__)

@app.route("/", methods= ['POST'])
def coba():
    if request.method == "POST":

        #load image dari post request
        # image = request.files.get('file')
        data = request.get_json()
        image64 = data['base64']
        # if image is None or image.filename == "":
        #     return jsonify({"error": "no file/image"})

        try:
            # Mulai prediksi gambar dari model
            # img_bytes = image.read()
            # pil_img = Image.open(io.BytesIO(img_bytes))
            # img = transform_img(pil_img)
            # cla = model.predict(img)
            # classes = np.argmax(cla)
            convertToImg(image64)
            image = transform_img('img.jpg')
            cla = model.predict(image)
            classes = np.argmax(cla)
            return jsonify({"hasil" :classes})
        except Exception as e:
            return jsonify({"error" : str(e)})

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
