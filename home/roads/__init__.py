import flask
from dreamtools import tools
from dreamtools.cfgmng import CFGBases
from flask import Blueprint
from flask import render_template, send_from_directory

bp = Blueprint('home', __name__, url_prefix="/")

def has_no_empty_params(rule):
    """

    :param rule:
    :return:
    """
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(tools.APP_DIR, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@bp.route('/logo')
def logo():
    return send_from_directory(tools.APP_DIR, 'logo.png', mimetype='image/vnd.microsoft.icon')


@bp.route('/', methods=["GET"])
def index():
    """
    :return:
    """
    p = CFGBases.loadingbyref('content')
    return render_template("home/index.html", title="Couleur West I.T", page=p)
