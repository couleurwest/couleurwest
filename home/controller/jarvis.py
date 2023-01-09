# -*- coding: utf-8 -*-
#

from dreamtools.logmng import CTracker, CError


class CJarvis(CTracker):
    pass

class Error(CError):
    """Base class for exceptions in this module."""
    pass

class AuthError(CError):
    """Exception raised for errors when user exist but check with bad password.
    """

    def __init__(self, message="Mauvaise authentification login/mot de passe", status=406, title='ERREUR Authentification'):
        super(AuthError, self).__init__(message, status, title)

class UExistException(CError):
    """Exception raised for errors when user exist with good password.
    """

    def __init__(self, message="Compte existant", status=403, title='Validation compte'):
        super(UExistException, self).__init__(message, status, title)

