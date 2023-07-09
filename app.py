from application import app
import os

is_gunicorn = os.getenv('GUNICORN')
PORT = os.getenv('PORT')

if is_gunicorn == 'True':
    print('Running with gunicorn')
    if __name__ == 'main':
        app.run()
else:
    print('Running without gunicorn')
    app.run(debug=True, host='0.0.0.0', port=PORT)
