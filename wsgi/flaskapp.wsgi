import sys

project_home = "/var/www/flaskapp"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from flaskapp.app import app as application

