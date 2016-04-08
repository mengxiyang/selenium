from libs.mysql import connector
from com.ericsson.xn.commons import test_logger as test

class PyMysql:
    def __init__(self):
        self.conn = None
        pass

    def newConnection(self,host,user,passwd,defaultdb):
        try:
            self.conn = connector.connect(user=user, password = passwd, host = host, database=defaultdb)
        except Exception as e:
            test.info(e.msg)

    def closeConnection(self):
        self.conn.close()

    def query(self,sqltext,mode="one"):
        if self.conn == None:
            test.error("will exit for DB connection Failure")
        else:
            cursor = self.conn.cursor()
            cursor.execute(sqltext)
            if mode=="one":
                result = cursor.fetchone()
            elif mode == "all":
                result = cursor.fetchall()
            else:
                test.error("query mode error")
            cursor.close()
        return (cursor.rowcount,result)

    def execute(self,sqltext):
        if self.conn == None:
            test.error("will exit for DB connection Failure")
        else:
            cursor = self.conn.cursor()
            cursor.execute(sqltext)
            cursor.close()
            self.conn.commit()









