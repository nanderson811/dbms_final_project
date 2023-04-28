
import mariadb
import sys


# class for managing connections and calls to the database
class Database:
    def __init__(self, username, password, host, port, db):
        self.__username = username
        self.__password = password
        self.__host = host
        self.__port = port
        self.__db = db
        try:
            # Connect to the database
            self.__conn = mariadb.connect(
                user=self.__username,
                password=self.__password,
                host=self.__host,
                port=self.__port,
                database=self.__db
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            sys.exit(1)

    # calls a stored procedure and returns a list of the results
    # where procname is the name of the stored procedure, and args is the
    # parameters/arguments
    def callProcedure(self, procname, args):
        cursor = self.__conn.cursor()

        cursor.callproc(procname, args)

        results = cursor.fetchall()
        cursor.close()
        return results

    # calls an SQL statement and returns a list of the results
    def execStatement(self, statement):
        cursor = self.__conn.cursor()

        cursor.execute(statement)

        results = cursor.fetchall()
        cursor.close()
        return results
