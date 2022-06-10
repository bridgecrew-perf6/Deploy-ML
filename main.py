from keras.models import load_model

from flask import Flask, request, jsonify
import numpy as np
import urllib.request
import cv2
import h5py
import gcsfs
# Load Model
#model = load_model("my_model.h5")

FS = gcsfs.GCSFileSystem(project='Rehat', token=
{
  "type": "service_account",
  "project_id": "rehat-351413",
  "private_key_id": "e480a0e969525dcf242100c5977734433c1e5b36",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDKtA5tnHezRUBT\nMSFTkc6w/DjPnStobD6AQSpIchm67s6OQLKTfe9s2lLSTNXX3PYj85t9FsgPZNkY\nS/gCZHE/LuIpZv6JXlBR79NmsYZGEcINhc2lBYrntcYs7Ov73QvNJiZteTgUjLir\ndzzRO/xlWSKa64jM8ccn+YxVZvNSHTsctjie+hyoTiH89vCZobVL18LVqYMOJG/p\n97S6nj5JTU5ow1hOVuM2dvEaFJihyDC+fpIQgYBdNE3Nq52X4luUQRtNov7JKTUB\nYDF/3nWyw0C2jsKewyLFwax0ocrADq01cdeSdIG2rxsQ3BpNQqAX5okrddyDpYaU\nmC10UhjrAgMBAAECggEAA8xT6OHhrE5D4kstYK9+u/o95kX/pjlBAo42CJ16tfH7\nlNbJgdH+Rn/gxWgDKcROKGZMJ4/ht8gf+UCTKRhQtupd+oCfjFtkDeT8hRQWfAGh\nLTewnsL301eomvblhRajPfjVB4AZ+OiaHTxiu1jwZcXBzD1VluGA5dLbOk5viL5S\n4kylsDXnz8m9fuCJa/sIVIgxm8F0uM72BVvrGFpXiX3Raxh7zpEoxIq1OSHMn3jd\nT+A99HNU36iKH+MyCwRdrERN/zKiNdCzbvY/gdVxWFmGa3MsguKOgZNHkOGOyIez\nsDMZ6T9s5fafFybbEBiSNZKezaBSq4fX630NlA7Y4QKBgQD+jgOadboEqMbYZ2mo\nhRUAJ4yYId5QZ46pwi2ABK2X3nhxZtIkp+lw/3W3wZb4kdckBEUeBvh/wBo+hydA\nM6euJyXMeBDvoPTJFiJehUdXDW1du2OP+9GzYrDTlgyJ5wFe8x05TMLOnRhJyeTm\nwvOLAUL3REiVYe5+lLO2Q9XGfQKBgQDL2q2d+3jK7bGMKmRb/EXDaI/urHvhSuy9\nv/wkz32ZHColXUWm7EWPC8ClyG8VX68CkQpf4T2tb8ciXZckOgiAQ9Wf0u/+Ys2Y\nL0TQdc5To+c81iVeZxkr0MPkgp9UbPa+2lkudcfEUmSQsva9WS+/lgyPWZmeuB9h\nXRVxHuKxhwKBgHtrIYYfNDyUFCzSHuFM/PyhMEKGkUJMo1fdRLBAFGaAv8bDwnlx\nS/a0dT/NxcPo+fWFeHlxicRuwIq2fqpbIR6H7oSvZg647FYevDU1y3wCj5cVhtVF\nk8u0uuUraBLohLqjhvTEKeOBOUh1cd0MgoZP60b1vXdoDvkiYeuqAhkFAoGAH2XJ\nA+ItkqPVis8ksf5DCHvcX1h1pBeUKw2c2laS87ggzax2A+W0OPoIbABZC6O3IuAQ\nBwB8LXBf7W0Y0F2X3ZmVF463pCi3nc75/FmIs900ymv5SXb7q4H2CgYMYEaAIpki\nz0MYx6YhEyBdXICWGB4WRSX5wTZ+rtJVcRzesZUCgYAwX2oF2oJsIszsfxcQmgSi\niMToonauOLJx1uYAnNdibqc3ec97srhgpYvlGJP8ExhluV6+ceiRn9lCrsGxxlRw\nqb4XzCQfcbSotXTFjrPL3nstBqY/Yft9Y87eNUWFL3Or9t+dhU7KkoZoS0HXAU+A\nZ7ji/g1HgHEruI2k6hgOVQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "access-rehat-model-bucket@rehat-351413.iam.gserviceaccount.com",
  "client_id": "112999879468750158783",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/access-rehat-model-bucket%40rehat-351413.iam.gserviceaccount.com"
})

with FS.open('gs://rehat-model/my_model.h5', 'rb') as model_file:
        model_gcs = h5py.File(model_file, 'r')
        model = load_model(model_gcs)


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
