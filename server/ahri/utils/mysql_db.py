import pymysql
from ahri.settings import MYSQL_DB


class DB:
    def __init__(self, host=MYSQL_DB['host'], port=MYSQL_DB['port'], user=MYSQL_DB['user'], passwd=MYSQL_DB['pass'],
                 dbname=MYSQL_DB['db']):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.conn = self.connection()

    def connection(self):
        # conn = pymysql.connect(self.host, self.user, self.passwd)
        connection = pymysql.connect(host='111.67.206.108',
                                     user='root',
                                     password='Aa12345!',
                                     db='mysql',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection

    def addUser(self, username, passwd):
        cur = self.conn.cursor()
        res = cur.execute("CREATE USER '" + username + "'@'%' IDENTIFIED BY '" + passwd + "'")
        return res

    def subUser(self, username):
        cur = self.conn.cursor()
        res = cur.execute("delete from user where user='" + username + "'")
        res = cur.execute("flush privileges")
        return res

    def grant(self, dbname, username):
        cur = self.conn.cursor()
        res = cur.execute("GRANT ALL ON " + username + '_' + dbname + ".* TO '" + username + "'@'%'")
        res = cur.execute("flush privileges")
        return res

    def createDb(self, user, dbname):
        cur = self.conn.cursor()
        res = cur.execute('create database if not exists ' + user + '_' + dbname)
        return res

    def dropDb(self, dbname):
        cur = self.conn.cursor()
        res = cur.execute('drop database ' + dbname)
        return res

    def databases(self):
        cur = self.conn.cursor()
        cur.execute("show databases")
        res = cur.fetchall()
        list = []
        for i in res:
            # print(type(i), i)
            if i['Database'] == 'information_schema' and self.user != 'root':
                pass
            else:
                list.append(i['Database'])
        return list

    def createTable(self, dbname, tbname):
        cur = self.conn.cursor()
        cur.execute("USE " + dbname)
        cur.execute("drop table if exists " + tbname)
        sql = """CREATE TABLE """ + tbname + """ (
                 FIRST_NAME  CHAR(20) NOT NULL,
                 LAST_NAME  CHAR(20),
                 AGE INT,  
                 SEX CHAR(1),
                 INCOME FLOAT )"""
        res = cur.execute(sql)
        return res


if __name__ == '__main__':
    # db = DB('111.67.206.108', 'root', 'Aa12345!', 'mysql')
    db = DB('111.67.206.108', 'ahri', '123456', 'mysql')
    # res = db.createDb('ahri', 'test')
    res = db.createTable('ahri_test', 'tb')
    # res = db.grant('test', 'ahri')
    # res = db.databases()
    # res = db.addUser('ahri', '123456')
    # res = db.subUser('ahri')
    print(res)
