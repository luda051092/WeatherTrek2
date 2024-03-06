from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

# Use the current_app proxy within a request context
def get_login_manager():
    with current_app.app_context():
        from init import login_manager
        return login_manager

db = SQLAlchemy()
login_manager = get_login_manager()

user_bp = Blueprint('user', __name__)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')

@user_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user_dashboard.html', user=current_user)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
