# from app import app
from flask import Flask, flash,request,render_template, redirect, url_for
from skimage.metrics import structural_similarity
import imutils
import cv2 as cv
from PIL import Image
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Replace this with your own secret key



UPLOAD_FOLDER = 'app\static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "NaN"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        
            # ML model
            original = Image.open(('app/static/pan-card.jpg'))
            test_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            # resizing Image
            original = original.resize((250,160))
            test_image = test_image.resize((250,160))

            original.save('App/static/original_final.png')
            test_image.save('App/static/test_image_final.png')

            original = cv.imread('App/static/original_final.png')
            test_image = cv.imread('App/static/test_image_final.png')
        
        
            original_grey = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
            test_image_grey = cv.cvtColor(test_image, cv.COLOR_BGR2GRAY)
        
            # Computing the structural similarity index (SSIM) between the two images
            (score, diff) = structural_similarity(original_grey, test_image_grey, full=True)
            diff = (diff * 255).astype("uint8")

            # calculating threshold(converts grey scale to binary) and contours
            thresh = cv.threshold(diff, 0, 255,cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
            cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cnts =imutils.grab_contours(cnts)

            # Bounding rectangles
            for c in cnts:
              (x, y, w, h) = cv.boundingRect(c)
              cv.rectangle(original, (x,y), (x+w, y+h), (0,0,255), 2)
              cv.rectangle(test_image, (x,y), (x+w, y+h), (0,0,255), 2)
            
            if round(score*100, 2) <= 30:
                return render_template('index.html', pred= str("The image is not of a PAN Card"))
            elif round(score*100, 2) >= 30 and round(score*100, 2) <= 80:
                return render_template('index.html', pred= str("This is a tampered PAN Card"))
            else:
                return render_template('index.html', pred= str("This is a real PAN Card"))
    return render_template('index.html')

      
        
# Main Function
# if __name__ == '__main__':
#     app.run(debug=True)
