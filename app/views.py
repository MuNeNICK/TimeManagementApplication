from flask import render_template,request,redirect,url_for, flash
from app import app 
from random import randint
from models.user import User_info
from models.learning_record import Learning_info
from app import db
from flask_login import UserMixin, LoginManager, login_user , logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
import datetime

@app.route('/')
def index():
    if current_user.is_authenticated:
    # トップページにリダイレクト
        return render_template('/stopwatch.html')
   
    return redirect(url_for('login'))

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

        if form_name == '' or form_mail == '' or form_password == '':
            flash('未入力の項目があります', "failed")
            return redirect(url_for('registar'))

        user = User_info(
            name=form_name,
            mail=form_mail,
            password=generate_password_hash(form_password, method='sha256')
            #password=form_password
            #year=form_year
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('name')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        #名前要修正
        user = User_info.query.filter(User_info.name == username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password', "failed")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect('/')
    else:
        return render_template('/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.login_manager.user_loader
def load_user(user_id):
    return User_info.query.get(user_id)

@app.route('/users')
@login_required
def users_list():
    users = User_info.query.all()
    return render_template('/user_list.html', users=users)

@app.route('/users/<int:id>')
@login_required
def user_detail(id):
    user = User_info.query.get(id)
    return render_template('/user_detail.html', user=user)

@app.route('/users/<int:id>/edit', methods=['GET'])
@login_required
def user_edit(id):
    # 編集ページ表示用
    user = User_info.query.get(id)
    return render_template('/user_edit.html', user=user)

@app.route('/users/<int:id>/update', methods=['POST'])
@login_required
def user_update(id):
    user = User_info.query.get(id)  # 更新するデータをDBから取得
    user.name = request.form.get('name')
    user.mail = request.form.get('mail')
    user.password = request.form.get('password')

    db.session.merge(user)
    db.session.commit()
    return redirect(url_for('users_list'))

@app.route('/users/<int:id>/delete', methods=['POST'])  
@login_required
def user_delete(id):  
    user = User_info.query.get(id)   
    db.session.delete(user)  
    db.session.commit()  
    return redirect(url_for('users_list'))

@app.route('/form', methods=['GET','POST'])
@login_required
def form():
    form_user_id = current_user.get_id()
    user = User_info.query.get(form_user_id)
    now = datetime.date.today()
    form_today = now.strftime ('%Y 年 %m 月 %d 日')
    if request.method == 'GET':
        req = request.args
        form_nowtime = req.get("nowtime")
        return render_template('/form.html', user=user, today=form_today, nowtime=form_nowtime)
    if request.method == 'POST':
        form_record = request.form['dat']
        form_nowtime_post = request.form['time']
        lrecord = Learning_info(
            user_id = form_user_id,
            nowtime = form_nowtime_post,
            record = form_record
        )
        db.session.add(lrecord)
        db.session.commit()
        return redirect(url_for('learning_record'))


@app.route('/batoope',methods=['GET','POST'])
@login_required
def batoope():
    if request.method == 'GET':
        return render_template('/batoope.html')  
    if request.method == 'POST':
        kitai = {
            '1' : '汎用機',
            '2' : '支援機',
            '3' : '強襲機'
        }
        gundam_mapping = {
            'draw' : '相撃ち！俺もお前も死んだ！',
            'win' : 'お前の勝ち！さすがだ！',
            'lose' : 'お前の負け🤪頼りになるな！' 
        }

        player_kitai_ja = kitai[request.form['gundam']]
        player_kitai = int(request.form['gundam'])
        enemy_kitai = randint(1,3)
        enemy_kitai_ja = kitai[str(enemy_kitai)]
        if player_kitai == enemy_kitai:
            judgement = 'draw'
        elif (player_kitai == 1 and enemy_kitai == 3) or (player_kitai == 2 and enemy_kitai == 1) or (player_kitai == 3 and enemy_kitai == 2):
            judgement = 'win'
        else:
            judgement = 'lose'
        result = {
            'enemy_kitai_ja': enemy_kitai_ja,
            'player_kitai_ja': player_kitai_ja,
            'judgement': gundam_mapping[judgement],
        }
        return render_template('/batoope_result.html', result=result)

@app.route('/lrecords')
@login_required
def learning_record():
    form_user_id = current_user.get_id()
    lrecords = Learning_info.query.filter(Learning_info.user_id==form_user_id)
    # lrecords = Learning_info.query.all()
    return render_template('/l_record.html', lrecords=lrecords)


@app.errorhandler(401)
def unauthorized(error):
    return redirect(url_for('login'))

@app.errorhandler(404)
def unauthorized(error):
    return redirect(url_for('index'))

@app.route('/stopwatch')
@login_required
def stopwatch():
    return render_template('/stopwatch.html')

