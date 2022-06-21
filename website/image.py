


from flask import Flask, Blueprint, render_template, request, flash,  url_for, redirect 

from werkzeug.utils import secure_filename
from flask_login import current_user
import os

app = Flask(__name__)
image = Blueprint('image', __name__)
app.config['IMAGE_UPLOADS'] = r"C:\Users\Cbcbc\Desktop\StCh\website\static\Images"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024



ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@image.route('/')
def upload_form():
	return render_template('image.html', user=current_user)

@image.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('image.html', filename=filename, user=current_user)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@image.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='images/' + filename), code=301)
               