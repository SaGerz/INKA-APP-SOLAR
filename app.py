from flask import Flask, render_template, request, send_file, jsonify
import base64
from PIL import Image
from io import BytesIO
import os
import torch
import cv2
import numpy as np

# model = torch.hub.load('ultralytics/yolov5', path='Models/best.pt')
model = torch.hub.load('ultralytics/yolov5', 'custom', path='Models/best.pt')
# model.eval()

# app = Flask(__name__)
# app.static_folder = 'static'
# app = Flask(__name__, '/Static')
app = Flask(__name__, static_folder='Static', static_url_path='/Static')


@app.route("/")
def home():
    return render_template("index.html")    

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    image_data = data['image'].split(',')[1]  # Ambil data gambar dari base64 string
    image = Image.open(BytesIO(base64.b64decode(image_data)))

    # Proses gambar dengan model YOLOv5 atau apapun yang Anda gunakan
    # ...
    try: 
    # Simpan gambar di dalam folder static/images
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Gunakan model yolov5 untuk melakukan deteksi pada gambar
        results = model(image)

        # hasil deteksi
        detections = results.xyxy[0].cpu().numpy()
        print(detections)

        # Konversi gambar ke format NumPy
        image_np = np.array(image)

        # Gambar kotak deteksi pada gambar
        for detection in detections:
            x_min, y_min, x_max, y_max, confidence, class_idx = detection
            x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

            # Warna dan label berdasarkan class_idx (jika diperlukan)
            color = (0, 255, 0)  # Misalnya, gunakan warna hijau
            label = f'Class {int(class_idx)}'


            label_text = f'Class {int(class_idx)}'
            if class_idx == 0: 
               label_text = "Apel Segar"
            elif class_idx == 1:
                label_text = "Apel Tidak Segar"

              # Gambar kotak deteksi
            cv2.rectangle(image_np, (x_min, y_min), (x_max, y_max), color, 2)
            cv2.putText(image_np, label_text, (x_min, y_min - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            # cv2.putText(image_np, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Simpan hasil
            # result_image = Image.fromarray(image_np)
            # image.save(result_image_path)
            # result_image.save('Static/Images/detected_image.jpg')
            # result_image_path = os.path.join(os.getcwd(), 'Static/Images/detected_image.jpg')
            result_image = Image.fromarray(image_np)
            result_image_path = os.path.join(os.getcwd(), 'Static/Images/detected_image.jpg')
            result_image.save(result_image_path)

        with open(result_image_path, 'rb') as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        # image.save(os.path.join(os.getcwd(), 'Static/Images/detected.jpg'))
        # image.save('Static/Images/detected.jpg')  # Ganti dengan path yang sesuai

        # return send_file('Static/Images/detected.jpg', as_attachment=True)
        return jsonify({'message': 'Image processed successfully', 'detections': detections.tolist(), 'result_image_base64': image_base64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route("/detected_image", methods=['GET'])
def get_detected_image():
    result_image_path = os.path.join(os.getcwd(), 'Static/Images/detected_image.jpg')
    return send_file(result_image_path, mimetype='image/jpg')


# if __name__ == "__main__":  
#     app.run(debug=True)
if __name__ == "__main__":  
    app.run(debug=False)