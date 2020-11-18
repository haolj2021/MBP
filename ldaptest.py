from flask_ldap3_login import LDAP3LoginManager
#from app import app
import config
from flask import Flask,render_template,request,redirect,url_for,session
from ldap3 import Server , Connection , NTLM
import config
from models import  User,Question
from exts import  db
from sqlalchemy import  or_
from flask_paginate import  Pagination,get_page_parameter

class ladpAuth():

    def __init__(self):
        self.ldap_manager = LDAP3LoginManager()
        self.ldap_manager.init_config(config)

    def auth(self,username,password):
        response = self.ldap_manager.authenticate(username,password)
        if response.status.value == 2:
            return ({
                'name':response.user_info.get('name'),
                'displayName':response.user_info.get('displayName'),
                'mail':response.user_info.get('mail'),
            })
        else:
            return None

    def getUserInfoForUsername(self,username):
        try:
            user_info = self.ldap_manager.get_user_info_for_username(username)
            return ({
                'name': user_info.get('name'),
                'displayName': user_info.get('displayName'),
                'mail': user_info.get('mail'),
            })
        except:
            return None


if __name__ == '__main__':
    userInfo = ladpAuth().getUserInfoForUsername('orionc')
    print(userInfo)