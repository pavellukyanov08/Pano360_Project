from collections import OrderedDict

from flask import url_for

from app.admin.models import Section


class Breadcrumb:
    @staticmethod
    def generate_breadcrumbs(section_id):
        section = Section.query.get(section_id)

        breadcrumbs = [
            {'name': 'Раздел панорам', 'url': url_for('admin.index')},
            {'name': section.title, 'url': url_for('projects.projects', slug=section.slug)},
            # {'name': 'Библиотека раздела', 'url': url_for('projects.section_library', slug=section.slug)}
        ]

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