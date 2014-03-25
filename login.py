
from database import init_db
init_db()
  
from database import db_session
from models import User
 
from flask import Flask, render_template, url_for, request, redirect, flash, session, escape, g#, url_for, about, 
from sqlalchemy import desc

from flask.ext.login import (LoginManager, UserMixin, AnonymousUserMixin,
                             make_secure_token, current_user, login_user,
                             logout_user, user_logged_in, user_logged_out,
                             user_loaded_from_cookie, user_login_confirmed,
                             user_loaded_from_header, user_loaded_from_request,
                             user_unauthorized, user_needs_refresh,
                             make_next_param, login_url, login_fresh,
                             login_required, session_protected,
                             fresh_login_required, confirm_login,
                             encode_cookie, decode_cookie,
                             _secret_key, _user_context_processor,
                             user_accessed)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY']    = 'secret_garden'
#db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.before_request
def before_request():
    g.User = current_user

class UserController:
    @app.route('/')
    def show_entries(): 
        users_query = db_session.query(User)
        
        entries = [dict(user_id=user.user_id, nickname=user.nickname) for user in users_query]

        db_session.close()

        return render_template('user/show_entries.html', entries=entries)

    @app.route('/user/login')
    def login():
        return render_template('/user/login.html')

    @app.route('/user/login', methods=['POST'])
    def login_entries():
        user_id = request.form['user_id']
        password = request.form['password']

        remember_me = False

        if 'remember_me' in request.form:
            remember_me = True

        user = db_session.query(User).filter(User.user_id==user_id).first()
        db_session.close()

        if user is None:
            flash('Username is invalid' , 'error')
            return redirect(url_for('login'))

        if not user.check_password(password):
            flash('Password is invalid : '+password,'error')
            return redirect(url_for('login'))

        login_user(user, remember = remember_me)
        flash('Logged in successfully')
        return redirect(url_for('show_entries'))

    @app.route('/user/logout')
    def logout():
        logout_user()
        return redirect(url_for('show_entries'))

    @app.route('/user/add')
    def add():
        return render_template('user/add.html')

    @app.route('/user/add', methods=['POST'])
    def add_entries():
        u = User(request.form['user_id'], request.form['nickname'])
        u.set_password(request.form['password'])

        db_session.add(u)
        db_session.commit()
        db_session.close()

        flash('New User was successfully posted')
        
        return redirect(url_for('show_entries'))

    @app.route('/user/update/<user_id>')
    @login_required
    def update(user_id):
        if user_id == g.User.user_id :
            user = g.User
            return render_template('/user/update.html', user=user)
        
        flash('Connected to a different user.','error')
        return redirect(url_for('show_entries'))        
    
    @app.route('/user/update/<user_id>', methods=['POST'])
    @login_required
    def update_entries(user_id):
        if request.form['user_id'] == g.User.user_id:
            user = db_session.query(User).filter(User.user_id==request.form['user_id']).first()
            user.nickname = request.form['nickname']
            user.set_password( request.form['password'] )

            db_session.commit()
            db_session.close()
            return redirect(url_for('show_entries'))

        flash('Connected to a different user.','error')

        return redirect(url_for('show_entries'))

    @app.route('/user/delete/', methods=['POST'])
    @login_required
    def delete():
        user_id = request.form['user_id']

        print "delete ID : %s , %s " % (user_id, g.User.user_id)

        if user_id == g.User.user_id:
            db_session.query(User).filter(User.user_id==user_id).delete()
            db_session.commit()
            db_session.close()
            flash('Selected User was successfully deleted')
            return redirect(url_for('show_entries'))

        flash('Connected to a different user.','error')        
        return redirect(url_for('show_entries'))

@login_manager.user_loader
def load_user(user_id):
    #return User.query.get(int(user_id))
    users = db_session.query(User).get(user_id)
    db_session.close()
    print 'load_user Call!!'
    return users


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
