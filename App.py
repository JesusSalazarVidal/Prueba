from flask import Flask, render_template,request, url_for, redirect, make_response, jsonify
import cv2
import numpy as np
from werkzeug.utils import secure_filename
import os
from datetime import timedelta

# Configuración de formatos de archivo permitidos
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp', 'jpeg', 'JPEG'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
# Establecer el tiempo de caducidad de la caché de archivos estáticos
app.send_file_max_age_default = timedelta(seconds=1)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "Verifique el tipo de imagen cargada, solo png, PNG, jpg, JPG, bmp"})

        basepath = os.path.dirname(__file__)  # ruta del archivo actual

        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))
        f.save(upload_path)

        # Use Opencv para convertir el formato y el nombre de la imagen
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

        return render_template('subida.html')
    return render_template('index.html')


@app.route("/")
def Index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)