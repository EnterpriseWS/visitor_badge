import printer_listener

# ------------------------------------------------------
# Use main.py to run on any WSGI server
# Example for manually run gunicorn with shell command:
#   $ uwsgi --http 0.0.0.0:8080 --module main:app
# ------------------------------------------------------
app = printer_listener.app
