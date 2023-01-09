from copy import copy

import flask
from dreamtools.cfgmng import CFGBases
from flask_login import current_user, login_user

from app import captcha
from home.controller import flash_message, org_login, org_signin, CJarvis
from home.controller.frm.backoff import FLogin, FSignin
from home.mdl.db_user import DBUser
from home.roads import oauth

bp = flask.Blueprint('wwwproject',__name__, url_prefix='/wwwproject')


@bp.route('/access', methods=['GET', 'POST'])
def access():
    """connexion"""
    transformer = None
    recorder = None

    if current_user.is_active:
        next = flask.url_for('home.index')
        return flask.redirect(next)

    if flask.request.method == 'POST':
        request_form = flask.request.form
        # Verification du CAPTCHA
        c_hash = request_form.get('captcha-hash')
        c_text = request_form.get('captcha-text')

        if not captcha.verify(c_text, c_hash):
            flash_message('ERR_CAPTCHA')
        else:
            authorization = oauth.autorize()
            access_token = authorization['access_token']
            token_type = authorization['token_type']

            if 'signin' in flask.request.form:
                mode = 'cnx'
                form = FLogin(flask.request.form)
            else:# 'signup' in flask.request.form:
                mode = 'sin'
                form = FSignin(flask.request.form)

            if form.validate_on_submit():
                data = form.data
                email = data.get['email']

                account = {'username' : email, 'password': data.get['password']}
                user = {'username' : data.get['username']}

                if mode == 'sin':
                    token = oauth.register(access_token, token_type, account)
                    user.update(**token)
                    DBUser.insert_one_document(**user)
                else:
                    token = oauth.auth(access_token, token_type, account)
                    user = DBUser.find_one_document(account_id = token.get('account_id'))
                    user.save_me(**token)

                if token is not None:
                    flask.request.headers.add_header('x-access-token', token['access_token'])

                    next_page = flask.redirect(flask.url_for('check_code'))
                    next_page.headers['x-access-tokens'] = access_token
                    return next_page

            else:
                flash_message('ERR_FORM')

    form_cnx = FLogin()
    form_sin = FSignin()

    cp = captcha.create()
    p = CFGBases.loadingbyref('projets')
    header = p.get('wwwproject')
    main_content = {'uuid': 'access', "image":'', 'title': 'Connexion'}

    return flask.render_template('wwwproject/access.html', form_cnx=form_cnx, form_sin=form_sin,
                                 page="login", captcha=cp, header=header, main_content=main_content, content={})


def load_content (code):
    p = CFGBases.loadingbyref('content')
    main_content = None
    uuid = None
    menu = []
    for page in p.get('index'):
        uuid_current= page.get('uuid')
        if uuid_current is None:
            continue
        elif uuid_current == 'projets':
            for subpage in page.get('submenu'):
                if subpage.get('uuid') == code:
                    main_content = subpage
                else:
                    menu.append(subpage)

    p = CFGBases.loadingbyref('projets')
    header = p.get('wwwproject')
    if main_content:
        for page in p.get('index'):
            uuid_current = page.get('uuid')
            if uuid_current is None or (uuid_current != code):
                continue
            else:
                return flask.render_template(f'wwwproject/pages.html', content=page, menu=menu, main_content=main_content, mode="projets", page=code, header=header)


    return flask.redirect('/')


@bp.route('/<request_projets:page>')
def eservices(page):
    return load_content(page.value)
