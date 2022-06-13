from flask import render_template,request
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

@app.route('/kasuform', methods=['GET','POST'])
def kasuform():
    if request.method == 'GET':
        return render_template('/kasuform.html')
    if request.method == 'POST':
        print('データうけとった')
        data=request.form['dat']
        return f'おまえ{data}っておくってきただろ'
