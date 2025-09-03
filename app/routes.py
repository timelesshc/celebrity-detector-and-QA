from flask import Blueprint, request, render_template
from pipeline.image_handler import process_image
from pipeline.celebrity_detector import CelebrityDetector
from pipeline.qa_engine import QAEngine

import base64

main = Blueprint('main', __name__)

celebrity_detector = CelebrityDetector()
qa_engine = QAEngine()

@main.route('/', methods=['GET', 'POST'])
def index():
    celebrity_info = ""
    result_img_data = ""
    user_question = ""
    answer = ""

    if request.method == 'POST':
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                img_bytes, face_coords = process_image(image_file)
                if face_coords is not None:
                    celebrity_info, celebrity_name = celebrity_detector.identify(img_bytes)
                    result_img_data = base64.b64encode(img_bytes).decode('utf-8')
                else:
                    celebrity_info = "No face detected in the image. Please try another image."

        elif 'question' in request.form:
            user_question = request.form['question']
            celebrity_name = request.form['celebrity_name']
            celebrity_info = request.form['celebrity_info']
            result_img_data = request.form['result_img_data']

            answer = qa_engine.answer_question(celebrity_name, user_question)
        
    return render_template('index.html', 
                           celebrity_info=celebrity_info, 
                           result_img_data=result_img_data, 
                           user_question=user_question, 
                           answer=answer)