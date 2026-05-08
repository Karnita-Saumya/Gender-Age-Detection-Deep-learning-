from flask import Flask, request, jsonify
import cv2
import numpy as np
import io

app = Flask(__name__)

# model file paths (relative to repo root)
faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"
genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# lazy-loaded nets
faceNet = None
ageNet = None
genderNet = None

def get_nets():
    global faceNet, ageNet, genderNet
    if faceNet is None:
        faceNet = cv2.dnn.readNet(faceModel, faceProto)
    if ageNet is None:
        ageNet = cv2.dnn.readNet(ageModel, ageProto)
    if genderNet is None:
        genderNet = cv2.dnn.readNet(genderModel, genderProto)
    return faceNet, ageNet, genderNet

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
    return faceBoxes

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'no image provided'}), 400

    file = request.files['image'].read()
    nparr = np.frombuffer(file, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({'error': 'could not decode image'}), 400

    faceNet, ageNet, genderNet = get_nets()
    faceBoxes = highlightFace(faceNet, frame)
    results = []
    padding = 20
    for faceBox in faceBoxes:
        x1, y1, x2, y2 = faceBox
        face = frame[max(0, y1 - padding):min(y2 + padding, frame.shape[0] - 1),
                     max(0, x1 - padding):min(x2 + padding, frame.shape[1] - 1)]

        if face.size == 0:
            continue

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]

        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]

        results.append({
            'box': [int(x1), int(y1), int(x2), int(y2)],
            'gender': gender,
            'age': age
        })

    return jsonify({'faces': results})

if __name__ == '__main__':
    # development server
    app.run(host='0.0.0.0', port=8080, debug=True)
