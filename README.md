# AMR-Solution

![university project](https://img.shields.io/badge/university%20project-1E90FF)
![final year](https://img.shields.io/badge/final%20year-8A2BE2)

## About
An Automatic Meter Reader (AMR) is a system that automatically reads utility usage. While smart meters are gradually being rolled out, traditional utility meters are still widely used in Australia. Additionally, the manual process of traveling to and recording water meter readings across multiple properties is labor-intensive, making it a good candidate for automation. Since replacing traditional meters with smart meters is both time-consuming and costly, there is a need for an intermediate image-based AMR solution that can be deployed on a mobile device. 

This project responds to this need by creating a practical AMR solution for Australian mechanical water meters using deep learning. Two deep learning models were developed to perform two key functions of an AMR solution. A Reading Area Detection (RAD) module was developed to detect reading area of water meter faces, and a Character Recognition (CR) module was then developed to classify the meter digits within cropped reading areas produced by the RAD module. The complete AMR solution integrates both the RAD and CR modules. The full AMR solution was deployed in a Flask web application with an accompanying user interface to allow users to batch upload meter images and receive predicted readings in a CSV file.

## How to run
To run the web application, use a virtual environment to keep package installations confined to an environment. For this, first install Anaconda and follow the next steps.

### To set up Conda environment:
* conda create --name egh400-env python=3.11
* conda activate egh400-env
* navigate to directory that contains 'requirements.txt'
* pip install -r requirements.txt

### To run Flask app:
* navigate to the directory that contains 'main.py'
* export FLASK_APP=main.py (if using on Mac)
* set FLASK_APP=main.py (if using on Windows -> may also need to run $env:FLASK_APP="main.py")
* flask run

## Demo Video
~ pending ~
