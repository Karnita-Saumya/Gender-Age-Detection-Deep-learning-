from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# model files (assumed to be in project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
faceProto = os.path.join(BASE_DIR, "opencv_face_detector.pbtxt")
faceModel = os.path.join(BASE_DIR, "opencv_face_detector_uint8.pb")
ageProto = os.path.join(BASE_DIR, "age_deploy.prototxt")
ageModel = os.path.join(BASE_DIR, "age_net.caffemodel")
genderProto = os.path.join(BASE_DIR, "gender_deploy.prototxt")
genderModel = os.path.join(BASE_DIR, "gender_net.caffemodel")

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# load nets once (with diagnostics to help Render logs if files are missing)
import logging
logging.basicConfig(level=logging.INFO)

def _print_file_info(path):
    try:
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        logging.info("Model file: %s exists=%s size=%d", path, exists, size)
    except Exception as e:
        logging.error("Error checking file %s: %s", path, e)

_print_file_info(faceModel)
_print_file_info(faceProto)
_print_file_info(ageModel)
_print_file_info(ageProto)
_print_file_info(genderModel)

try:
    faceNet = cv2.dnn.readNet(faceModel, faceProto)
    ageNet = cv2.dnn.readNet(ageModel, ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)
    logging.info("Successfully loaded DNN models.")
except Exception as e:
    logging.exception("Failed to load DNN models: %s", e)
    raise


def read_image_file(file_storage):
    image = Image.open(file_storage.stream).convert('RGB')
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, faceBoxes


def encode_image_to_base64(img_bgr):
    _, buffer = cv2.imencode('.jpg', img_bgr)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    return jpg_as_text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
def index_html():
    return render_template('index.html')


@app.route('/healthz')
def healthz():
    return jsonify({'status': 'ok'})


@app.route('/<path:path>', methods=['GET'])
def spa_fallback(path):
    if path.startswith('static/') or path == 'predict':
        return jsonify({'error': 'not found'}), 404
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'no image provided'}), 400

    file = request.files['image']
    frame = read_image_file(file)
    padding = 20

    resultImg, faceBoxes = highlightFace(faceNet, frame)
    outputs = []
    if not faceBoxes:
        return jsonify({'result_image': encode_image_to_base64(resultImg), 'faces': []})

    for faceBox in faceBoxes:
        face = frame[max(0, faceBox[1] - padding):min(faceBox[3] + padding, frame.shape[0] - 1),
                     max(0, faceBox[0] - padding):min(faceBox[2] + padding, frame.shape[1] - 1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]

        cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 255), 2, cv2.LINE_AA)

        outputs.append({'gender': gender, 'age': age, 'box': faceBox})

    encoded = encode_image_to_base64(resultImg)
    return jsonify({'result_image': encoded, 'faces': outputs})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
