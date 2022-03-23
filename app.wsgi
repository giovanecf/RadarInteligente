import sys
sys.path.insert(0, '/var/www/webapp')

activate_this = '/home/webuser/.local/share/virtualenvs/webapp-UFTjLTBU/bin/a$
with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

from app import app as application