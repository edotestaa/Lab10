from database.DB_connect import DBConnect
from model.filiale import Filiale


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """

    @staticmethod
    def read_all_filiali():
        conn = DBConnect.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("""SELECT *
                                  FROM filiale""")
                result = []
                for row in cursor:
                    filiale = Filiale(row["id"], row["codice"], row["nome"], row["citta"], row["provincia"], row["latitudine"], row["longitudine"])
                    result.append(filiale)
                return result
            finally:
                cursor.close()
        finally:
            conn.close()

    @staticmethod
    def get_collegamenti():
        conn = DBConnect.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("""SELECT 
                                  LEAST(id_filiale_origine, id_filiale_destinazione) AS f1,
                                  GREATEST(id_filiale_origine, id_filiale_destinazione) AS f2,
                                  SUM(importo) AS somma_importi,
                                  COUNT(*) AS num_bonifici
                                  FROM bonifico
                                  WHERE id_filiale_origine <> id_filiale_destinazione
                                  GROUP BY f1, f2""")
                result = []
                for row in cursor:
                    result.append((
                        row["f1"],
                        row["f2"],
                        float(row["somma_importi"]),
                        int(row["num_bonifici"])
                    ))
                return result
            finally:
                cursor.close()
        finally:
            conn.close()