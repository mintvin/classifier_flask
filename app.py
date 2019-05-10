#encoding=utf-8

from flask import Flask,flash,request,redirect,url_for
from flask import render_template,send_from_directory
import os
from werkzeug.utils import secure_filename
import Classifier
import sys
reload(sys)
sys.setdefaultencoding('utf8')


UPLOAD_FOLDER = './data/'
ALLOWED_EXTENSIONS = set(['txt'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return  redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # print file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect(url_for('classifier',filename=filename))   #url_for构建指定函数的url
    return

@app.route('/classifier/<filename>')
def classifier(filename):
    classes = Classifier.classifier(filename)
    print type(classes)
    # for word in classes:
    #     classes = word
        # print classes
    return render_template('classifier.html',result = classes)

    # return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/index/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/classifier/',methods=['GET','POST'])
def text_classifier():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
