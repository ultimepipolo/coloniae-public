from application import app

#app.secret_key = 'xNn9T2fbWABfvLrRi0m5'
app.run(debug=True, host='0.0.0.0')


# VIA GUNICORN :
# if __name__=='main':
#     app.run()