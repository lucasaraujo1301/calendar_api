from flask import Blueprint

app = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/login')
def register():
    return 'Login API'
