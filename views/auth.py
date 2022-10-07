from urllib.parse import urlparse, urljoin

from flask import (
    Blueprint,
    jsonify,
    flash,
    abort,
    url_for,
    render_template,
    request,
    redirect,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_login import login_required, login_user, logout_user
from flask_wtf.csrf import CSRFProtect

from hanabi.models import User

csrf = CSRFProtect()


auth_app = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(LoginForm, self).__init__(*args, **kwargs)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = User()
        login_user(user)

        flash('Logged in successfully.')

        next_ = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next_):
            return abort(400)

        return redirect(next_ or url_for('base.root'))
    return render_template('login.html', form=form)


@csrf.exempt
@auth_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# @login_manager.request_loader
# def load_user_from_request(req):
#     # first, try to login using the api_key url arg
#     api_key = req.args.get('api_key')
#     if api_key:
#         user = User.query.filter_by(api_key=api_key).first()
#         if user:
#             return user
#     # next, try to login using Basic Auth
#     api_key = req.headers.get('Authorization')
#     if api_key:
#         api_key = api_key.replace('Basic ', '', 1)
#         try:
#             api_key = base64.b64decode(api_key)
#         except TypeError:
#             pass
#         user = User.query.filter_by(api_key=api_key).first()
#         if user:
#             return user
# 
#     # finally, return None if both methods did not login the user
#     return None
