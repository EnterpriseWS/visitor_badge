import controller

# ------------------------------------------------------
# Use main.py to run on any WSGI server
# Example for manually run gunicorn with shell command:
#   $ uwsgi --http 127.0.0.1:8080 --module main:app
# ------------------------------------------------------
app = controller.app
