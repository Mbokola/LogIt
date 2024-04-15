#!/usr/bin/python3
""" Flask application
"""

from models.auth import Auth
from flask import Flask, render_template, request, redirect, url_for, make_response
from models.log import Log
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
logging = Log()
AUTH = Auth()
host = '0.0.0.0'
port = 5001


def check_session(session_id):
    """ Checks if session exists
    """
    record = AUTH.get_user_from_session_id(session_id)
    return record


# Logging app routes
@app.route('/', strict_slashes=False)
def logs():
    """ Displays logs
    """
    return render_template('about.html')


@app.route('/home', strict_slashes=False)
def home():
    """ Displays logs
    """
    session_id = request.cookies.get("session_id")
    record = check_session(session_id)
    if not record:
        return redirect(url_for("login"))
    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'], strict_slashes=False)
def create_log():
    """ Creates a log
    """
    session_id = request.cookies.get("session_id")
    record = check_session(session_id)
    if not record:
        return redirect(url_for("login"))

    if request.method == 'POST':
        log_name = request.form['Log Name']
        log_name_with_email = f"{log_name}_{record.email}"
        fields = request.form.getlist('text')
        if log_name_with_email not in logging.all_logs():
            logging.create_log(log_name_with_email, fields)
        return redirect(url_for('home'))
    return render_template('createlog.html')


@app.route('/logs', strict_slashes=False)
def all_logs():
    """ Retrives all logs
    """
    session_id = request.cookies.get("session_id")
    record = check_session(session_id)
    if not record:
        return redirect(url_for("login"))

    all_logs = logging.all_logs()
    for idx, log in enumerate(all_logs):
        if log == "users":
            del all_logs[idx]
    user_logs = [log.split("_")[0] for log in all_logs if log.split("_")[1] == record.email]
    return user_logs


@app.route('/log/<log_name>', methods=['GET', 'POST'], strict_slashes=False)
def log_fields(log_name):
    """ Retrieves log fields
    """
    session_id = request.cookies.get("session_id")
    record = AUTH.get_user_from_session_id(session_id)
    if not record:
        return redirect(url_for("login"))
    log_name_with_email = f"{log_name}_{record.email}"
    log_fields = logging.get_log_field(log_name_with_email)
    del log_fields[0]
    if request.method == 'POST':
        data = {}
        for field in log_fields:
            data[field] = request.form[field]
        logging.make_log_entry(log_name_with_email, data)

    return render_template('log.html', log_fields=log_fields)


@app.route('/log/view/<log_name>', strict_slashes=False)
def view_logs(log_name):
    """ Retrieves logs of log
    """
    session_id = request.cookies.get("session_id")
    record = AUTH.get_user_from_session_id(session_id)
    if not record:
        return redirect(url_for("login"))

    log_name_with_email = f"{log_name}_{record.email}"

    fields = logging.get_log_field(log_name_with_email)
    content = logging.retrieve_log(log_name_with_email)
    return render_template('show_logs.html', log_name=log_name, log_fields=fields, content=content)


@app.route('/log/<log_name>/page/<id>', strict_slashes=False)
def view_page(log_name, id):
    """ Expands a log
    """
    session_id = request.cookies.get("session_id")
    record = AUTH.get_user_from_session_id(session_id)
    if not record:
        return redirect(url_for("login"))

    log_name_with_email = f"{log_name}_{record.email}"
    fields = logging.get_log_field(log_name_with_email)[1:]
    log = logging.get_log(log_name_with_email, {"id": int(id)})
    contents = list(log[0])[1:]
    zipped_data = list(zip(fields, contents))

    return render_template('display.html', zipped_data=zipped_data)


@app.route('/log/delete/<log_name>', methods=['DELETE'], strict_slashes=False)
def del_log(log_name):
    """ Deletes a log
    """
    session_id = request.cookies.get("session_id")
    record = AUTH.get_user_from_session_id(session_id)
    if not record:
        return redirect(url_for("login"))

    log_name_with_email = f"{log_name}_{record.email}"
    logging.del_log(log_name_with_email)
    return render_template('index.html')


@app.route('/about', strict_slashes=False)
def about():
    """ Directs you to about page
    """
    return render_template("about.html")


# Auth service routes
@app.route("/users", methods=["GET", "POST"], strict_slashes=False)
def users():
    """ Handles registration of a user
    """
    if request.method == "POST":
        try:
            email = request.form.get("your_email")
            password = request.form.get("password")
            AUTH.register_user(email, password)

            return render_template("login.html")

        except ValueError:
            print("email already registered")
    return render_template("login.html")


@app.route("/sessions", methods=["GET", "POST"], strict_slashes=False)
def login():
    """ Handles user login
    """
    if request.method == "POST":

        email = request.form.get("your_email_1")
        password = request.form.get("password_1")
        result = AUTH.valid_login(email, password)

        if result:
            session_id = AUTH.create_session(email)
            response = make_response(redirect(url_for("home")))
            response.set_cookie("session_id", session_id)
            return response

    return render_template("login.html")


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """ Ends a session and logs out user
    """
    session_id = request.cookies.get("session_id")
    record = AUTH.get_user_from_session_id(session_id)

    if record:
        user_id = record.id
        AUTH.destroy_session(user_id)
    return make_response("", 200)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ handles password reset
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return "Succesful"
    except ValueError:
        return "unsucessful"


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ Updates the users' password
    """
    email = request.form.get("your_email")
    new_password = request.form.get("new_password")
    reset_token = request.form.get("reset_token")

    try:
        AUTH._db.find_user_by(reset_token=reset_token)
        AUTH.update_password(reset_token, new_password)
        return "succesful"
    except (NoResultFound, ValueError):
        return "unsucessful"


if __name__ == '__main__':
    app.run(host=host, port=port)
