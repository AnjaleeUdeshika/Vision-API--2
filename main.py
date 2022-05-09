import io
import os

from flask import Flask, render_template , request


app = Flask(__name__, template_folder='template')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cloud-work-shop-cf633c35db2b.json"

# Imports the Google Cloud client library
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("Data Received Successfully !!!")
    return render_template('index.html')


@app.route('/lable', methods=['GET', 'POST'])
def lable():
    from google.cloud import vision

    image_uri = 'gs://cloud-work-shop/cloudTestImg.jpg'

    # Instantiates a client
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    # Performs label detection on the image file
    response = client.label_detection(image=image)

    print('Labels (and confidence score):')
    

    labels = response.label_annotations
    
    labelName = []
    labelScore = []

    for label in labels:
        resultV = label.description
        labelName.append(resultV)
        resultS = '%.2f%%' % (label.score*100.)
        labelScore.append(resultS)

    return render_template('index.html', labelName=labelName, labelScore=labelScore)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
