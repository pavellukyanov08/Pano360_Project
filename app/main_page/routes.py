from flask import render_template, Blueprint, send_from_directory, url_for
from ..admin.models import Section

# main_page = Blueprint('main_page', __name__)

class MainPage:
    def __init__(self, app):
        self.app = app
        self.main_page = Blueprint('main_page', __name__)
        self._register_routes()

    def _register_routes(self):
        self.main_page.add_url_rule('/uploads/<filename>', 'get_image', self.get_image)
        self.main_page.add_url_rule('/main', 'main', self.main)

    def get_image(self, filename):
        print(f'Изображение (get_image)={filename}')
        return send_from_directory('static/uploads', filename)

    # @main_page.route('/main')
    def main(self):
        sections = Section.query.all()
        print(f'Разделы: {sections}')

        return render_template('main_page/main_page.html', sections=sections)



