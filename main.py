from urllib import request

import boto3
from flask import (
    Flask,
    request,
    redirect,
    url_for
)
from flask_admin import Admin
import os
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

from app.config import Database, db
from app.admin.routes import MainAdminDashboard, SectionView
from app.auth.models import User

from app.auth.routes import (
    log_user_page,
    reg_user_page,
    logout_user_page
)

migrate = Migrate()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config.from_object(Database)
db.init_app(app)



s3_client = boto3.client(
    's3',
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
    bucket = os.getenv('AWS_BUCKET_NAME'),
    endpoint_url = os.getenv('AWS_S3_ENDPOINT_URL'),
    region_name = os.getenv('AWS_S3_REGION_NAME')
)


# def allowed_file(filename):
#     allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


migrate.init_app(app, db, directory='app/migrations')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin = Admin(app, name='Pano360 | Admin panel', index_view=MainAdminDashboard(), template_mode='bootstrap4')
admin.add_view(SectionView(name='Sections', endpoint='section'))

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
