from database.DB_connect import DBConnect
from model.NODO import Nodo
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getter_estremi_lat():
        """
        :return:
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select min(s.latitude), max(s.latitude)
                        from sighting s """
            cursor.execute(query)
            for row in cursor:
                result = row #row è una tupla contenente lat inf, lat sup
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_estremi_long():
        """
        :return:
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select min(s.longitude), max(s.longitude)
                            from sighting s """
            cursor.execute(query)
            for row in cursor:
                result = row  # row è una tupla contenente long inf, long sup
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_shapes():
        """
        :return: lista di tuple contenenti gli attributi selezionati dalla query
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select distinct shape
                        from sighting s 
                        where shape is not null
                        order by shape desc
                    """
            cursor.execute(query)
            for row in cursor:
                result.append(row[0]) #row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_nodes(minLat, minLong, shape):
        """
        usa unpacking di dizionari per creare oggetti di classe avente tutte le righe di data tabella
        return: mappa key= id, value= oggetto
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor(dictionary=True)
            query = """select s.state, sum(s.duration) as 'pesoNodo'
                        from sighting s, state st 
                        where st.lat > %s
                        and st.lng > %s
                        and s.shape = %s
                        and s.state = st.id
                        group by s.state 
                        """
            cursor.execute(query, (minLat, minLong, shape))
            for row in cursor:
                result.append(Nodo(**row))  #**row è un operatore di unpacking (espansione) di un dizionario. nb: serve che tutti i nomi degli attributi combacino
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_confini():
        """
        :return: lista di tuple contenenti gli attributi selezionati dalla query
        """
        conn = DBConnect.get_connection()
        result = []
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor()
            query = """select *
                            from neighbor n """
            cursor.execute(query)
            for row in cursor:
                result.append(row)  # row è una tupla contenente tutti gli attributi selezionati dalla query
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def getter_idMapState():
        """
        usa unpacking di dizionari per creare oggetti di classe avente tutte le righe di data tabella
        return: mappa key= id, value= oggetto
        """
        conn = DBConnect.get_connection()
        result = {}
        if conn is None:
            print("Connection failed")
        else:
            cursor = conn.cursor(dictionary=True)
            query = """select *
                        from state s
                        """
            cursor.execute(query)
            for row in cursor:
                result[row["id"].lower()] = (State(**row))  # **row è un operatore di unpacking (espansione) di un dizionario. nb: serve che tutti i nomi degli attributi combacino
            cursor.close()
            conn.close()
        return result


if __name__ == '__main__':
    for c in DAO.getter_confini():
        print(c)

