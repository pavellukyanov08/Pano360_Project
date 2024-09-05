import os
from flask_admin import AdminIndexView, expose, BaseView
from flask_login import login_required
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for


from app.auth.models import User
from .forms import SectionForm, ProjectForm, PanoramaForm
from .models import Section, Project, Panorama
from ..config import db
from .utils import Breadcrumb, ImageCache


class MainAdminPage(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        current_user = User.query.first()
        sections = Section.query.all()

        nums_projects = Section.query.count()


        for section in sections:
            section.image_url = ImageCache.get_image(section.cover_proj)

        return self.render('admin/index.html', user=current_user, sections=sections, num_projects=nums_projects)


    @expose('/add/', methods=('GET', 'POST'))
    @login_required
    def add_section(self):
        from main import app

        add_section = SectionForm()

        if add_section.validate_on_submit():
            title = add_section.title.data
            description = add_section.description.data
            sort_in_list = add_section.sort_in_list.data
            cover_proj = add_section.cover_proj.data

            if cover_proj and ImageCache.allowed_file(cover_proj.filename):
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

        return render_template('admin/add_section.html', add_section=add_section)

    @expose('/share/<int:section_id>/', methods=('GET', 'POST'))
    @login_required
    def share_section(self, section_id):
        pass

    @expose('/edit/<int:section_id>', methods=('GET', 'POST'))
    @login_required
    def edit_section(self, section_id):
        section = Section.query.get_or_404(section_id)
        edit_form = SectionForm(obj=section)

        if edit_form.validate_on_submit():
            edit_form.populate_obj(section)

            db.session.commit()
            # flash('section updated successfully!')
            return redirect(url_for('admin.index'))

        return render_template('admin/edit_section.html', edit_form=edit_form)
    
    @expose('/delete/<int:section_id>', methods=('GET', 'POST'))
    @login_required
    def delete_section(self, section_id):
        from main import app
        section = Section.query.get_or_404(section_id)

        if section.cover_proj:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], section.cover_proj)

            if section.cover_proj in ImageCache._image_cache:
                del ImageCache._image_cache[section.cover_proj]

            if os.path.exists(file_path):
                os.remove(file_path)


        db.session.delete(section)
        db.session.commit()
        # flash('Doctor deleted successfully!')
        return redirect(url_for('admin.index'))


class ProjectView(BaseView):
    @expose('/')
    @login_required
    def index(self):
        return redirect(url_for('.projects'))

    @expose('/<slug>')
    @login_required
    def projects(self, slug):
        current_user = User.query.first()

        section = Section.query.filter_by(slug=slug).first_or_404()

        projects = Project.query.filter_by(section_id=section.id).all()

        breadcrumbs = Breadcrumb.generate_breadcrumbs(section.id)

        nums_projects = Project.query.count()

        section.image_url = ImageCache.get_image(section.cover_proj)
        for project in projects:
            project.image_url = ImageCache.get_image(project.cover_proj)

        return self.render('admin/section_projects.html', user=current_user,
                           breadcrumbs=breadcrumbs,
                           section=section,
                           projects=projects,
                           num_projects=nums_projects)

    @expose('/view/<int:project_id>')
    @login_required
    def view_project(self, project_id):
        current_user = User.query.first()
        project = Project.query.get_or_404(project_id)

        return self.render('admin/view_project.html', user=current_user, project=project)


    @expose('/section_library/', methods=('GET', 'POST'))
    @login_required
    def section_library(self):
        current_user = User.query.first()
        # breadcrumbs = Breadcrumb.generate_breadcrumbs(current_user.id)

        return self.render('admin/section_library.html', user=current_user)

    @expose('/add/<int:section_id>/', methods=('GET', 'POST'))
    @login_required
    def add_project(self, section_id):
        from main import app

        add_project = ProjectForm()
        section = Section.query.get(section_id)

        if add_project.validate_on_submit():

            # section_id =
            title = add_project.title.data
            location = add_project.location.data
            sort_in_list = add_project.sort_in_list.data
            cover_proj = add_project.cover_proj.data

            # section_id = add_project.section_id.data

            if cover_proj and ImageCache.allowed_file(cover_proj.filename):
                filename = secure_filename(cover_proj.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                cover_proj.save(file_path)

                new_project = Project(
                    title=title,
                    location=location,
                    sort_in_list=sort_in_list,
                    cover_proj=filename,
                    section_id=section_id
                )

                db.session.add(new_project)

                # if section:
                #     section.prpoject_count += 1
                #     db.session.add(section)

                db.session.commit()
            return redirect(url_for('projects.projects', slug=section.slug))

        return render_template('admin/add_project.html', add_project=add_project)

    @expose('/edit/<int:project_id>', methods=('GET', 'POST'))
    @login_required
    def share_project(self, project_id):
        pass


    @expose('/edit/<int:project_id>', methods=('GET', 'POST'))
    @login_required
    def edit_project(self, project_id):
        project = Project.query.get_or_404(project_id)
        edit_form = ProjectForm(obj=project)

        if edit_form.validate_on_submit():
            edit_form.populate_obj(project)

            db.session.commit()
            # flash('section updated successfully!')
            return redirect(url_for('admin.index'))

        return render_template('admin/edit_section.html', edit_form=edit_form)

    @expose('/delete/<int:project_id>', methods=('GET', 'POST'))
    @login_required
    def delete_project(self, project_id):
        from main import app
        section = Section.query.get_or_404(project_id)

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


class PanoramaView(BaseView):
    @expose('/')
    @login_required
    def index(self):
        return redirect(url_for('.panoramas'))

    @expose('/add/<int:project_id>/', methods=('GET', 'POST'))
    @login_required
    def add_panorama(self, project_id):
        from main import app

        add_panorama = PanoramaForm()
        project = Section.query.get(project_id)

        if add_panorama.validate_on_submit():
            title = add_panorama.title.data
            sort_in_list = add_panorama.sort_in_list.data
            cover_proj = add_panorama.cover_proj.data

            # section_id = add_project.section_id.data

            if cover_proj and ImageCache.allowed_file(cover_proj.filename):
                filename = secure_filename(cover_proj.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                cover_proj.save(file_path)

                new_panorama = Panorama(
                    title=title,
                    sort_in_list=sort_in_list,
                    cover_proj=filename,
                    project_id=project_id
                )

                db.session.add(new_panorama)

                # if section:
                #     section.prpoject_count += 1
                #     db.session.add(section)

                db.session.commit()
            return redirect(url_for('projects.projects', slug=project.slug))

        return render_template('admin/add_panorama.html', add_panorama=add_panorama)








