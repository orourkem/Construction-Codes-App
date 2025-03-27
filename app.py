from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///construction_codes.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Basic User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

# Basic Building Code model
class BuildingCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_number = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    section = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        results = BuildingCode.query.filter(
            (BuildingCode.code_number.ilike(f'%{query}%')) |
            (BuildingCode.title.ilike(f'%{query}%')) |
            (BuildingCode.description.ilike(f'%{query}%'))
        ).all()
    else:
        results = []
    return jsonify([{
        'id': code.id,
        'code_number': code.code_number,
        'title': code.title,
        'description': code.description,
        'category': code.category,
        'section': code.section
    } for code in results])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
