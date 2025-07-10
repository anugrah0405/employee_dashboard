from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import check_password_hash
from app.models import User

bp = Blueprint('auth', __name__)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('routes.upload'))
        
        # Only flash message when there's an actual failed attempt
        flash('Invalid username or password', 'danger')
    
    # No flash messages on GET requests
    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))