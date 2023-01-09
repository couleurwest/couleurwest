# -*- coding: utf-8 -*-

__all__ = ['DBEngine']

import inspect

import couchdb3
from couchdb3 import Document
from dreamtools import dtemng

action = '[wapp.models.couchdb]'


class DBEngine(Document):
    __dbserve = None

    __required__ = None
    __map__ = None
    __server = None
    __indexes__ = []

    __default__ = {}
    __design__ = {}

    _instance = None
    _ddoc = ''
    _dbname = None

    dbname = None
    created = dtemng.dtets()
    updated = created

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            if DBEngine.__server is None and 'server' in kwargs:
                DBEngine.__server = kwargs.pop('server')

            if cls.dbname is None and cls._dbname is not None and 'pfx' in kwargs:
                pfx = kwargs.pop('pfx')
                cls.dbname = f'{pfx}{cls._dbname}'
                cls._ddoc = f"design{cls._dbname.capitalize()}"

                if cls.__design__:
                    cls.__design__.update(ddoc=cls._ddoc)

                with couchdb3.Server(DBEngine.__server) as client:
                    if cls.dbname not in client:
                        db = client.create(cls.dbname)

                        db.put_design(**cls.__design__)
                        for idx in cls.__indexes__:
                            db.save_index(**idx)

            cls._instance = super(DBEngine, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __enter__(self):
        self.__cnx = couchdb3.Server(DBEngine.__server)
        return self.__cnx.get(self.dbname)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cnx.session.close()
        self.__cnx = None


    def save_me(self, **dc):
        """Save and return document"""
        with self as db:
            self.update(updated=dtemng.dtets(),**dc)
            return db.save(self)


    @classmethod
    def all_document(cls):
        with cls() as db:
            result = None

            dcm = db.all_docs(include_docs=True)
            if dcm.total_rows > 0:
                result = list(map(lambda dc: db.get(dc.id), filter(lambda dc: '_design' not in dc.id, dcm.rows)))

            return result

    @classmethod
    def all_docid(cls):
        with cls() as db:
            dcm = db.all_docs()
            return list(map(lambda dc: dc.id, filter(lambda dc: '_design' not in dc.id, dcm.rows)))

    def update_me(self, **dc):
        """Save and return document"""
        with self as db:
            self.updated = dtemng.dtets()
            dc.update(**dc)
            return db.save(dc)

    @classmethod
    def insert_one_document(cls, **dc):
        """Save and return document"""
        with cls() as db:
            dcm = cls().__default__.copy()

            dcm['created'] = dtemng.dtets()
            dcm['updated'] = dcm['created'] = dtemng.dtets()
            dcm.update(**dc)

            uuid, result, rev = db.create(dcm)

        return uuid

    @classmethod
    def update_or_insert(cls, uuid, **doc):
        dcm = cls.load_document(uuid) if uuid is not None else None
        if dcm:
            dcm.save_me(**doc)
            return dcm
        else:
            return cls.insert_one_document(id=uuid, **doc)
    @classmethod
    def update_one_document(cls, uuid, **newDoc):
        """Save and rettur document"""
        oldDoc = None

        with cls() as db:
            if uuid in db:
                oldDoc = cls(db.get(uuid))
                oldDoc.update(updated=dtemng.dtets(), **newDoc)

                return db.save(oldDoc)

        return oldDoc



    @classmethod
    def find_documents(cls, where, **kwargs):
        """Récupération d'un document
        selector: Dict, limit: int = 25,
         skip: int = 0,
         sort: List[Dict] = None,
         fields: List[str] = None,
         use_index: Union[str, List[str]] = None,
         conflicts: bool = False, r: int = 1,
          bookmark: str = None, update: bool = True,
          stable: bool = None, execution_stats: bool = False
        """
        with cls() as db:
            doc = db.find(where, **kwargs)
            return list(map(lambda dc: cls(**dc), doc['docs']))

    @classmethod
    def find_one_document(cls, **where):
        dcm = cls.find_documents(where, limit=1)
        if len(dcm) == 1:
            return dcm[0]

        return None

    @classmethod
    def find_last_one (cls, where, **kwargs):
        return  cls.find_documents( where, sort=[{'codeapp':'desc'}], limit=1, **kwargs)

    @classmethod
    def delete_one_document(cls, uuid) -> bool:
        """Supression d'un document grace à son id

        :param uuid: login document à supprimer
        :return bool: True or False | None id inexistant
        """
        result = None
        with cls() as db:
            if uuid in db:
                result = db.delete(docid=uuid, rev=db.rev(uuid))

        return result

    @classmethod
    def delete_db(cls):
        with cls() as db:
            dcm = db.all_docs(include_docs=True)
            for row in dcm.rows:
                if row['id'].startswith('_'):
                    continue
                doc = row['doc']
                doc['_deleted'] = True

                db.save (doc)

    @classmethod
    def load_document(cls, uuid):
        """Récupération document à partir de son id
        :param uuid: login du document recherché
        :rtype: DBEngine
        """
        result = None
        with cls() as db:
            if uuid in db:
                result = cls(db.get(uuid))
        return result

    @classmethod
    def execute_view(cls, views, **kwargs):
        """Save and return document"""
        with cls() as db:
            results = db.view(cls._ddoc, views, **kwargs)
            if results.total_rows > 0:
                return [cls(doc) for doc in results.rows]
        return []

    @classmethod
    def like_code (cls, reference):
        """Save and rettur id"""
        mango =  {'code': {"$regex": f"^{reference}.*"}} #"" #, 'fields': ['title']
        return cls.find_documents(mango)


    @classmethod
    def from_dict(cls, **document):
        return cls(**{
            k : v for k,v in document.items() if k in inspect.signature(cls).parameters })

    @classmethod
    def update_document(cls, filtre, **docs):
        dcm = cls.find_documents(filtre)

        for row in dcm:
            row.save_me(**docs)