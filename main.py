from printer_listener import app

# ------------------------------------------------------
# Use main.py to run on any WSGI server
# Example for manually run gunicorn with shell command:
#   $ uwsgi --http 0.0.0.0:8080 --module main:app
# ------------------------------------------------------

if __name__ == "__main__":
    app.run()
