from CT.app import db
from CT.models import *

# Create tables
db.create_all()

password = 'password'

# Create admin user
admin = Users('Admin', password, 'admin@admin', 1)
db.session.add(admin)
db.session.commit()
