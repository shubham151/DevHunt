from flask import Flask

app = Flask(__name__)

if hasattr(app.jinja_env, 'cache'):
    app.jinja_env.cache.clear()
    print('Cache cleared successfully')
else:
    print('Cache not found or unable to clear')
