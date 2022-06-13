from flask import render_template,request,redirect,url_for
from app import app 
from random import randint
from models.user import User_info
from app import db

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/registar', methods=['GET', 'POST'])
def registar():
    if request.method == 'GET':
        return render_template('/registar.html')
    if request.method == 'POST':
        form_name = request.form.get('name')  # str
        form_mail = request.form.get('mail')  # str
        # チェックなしならFalse。str -> bool型に変換
        # form_is_remote = request.form.get('is_remote', default=False, type=bool)
        form_password = request.form.get('password')  # str
        # int, データないとき０
        # form_year = request.form.get('year', default=0, type=int)

        user = User_info(
            name=form_name,
            mail=form_mail,
            password=form_password
            #year=form_year
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/users')
def users_list():
    users = User_info.query.all()
    return render_template('/user_list.html', users=users)

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

@app.route('/batoope',methods=['GET','POST'])
def batoope():
    if request.method == 'GET':
        return render_template('/batoope.html')  
    if request.method == 'POST':
        kitai = {
            '0' : '汎用機',
            '1' : '支援機',
            '2' : '強襲機'
        }
        gundam_mapping = {
            'draw' : '相撃ち！俺もお前も死んだ！',
            'win' : 'お前の勝ち！さすがだ！',
            'lose' : 'お前の負け🤪頼りになるな！' 
        }

        player_kitai_ja = kitai[request.form['gundam']]
        player_kitai = int(request.form['gundam'])
        enemy_kitai = randint(0,2)
        enemy_kitai_ja = kitai[str(enemy_kitai)]
        if player_kitai == enemy_kitai:
            judgement = 'draw'
        elif (player_kitai == 0 and enemy_kitai == 2) or (player_kitai == 1 and enemy_kitai == 0) or (player_kitai == 2 and enemy_kitai == 1):
            judgement = 'win'
        else:
            judgement = 'lose'
        result = {
            'enemy_kitai_ja': enemy_kitai_ja,
            'player_kitai_ja': player_kitai_ja,
            'judgement': gundam_mapping[judgement],
        }
        return render_template('/batoope_result.html', result=result)