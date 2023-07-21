from application import app
import os

is_gunicorn = os.getenv('GUNICORN')
PORT = os.getenv('PORT')
HOST = os.getenv('HOST')

if is_gunicorn == 'True':
    print('Running with gunicorn')
    if __name__ == 'main':
        # the host and port are set through the gunicorn command parameters
        app.run()
else:
    print('Running without gunicorn')
    app.run(debug=True, host=HOST, port=PORT)
