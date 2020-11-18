import  os
import pymysql
pymysql.install_as_MySQLdb()
DEBUG = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '10.18.97.60'
PORT = '13306'
DATABASE = 'mobperf'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI  = "mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS =True



#LDAP登录

LDAP_HOST = 'ldap://10.21.137.202:389'
LDAP_BASE_DN = 'cn=Manager,dc=yoozoo,dc=com'
LDAP_USER_LOGIN_ATTR = 'sAMAccountName'
LDAP_BIND_USER_DN= 'Manager@yoozoo.com'
LDAP_BIND_USER_PASSWORD= "2124g$"