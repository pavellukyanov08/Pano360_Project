from flask import (
    Flask,
    redirect,
    url_for
)
from flask_admin import Admin
import os
from flask_login import LoginManager
from flask_migrate import Migrate

from app.config import Database, db
from app.admin.routes import SectionView
from app.auth.models import User

from app.auth.routes import (
    log_user_page,
    reg_user_page,
    logout_user_page
)

from app.main_page.routes import MainPage

migrate = Migrate()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config.from_object(Database)

db.init_app(app)


app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

migrate.init_app(app, db, directory='app/migrations')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin = Admin(app, name='Pano360 | Admin panel', index_view=SectionView(), template_mode='bootstrap4')


# Main page
main_page = MainPage(app)
app.register_blueprint(main_page.main_page)

# Auth
app.register_blueprint(reg_user_page)
app.register_blueprint(log_user_page)
app.register_blueprint(logout_user_page)

@app.route('/')
def main():
    return redirect(url_for('admin.index'))


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
        app.run(debug=True)
