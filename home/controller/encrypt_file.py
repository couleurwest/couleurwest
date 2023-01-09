from cryptography.fernet import Fernet
from dreamtools import profiler


class cryptofile:
    KEY = None  # key = Fernet.generate_key()
    DIR_DST = ".sources"

    @classmethod
    def encrypt(cls, df, nf):
        """Cryptage d'un fichier

        Parametres
        ============================
        :param str df: données à cryptées
        :param str df: nom du fichiers
        """

        # encrypting the file
        b_df = str.encode(df, "utf-8")
        fp = profiler.path_build(cls.DIR_DST, nf)

        fernet = Fernet(cls.KEY)
        encrypted = fernet.encrypt(b_df)
        with open(fp, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

    @classmethod
    def decrypt(cls, nf):
        """Chargement d'un fichier et decryptage du contenu

        Parametres
        ============================
        :param any df: données à cryptées
        :param str df: nom du fichiers
        """
        fp = profiler.path_build(cls.DIR_DST, nf)
        if profiler.file_exists(fp):
            fernet = Fernet(cls.KEY)

            with open(fp, 'rb') as enc_file:
                encrypted = enc_file.read()
                df = fernet.decrypt(encrypted)
                return df.decode("utf-8")

        return None
