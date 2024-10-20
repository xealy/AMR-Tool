from flask import Blueprint, send_from_directory, render_template, request, redirect, send_file, url_for
import os
from datetime import datetime
import shutil
from ultralytics import YOLO
from PIL import Image
import csv


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
    
        # generate timestamped folder names
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        input_folder = f'images/inputs/input_{timestamp}'
        interim_folder = f'images/interim/interim_{timestamp}'
        cropped_folder = f'images/cropped/cropped_{timestamp}'
        output_folder = f'images/outputs/output_{timestamp}'
        output_zips_folder = f'images/output_zips/output_{timestamp}'

        # create directories if they don't exist
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
        if not os.path.exists(interim_folder):
            os.makedirs(interim_folder)
        if not os.path.exists(cropped_folder):
            os.makedirs(cropped_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # iterate through files received from POST request
        for file in files:
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)
            file.save(os.path.join(input_folder, file.filename)) # save file to designated folder

        # RAD MODULE
        rad_model = YOLO("C:/EGH400-UI/ui/models/rad_model.pt")
        results = rad_model.predict(source=f"C:/EGH400-UI/ui/{input_folder}", show=True)
        bounding_boxes = {} # create bounding boxes dictionary (to crop RAD images)
        for idx, result in enumerate(results):
            # save predicted RAD image to interim folder
            og_filename = os.path.basename(result.path)
            result.save(filename=f"C:/EGH400-UI/ui/{interim_folder}/{og_filename}")

            # update bounding boxes dictionary
            key = og_filename
            bbox_array = result.boxes.xyxy.cpu().numpy()
            bbox_array_1d = bbox_array.flatten()
            value = bbox_array_1d
            bounding_boxes.update({key : value})

        # CROP BASED ON RAD MODULE OUTPUT
        for filename in os.listdir(f"C:/EGH400-UI/ui/{interim_folder}"):
            if filename.endswith(".jpg"):
                image_path = os.path.join(f"C:/EGH400-UI/ui/{interim_folder}", filename)
                image = Image.open(image_path)
                if filename in bounding_boxes:
                    bbox = bounding_boxes[filename]
                    cropped_image = image.crop((bbox[0], bbox[1], bbox[2], bbox[3])) # crop image using the bounding box coordinates
                    output_path = os.path.join(f"C:/EGH400-UI/ui/{cropped_folder}", filename) # save cropped image to cropped folder
                    cropped_image.save(output_path)
                    print(f"Cropped image saved to {cropped_folder}")
                else:
                    print(f"No bounding box found for {filename}")

        # CR MODULE
        cr_model = YOLO("C:/EGH400-UI/ui/models/cr_model.pt")
        results = cr_model.predict(source=f"C:/EGH400-UI/ui/{cropped_folder}", show=True)

        output_csv_file = f"C:/EGH400-UI/ui/{output_folder}/amr_readings.csv"
        fieldnames = ['image_name', 'predicted_amr_reading']

        # Check if the CSV file exists
        file_exists = os.path.isfile(output_csv_file)

        # Open the CSV file in append mode
        with open(output_csv_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header only if the file is new
            if not file_exists:
                writer.writeheader()

            for idx, result in enumerate(results):
                og_filename = os.path.basename(result.path)
                image_name = og_filename
                # Save predicted CR image to output folder
                result.save(filename=f"C:/EGH400-UI/ui/{output_folder}/{image_name}")

                # Output AMR readings to CSV file
                sorted_indices = sorted(range(len(result.boxes.xyxy)), key=lambda i: result.boxes.xyxy[i][0])
                sorted_class_predictions = [result.boxes.cls[i] for i in sorted_indices]
                sorted_class_predictions_list = [int(tensor.item()) for tensor in sorted_class_predictions]
                predicted_amr_reading_string = ''.join([str(num) for num in sorted_class_predictions_list])
                predicted_amr_reading_string = predicted_amr_reading_string[:5] + '.' + predicted_amr_reading_string[5:]
                predicted_amr_reading_string = predicted_amr_reading_string + 'kL'

                # Write the row to the CSV file
                writer.writerow({'image_name': image_name, 'predicted_amr_reading': predicted_amr_reading_string})

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

