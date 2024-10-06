from flask import Blueprint, send_from_directory, render_template, request, redirect, send_file, url_for
import os
from datetime import datetime
import shutil
from ultralytics import YOLO


bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # UPLOAD BATCH OF IMAGES
        # check if the 'files' input exists in the request
        if 'files' not in request.files:
            print('No file part')
            return redirect(request.url)
        
        files = request.files.getlist('files')
    
        # generate a timestamped folder name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_folder = f'images/inputs/input_{timestamp}'
        output_folder = f'images/outputs/output_{timestamp}'
        output_zips_folder = f'images/output_zips/output_{timestamp}'

        # create directories if they don't exist
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        for file in files:
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)
            
            # save file to designated folder
            file.save(os.path.join(input_folder, file.filename))
        
        print('Files successfully uploaded')

        # PREDICT IMAGES WITH MODEL
        model = YOLO("C:/EGH400-UI/ui/models/ver1.pt")
        results = model.predict(source=f"C:/EGH400-UI/ui/{input_folder}", show=True)
        for idx, result in enumerate(results):
            result.save(filename=f"C:/EGH400-UI/ui/{output_folder}/result_{idx}.jpg")

        # compress the output folder into a ZIP file
        zip_filename = f"{output_zips_folder}.zip"
        shutil.make_archive(output_zips_folder, 'zip', output_folder)

        # redirect to the download route after processing
        return redirect(url_for('main.download_output', filename=zip_filename))

    return render_template('index.html')


@bp.route('/download/<path:filename>', methods=['GET'])
def download_output(filename):
    # serve the zip file for download
    zip_path = os.path.join('C:/EGH400-UI/ui', filename)
    return send_file(zip_path, as_attachment=True)


@bp.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

