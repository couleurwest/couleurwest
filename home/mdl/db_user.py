
__all__ = ['DBUser']

from home.mdl import DBEngine

class DBUser(DBEngine):
    _dbname = "uzanto"

    @property
    def username(self):
        return self.get("username")

    @username.setter
    def username(self, v):
        self.update(username=v)

    @property
    def account_id(self):
        return self.get("account_id")

    @account_id.setter
    def account_id(self, v):
        self.update(account_id=v)


    @property
    def access_token(self):
        return self.get("access_token")

    @access_token.setter
    def access_token(self, v):
        self.update(access_token=v)

    refresh_token = None
    expires_in = None
    token_type = None

    __design__ = {
        "ddoc": "",
        "language": "javascript",
        "views": {
            "find_user": {
                "map": """function(doc) { emit(doc.username, doc)}"""
            }
        },
        "validate_doc_update": """function(newDoc, oldDoc, userCtx) {
            function required (field, msg){
                msg = msg | "Données manquante : " + field;
                if (!newDoc._deleted && !newDoc[field]) throw ({forbidden: msg}); 
            }
            required ("public_id");
        }"""
    }
    __indexes__ = [
        {
            "ddoc": "idxaccount",
            "index": {
                "fields": ["public_id"]
            },
            "name": "idxaccount"
        }]
