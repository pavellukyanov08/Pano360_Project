from flask import render_template, Blueprint
from ..admin.models import Section

main_page = Blueprint('main_page', __name__)

class MainPage:
    @staticmethod
    @main_page.route('/main')
    def index():
        sections = Section.query.all()

        return render_template('main_page/main_page.html', sections=sections)


