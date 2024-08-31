import logging
import os
from flask_admin import AdminIndexView, expose
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, request
from collections import OrderedDict

from app.auth.models import User
from .forms import SectionForm
from .models import Section
from ..config import db

class MainAdminPage(AdminIndexView):
    _image_cache = OrderedDict()
    _cache_limit = 100

    def get_image(self, filename):
        if not filename:
            # return url_for('static', filename=os.path.join('uploads', filename))
            return None

        if filename in self._image_cache:
            self._image_cache.move_to_end(filename)
            # print(f'Проверка кэша: {self._image_cache}')
        else:
            if len(self._image_cache) > self._cache_limit:
                self._image_cache.popitem(last=False)

            # Добавление нового элемента в кэш
            self._image_cache[filename] = url_for('static', filename=f'uploads/{filename}')
        # print(f'Кэш: {self._image_cache[filename]}')
        return self._image_cache[filename]

    def clear_cache(self):
        self._image_cache.clear()


    @expose('/')
    @login_required
    def index(self):
        current_user = User.query.first()
        sections = Section.query.all()

        nums_projects = Section.query.count()

        for section in sections:
            section.image_url = self.get_image(section.cover_proj)

        return self.render('admin/index.html', user=current_user, sections=sections, num_projects=nums_projects)

    def allowed_file(self, filename):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @expose('/add/', methods=('GET', 'POST'))
    @login_required
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

    @expose('/edit/<int:idx>', methods=('GET', 'POST'))
    @login_required
    def edit_section(self, idx):
        section = Section.query.get_or_404(idx)
        edit_form = SectionForm(obj=section)

        if edit_form.validate_on_submit():
            edit_form.populate_obj(section)

            db.session.commit()
            # flash('section updated successfully!')
            return redirect(url_for('admin.index'))

        return render_template('admin/edit_section.html', edit_form=edit_form)
    
    @expose('/delete/<int:idx>', methods=('GET', 'POST'))
    @login_required
    def delete_section(self, idx):
        from main import app
        section = Section.query.get_or_404(idx)

        if section.cover_proj:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], section.cover_proj)

            if section.cover_proj in self._image_cache:
                del self._image_cache[section.cover_proj]

            if os.path.exists(file_path):
                os.remove(file_path)


        db.session.delete(section)
        db.session.commit()
        # flash('Doctor deleted successfully!')
        return redirect(url_for('admin.index'))






