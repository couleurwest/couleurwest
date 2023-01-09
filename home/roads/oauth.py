from functools import wraps

import flask
import requests
from werkzeug.security import gen_salt

from home.controller.constantes import Constantine
from home.mdl.db_user import DBUser

OAUTH_CODE = 'authorization_code'
OAUTH_PWD = 'password'

def is_authenticated(f):
   @wraps(f)
   def decorator(jwt=None, *args, **kwargs):

      token = None

      if 'x-access-tokens' in flask.request.headers:
         token = flask.request.headers['x-access-tokens']

      if not token:
         return flask.jsonify({'message': 'a valid token is missing'})

      try:
         data = jwt.decode(token, Constantine.SECRET_KEY)
         current_user = DBUser.find_one_document(public_id=data['public_id'])
      except:
          return flask.jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator
def token_required(f):
   @wraps(f)
   def decorator(jwt=None, *args, **kwargs):

      token = None

      if 'x-access-tokens' in flask.request.headers:
         token = flask.request.headers['x-access-tokens']

      if not token:
         return flask.jsonify({'message': 'a valid token is missing'})

      try:
         data = jwt.decode(token, Constantine.SECRET_KEY)
         current_user = DBUser.find_one_document(public_id=data['public_id'])
      except:
          return flask.jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator

def code_token(code):
    r = requests.post(
        Constantine.ACCESS_URI['uri_access_token'],
        headers=Constantine.CONTENT_TYPE,
        auth=(Constantine.OAUTH_CLIENT_ID, Constantine.OAUTH_CLIENT_SECRET),
        json={'authorization_code': code, 'grant_type': OAUTH_CODE})

    if r.ok:
        return r.json()

    return flask.abort(r.status_code)

def autorize():
    code_verifier = gen_salt(24)
    r = requests.post(Constantine.ACCESS_URI['uri_access_authorize'],
                      headers=Constantine.CONTENT_TYPE,
                      auth=(Constantine.OAUTH_CLIENT_ID, Constantine.OAUTH_CLIENT_SECRET),
                      json=
                      {'scopes': ['oauthapp'],  # todo wwwproject
                       'grant_type': OAUTH_CODE,
                       'state': code_verifier})
    if r.ok:
        dcm = r.json()
        if dcm['code_verifier'] == code_verifier:
            code = dcm['code']
            return code_token(code)

    return flask.abort(r.status_code)

def register(access_token, token_type, account):
    r = requests.post(
        Constantine.ACCESS_URI['uri_access_register'],
        headers={
            "Authorization": f"{token_type} {access_token}",
            "X-CLIENT": Constantine.OAUTH_CLIENT_ID},
        json=account)

    if r.ok:
        return r.json()

    return None
    # ClientOauthUser.access_token = dcm['access_token']
    # ClientOauthUser.expires_in = dcm['expires_in']
    # ClientOauthUser.refresh_token = dcm['refresh_token']
    # ClientOauthUser.token_type = dcm['token_type']


def auth(access_token, token_type, account):
    r = requests.post(
        Constantine.ACCESS_URI['uri_access_user'],
        headers= {
            "Authorization": f"{token_type} {access_token}",
            "X-CLIENT": Constantine.OAUTH_CLIENT_ID},
        json=account)

    if r.ok:
        return r.json()
    return None
