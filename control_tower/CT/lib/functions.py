# -*- coding: utf-8 -*-
from flask import request
import bcrypt

#### Encryption with salt = 8; GENERATE A STRING OF 60 CHARACTERS ####
def crypt(new_password):
    new_password = new_password.encode("utf-8")
    return bcrypt.hashpw(new_password,bcrypt.gensalt(8))

#### Verify encryption ####
def verify_crypt(password,password_crypt):
    password = password.encode("utf-8")
    return bcrypt.hashpw(password,password_crypt) == password_crypt

#### Get Page Itens (per page = 10) ####
def get_page_items():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = 10
    else:
        per_page = int(per_page)
    offset = (page - 1) * per_page
    return page, per_page, offset
