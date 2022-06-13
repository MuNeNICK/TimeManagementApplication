from flask import render_template
from app import app 

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/test')
def test():
    chinman = {
        'thing1': '男性器',
        'thing2': '女性器',
        'things': ['ちんこ','まんこ']
    }
    return render_template('/test.html',chinman=chinman)

@app.route('/kasuform')
def kasuform():
    return render_template('/kasuform.html')