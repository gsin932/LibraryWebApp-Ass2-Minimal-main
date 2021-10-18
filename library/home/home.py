from flask import Blueprint, render_template

from library.utilities import utilities

# Configure Blueprint.
home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        daily_pick_book=utilities.get_daily_pick()
    )
