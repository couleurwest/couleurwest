#!/usr/bin/python3
# -*- coding: utf-8 -*-
# cw/__init__.py

"""Ma page WEB"""
import os

from dreamtools import tools, profiler, config, dtemng
from flask import Flask

__author__ = "[Dreamgeeker] Ketsia LENTIN"
__copyright__ = "Copyright 2019, Les couleurs de l'ouest"
__credits__ = ["Ketsia LENTIN"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "dreamgeeker"
__email__ = "dreamgeeker@couleurwest-it.com"
__status__ = "Developement"

from flask_ckeditor import CKEditor
from flask_login import LoginManager

from flask_simple_captcha import CAPTCHA
from flask_wtf import CSRFProtect

from home.controller import RequestProjetsConverter, constantes
from home.controller.constantes import Constantine, CDirectories
from home.controller.encrypt_file import cryptofile
from home.controller.jarvis import CJarvis

os.environ['TZ'] = 'America/Cayenne'  # set new timezone
csrf = CSRFProtect()
login_manager = LoginManager()

captcha = CAPTCHA({'SECRET_CAPTCHA_KEY': os.getenv('SECRET_CAPTCHA_KEY')})
ckeditor = CKEditor()

#app.instance_path = os.path.abspath(os.path.join(tools.PROJECT_DIR, '../instance'))

"""configuration des chemins d'accès"""


def create_app():
    action = '[config] Initialisation systemes'
    print(f"---- {action}----")

    app = Flask(__name__)
    app.config.from_object('config.CConfig')
    app.config['CKEDITOR_PKG_TYPE'] = 'basic'
    app.template_folder = profiler.path_build(tools.PROJECT_DIR, 'templates')
    app.static_folder = profiler.path_build(tools.PROJECT_DIR, 'static')
    app.url_map.converters.update(request_projets=RequestProjetsConverter)

    csrf.init_app(app)
    captcha.init_app(app)
    ckeditor.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"
    mode = os.getenv("FLASK_ENV").lower()
    config.CConfig("couleurwest", mode)

    Constantine.DIRECTORIES = CDirectories(tools.PROJECT_DIR)
    Constantine.MASTER_PWD = os.getenv("SUPERPASS")
    Constantine.SECRET_SALT = os.getenv("SECRET_SALT")
    Constantine.SECRET_KEY = os.getenv("SECRET_KEY")
    Constantine.ACCESS_URI = constantes.ACCESS[mode]
    Constantine.OAUTH_CLIENT_ID = os.getenv("OAUTH_CLIENT_ID")
    Constantine.OAUTH_CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")

    CJarvis.info_tracking("Initialisation filtres Jinja", "[pm] CREATE_APP")
    cryptofile.KEY = os.getenv("CRYPT_KEY")

    # from quizz.mdl import DBRouter
    # DBRouter.DB_SERVER = os.getenv("DB_SERVER")
    # DBRouter.PREFIX_DB = os.getenv("PREFIX_DB") or ''

    @app.template_global
    def experience():
        return int(dtemng.today("YYYY")) - 1999


    @login_manager.user_loader
    def load_user(uuid):
        pass

    from home.roads import bp as bph
    app.register_blueprint(bph)

    from home.roads.wwwproject import bp as bpe
    app.register_blueprint(bpe)

    return app