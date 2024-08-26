import os
from flask_admin import AdminIndexView, expose
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, send_from_directory

from app.auth.models import User
from .forms import SectionForm
from .models import Section
from ..config import db

class SectionView(AdminIndexView):
    def get_image(self, filename):
        if filename:
            return url_for('static', filename=os.path.join('uploads', filename))
        return None

    @expose('/')
    def index(self):
        current_user = User.query.first()
        sections = Section.query.all()

        for section in sections:
            section.image_url = self.get_image(section.cover_proj)

        return self.render('admin/index.html', user=current_user, sections=sections)

    def allowed_file(self, filename):
        from main import app
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @expose('/add/', methods=('GET', 'POST'))
    def add_section(self):
        from main import app
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
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                cover_proj.save(file_path)

                new_section = Section(
                    title=title,
                    description=description,
                    sort_in_list=sort_in_list,
                    cover_proj=filename
                )

                db.session.add(new_section)
                db.session.commit()

            return redirect(url_for('admin.index'))

        return render_template('admin/add_section.html', add_form=add_form, breadcrumbs=breadcrumbs)





