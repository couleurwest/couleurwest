import dataclasses

from dreamtools import profiler


@dataclasses.dataclass
class CDirectories:
    projet: str
    app: str = dataclasses.field(init=False)
    pics: str = dataclasses.field(init=False)
    registar: str = dataclasses.field(init=False)
    calendar: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.app = profiler.path_build(self.projet, "pm")
        self.pics = profiler.path_build(self.projet, 'static/pics')
        self.registar = profiler.path_build(self.projet, 'static/registar')
        self.calendar = profiler.path_build(self.registar, 'calendar.yml')
        self.quizz_import = profiler.path_build(self.projet, 'static/sources/question.yml')

        profiler.makedirs(self.registar)


class Constantine:
    DIRECTORIES: CDirectories
    ACCESS_URI = None
    MASTER_PWD: str
    QUIZZ_CATEGORIES = {
        "avis": [(0, "Négatif"), (3, "Plutot négatif"), (5, "Neutre"), (7, "Plutot positif"), (10, "Très positif")],
        "eval": (1, 11),
        "word": 3
    }
    URIS_HOSTS_ALLOWED = []
    URIS_REQUIRED_HTTPS = False
    SECRET_SALT = None
    SECRET_KEY = None
    CONTENT_TYPE= {'Content-Type': "application/json"}
    OAUTH_CLIENT_ID = None
    OAUTH_CLIENT_SECRET = None


ACCESS = {
    'development': {
        'uri_access_authorize': 'http://kuratoro.3p0.net:5000/authorize',
        'uri_access_token': 'http://kuratoro.3p0.net:5000/access_token',
        'uri_access_register': 'http://kuratoro.3p0.net:5000/register',
        'uri_access_user': 'http://kuratoro.3p0.net:5000/access'
    },
    'production': {
        'uri_access_authorize': 'https://kuratoro.3p0.net/authorize',
        'uri_access_token': 'https://kuratoro.3p0.net/access_token',
        'uri_access_register': 'https://kuratoro.3p0.net/register',
        'uri_access_user': 'https://kuratoro.3p0.net/access'
    }
}

FLASH_MESSAGE = {
    'ERR_FORM': ("""<h5>Formulaire non valide<br/><small class:"text-alert">Vérifier saisie</small></h5>""", 'alert'),
    'ERR_CAPTCHA': ('<h5>ERREUR CAPTCHA</h5>', "warning"),
    'ERR_USER_NOT_FOUND': (
        '<h5>ERREUR IDENTIFICATION<br/><small class:"text-warning">Les informations fournies ne permettent pas de vous identifier</small></h5>',
        "warning"),
    "ACTION_SUCCESS": ('<h5>Opération effectuée avec succès</h5>', "success"),
    'REC_OK': ('<h5>Enregistrement effectué</h5>', "success"),
    'CODE_SENT': (
        '<h5>CODE DE VALIDATION<br/><small>Un code vous a été envoyé dans votre boite électronique; N\'hésitez pas à vérifier vos indésirables (spams)</h5>',
        "success"),
    'ERR_CODE_AUTH': ('<h5>ERREUR CODE<br/><small class:"text-warning">Le code indiqué</h5>', "warning"),
    'ERR_SYS': (
        "<h5>ERREUR SYSTEME<br/><small class:'text-alert'>Raffraichir la page et réintérer l'operation<br/>Si l'erreur persiste contactez votre administrateur</small>",
        "alert")
}
