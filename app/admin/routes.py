import os
from flask_admin import Admin, BaseView, AdminIndexView, expose
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request
from app.auth.models import User

from .forms import SectionForm
from .models import Section
from ..config import db

class MainAdminDashboard(AdminIndexView):
    @expose('/')
    def index(self):
        current_user = User.query.first()

        return self.render('admin/index.html', user=current_user)


class SectionView(BaseView):
    @expose('/')
    def index(self):
        pass

    def allowed_file(self, filename):
        from main import app
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @expose('/add/', methods=('GET', 'POST'))
    def add_section(self):
        from main import app, s3_client

        breadcrumbs = [
            {'name': 'Главная', 'url': url_for('admin.index')},
            {'name': 'Добавить раздел', 'url': url_for('section.add_section')}
        ]

        add_form = SectionForm()

        if add_form.validate_on_submit():
            title = add_form.title.data
            description = add_form.description.data
            sort_in_list = add_form.sort_in_list.data
            cover_proj = add_form.cover_proj.data

            if cover_proj and self.allowed_file(cover_proj.filename):
                filename = secure_filename(cover_proj.filename)

                file_path = os.path.join(os.getenv('UPLOAD_FOLDER'), filename)
                cover_proj.save(file_path)

                s3_client.upload_file(
                    Filename=file_path,
                    Bucket=s3_client.bucket,
                    Key=filename
                )

                # Опционально: Получение URL файла из S3 для сохранения в базе данных
                file_url = f"{app.config['AWS_S3_ENDPOINT_URL']}/{app.config['AWS_BUCKET_NAME']}/{filename}"

                new_section = Section(
                    title=title,
                    description=description,
                    sort_in_list=sort_in_list,
                    cover_proj=file_url,  # Сохранение URL файла из S3 в базу данных
                )

                db.session.add(new_section)
                db.session.commit()

                # Удаление временного файла после успешной загрузки в S3
                os.remove(file_path)

            return redirect(url_for('admin.index'))

        return render_template('admin/add_section.html', add_form=add_form, breadcrumbs=breadcrumbs)



