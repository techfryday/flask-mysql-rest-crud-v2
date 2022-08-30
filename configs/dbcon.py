import mysql.connector
from configs.config import dbconfig

class dbcon():
    __dbcon = None
    def __init__(self):
        if self.__dbcon!=None:
            raise Exception("This Class is a Singleton!")
        else:
            self.__dbcon = self
    
    def connect(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)
        return self.cur
