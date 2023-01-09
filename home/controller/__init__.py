from dreamtools import tools
from flask import flash
from werkzeug.routing import BaseConverter, ValidationError

from enum import Enum, unique

from home.controller.constantes import FLASH_MESSAGE
from home.controller.jarvis import CJarvis


@unique
class RequestProjets(str, Enum):
    WEBSERVICES = 'webservices'
    ANDRID = 'android'
    STANDALONE = 'standalone'


class RequestProjetsConverter(BaseConverter):

    def to_python(self, value):
        try:
            request_type = RequestProjets(value)
            return request_type
        except ValueError as err:
            raise ValidationError()

    def to_url(self, obj):
        return obj


def flash_message(code):
    """Gestion des messages flash

    :param str code: code du message
        ERR_FORM : Erreur Formulaire / données non valide
    """

    if code in FLASH_MESSAGE:
        return flash(FLASH_MESSAGE[0], FLASH_MESSAGE[1])
    else:
        return flash(f'<h5>Erreur<br/><small class="text-alert">{code}</small></h5>', "alert")


def org_signin(login, email, password, **kwargs):
    """Enregistrement d'un utilisateur "organisateur"
    L'utilisateur se connecte grace à son login et son mot de passe
    Une fois valider, il recoit un code valable 10mn"""

    CJarvis.flag(f"[quizz.ctrl.org_login] NEW_USER {login}")
    uuid = DBUser.insert_user(login, email, password, False)

    if uuid:
        CJarvis.flag(f"[quizz.ctrl.org_signin] CONFIG_USER {login}")
        user = DBUser.get(uuid)
        org_access(user)

        return user
    else:
        raise logmng.CError("ERR_SYS", status=500)


def org_login(login, password, **kwargs):
    """chargement d'un utilisateur "organisateur"
    L'utilisateur se connecte grace à son login et son mot de passe
    Une fois valider, il recoit un code valable 10mn"""

    # Identification utilisateur
    CJarvis.flag(f"[quizz.ctrl.org_login] CHECK_USER {login}")
    user = DBUser.check_user(login, password)

    if user:
        CJarvis.flag(f"[quizz.ctrl.org_login] CONFIG_USER {login}")
        org_access(user)

        return user
    else:
        raise logmng.CError("ERR_USER_NOT_FOUND", status=500)

