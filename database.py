
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

    def add_to_crime(self, cid, dateoccurred, arrestmade, isdomestic, primarytype, xcoordinate, ycoordinate):

        cursor = self.__conn.cursor()

        sql = "INSERT INTO Crime (id, dateOccurred, arrestMade, isDomestic, primaryType, xCoordinate, yCoordinate) " \
              "VALUES (?, ?, ?, ?, ?, ?, ?);"

        values = (cid, dateoccurred, arrestmade, isdomestic, primarytype, xcoordinate, ycoordinate)
        exists = self.execStatement(f"SELECT * FROM Crime WHERE id={cid}")
        if not exists:
            cursor.execute(sql, values)
        else:
            values = (dateoccurred, arrestmade, isdomestic, primarytype, xcoordinate, ycoordinate)
            sql = "UPDATE Crime SET dateOccurred=?, arrestMade=?, isDomestic=?, primaryType=?, xCoordinate=?, " \
                  "yCoordinate=? WHERE id="+str(cid)
            cursor.execute(sql, values)

        self.__conn.commit()
        cursor.close()

    def add_to_case(self, casenum, casedesc, dateupdated):

        cursor = self.__conn.cursor()

        sql = "INSERT INTO CrimeCase (caseNumber, caseDesc, dateUpdated) " \
              "VALUES (?, ?, ?);"

        values = (casenum, casedesc, dateupdated)
        exists = self.execStatement(f"SELECT * FROM CrimeCase WHERE caseNumber=\'{casenum}\'")
        if not exists:
            cursor.execute(sql, values)
        else:
            values = (casedesc, dateupdated)
            sql = "UPDATE CrimeCase SET caseDesc=?, dateUpdated=? " \
                  "WHERE caseNumber=\'"+str(casenum)+"\'"
            cursor.execute(sql, values)

        self.__conn.commit()
        cursor.close()

    def add_to_location(self, xc, yc, lac, loc, loctype, beatid):

        cursor = self.__conn.cursor()

        sql = "INSERT INTO Location (xCoordinate, yCoordinate, latCoordinate, longCoordinate, locationType, beatID) " \
              "VALUES (?, ?, ?, ?, ?, ?);"

        values = (xc, yc, lac, loc, loctype, beatid)
        exists = self.execStatement(f"SELECT * FROM Location WHERE xCoordinate={xc} AND yCoordinate={yc};")
        if not exists:
            cursor.execute(sql, values)
        else:
            values = (lac, loc, loctype, beatid)
            sql = "UPDATE Location SET latCoordinate=?, longCoordinate=?, locationType=?, beatID=? " \
                  "yCoordinate=? WHERE xCoordinate="+str(xc)+" AND yCoordinate="+str(yc)+";"
            cursor.execute(sql, values)

        self.__conn.commit()
        cursor.close()

    def add_to_beat(self, beatid, districtid):

        cursor = self.__conn.cursor()

        sql = "INSERT INTO Beat (beatID, district) " \
              "VALUES (?, ?);"

        values = (beatid, districtid)
        exists = self.execStatement(f"SELECT * FROM Beat WHERE beatID={beatid};")
        if not exists:
            cursor.execute(sql, values)
        else:
            values = (districtid, )
            sql = "UPDATE Beat SET district=? " \
                  "WHERE beatID="+str(beatid)+";"
            cursor.execute(sql, values)

        self.__conn.commit()
        cursor.close()

    def add_to_isincase(self, cid, casenum):

        cursor = self.__conn.cursor()

        sql = "INSERT INTO IsInCase (id, caseNumber) " \
              "VALUES (?, ?);"

        values = (cid, casenum)
        exists = self.execStatement(f"SELECT * FROM IsInCase WHERE id={cid};")
        if not exists:
            cursor.execute(sql, values)
        else:
            values = (casenum, )
            sql = "UPDATE IsInCase SET caseNumber=? " \
                  "WHERE id="+str(cid)+";"
            cursor.execute(sql, values)

        self.__conn.commit()
        cursor.close()

    def delete_from_isincase(self, cid):
        cursor = self.__conn.cursor()
        sql = f"DELETE FROM IsInCase WHERE id={cid};"

        exists = self.execStatement(f"SELECT * FROM IsInCase WHERE id={cid};")
        print(exists)
        if exists:
            cursor.execute(sql)
        else:
            return "Item not found"

        self.__conn.commit()
        cursor.close()
        return "Item Deleted"

    def delete_from_beat(self, beatid):
        cursor = self.__conn.cursor()
        sql = f"DELETE FROM Beat WHERE beatID={beatid};"

        exists = self.execStatement(f"SELECT * FROM Beat WHERE beatID={beatid};")
        print(exists)
        if exists:
            cursor.execute(sql)
        else:
            return "Item not found"

        self.__conn.commit()
        cursor.close()
        return "Item Deleted"

    def delete_from_location(self, xc, yc):
        cursor = self.__conn.cursor()
        sql = f"DELETE FROM Location WHERE xCoordinate={xc} AND yCoordinate={yc};"

        exists = self.execStatement(f"SELECT * FROM Location WHERE xCoordinate={xc} AND yCoordinate={yc};")
        print(exists)
        if exists:
            cursor.execute(sql)
        else:
            return "Item not found"

        self.__conn.commit()
        cursor.close()
        return "Item Deleted"

    def delete_from_case(self, casenum):
        cursor = self.__conn.cursor()
        sql = "DELETE FROM CrimeCase WHERE caseNumber=\'"+str(casenum)+"\';"

        exists = self.execStatement(f"SELECT * FROM CrimeCase WHERE caseNumber=\'{casenum}\'")
        print(exists)
        if exists:
            cursor.execute(sql)
        else:
            return "Item not found"

        self.__conn.commit()
        cursor.close()
        return "Item Deleted"

    def delete_from_crime(self, cid):
        cursor = self.__conn.cursor()
        sql = "DELETE FROM Crime WHERE id="+str(cid)+";"

        exists = self.execStatement(f"SELECT * FROM Crime WHERE id={cid}")
        print(exists)
        if exists:
            cursor.execute(sql)
        else:
            return "Item not found"

        self.__conn.commit()
        cursor.close()
        return "Item Deleted"
