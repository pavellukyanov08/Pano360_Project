from collections import OrderedDict

from flask import url_for

from app.admin.models import Section, Season, Panorama, Project


class Breadcrumb:
    @staticmethod
    def generate_breadcrumbs(section_id=None, project_id=None):
        # Начальные хлебные крошки с главной страницей
        breadcrumbs = [
            {'name': 'Главная', 'url': url_for('admin.index')},  # Главная страница админ-панели
        ]

        # Если передан section_id, добавляем информацию о разделе
        if section_id:
            section = Section.query.get(section_id)
            breadcrumbs.append(
                {'name': 'Раздел панорам', 'url': url_for('admin.index')}  # Это можно изменить для конкретной страницы разделов
            )
            breadcrumbs.append(
                {'name': section.title, 'url': url_for('projects.projects', slug=section.slug, season='Лето', project=project)}
            )

        # Если передан project_id, добавляем информацию о проекте
        if project_id:
            project = Project.query.get(project_id)
            breadcrumbs.append(
                {'name': project.title, 'url': url_for('projects.project_detail', project_id=project.id)}
            )

        return breadcrumbs


class ImageCache:
    _image_cache = OrderedDict()
    _cache_limit = 100
    @staticmethod
    def allowed_file(filename):
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def get_image(filename):
        if not filename:
            # return url_for('static', filename=os.path.join('uploads', filename))
            return None

        if filename in ImageCache._image_cache:
            ImageCache._image_cache.move_to_end(filename)
        else:
            if len(ImageCache._image_cache) > ImageCache._cache_limit:
                ImageCache._image_cache.popitem(last=False)

            # Добавление нового элемента в кэш
            ImageCache._image_cache[filename] = url_for('static', filename=f'uploads/{filename}')
        return ImageCache._image_cache[filename]


    def clear_cache(self):
        self._image_cache.clear()