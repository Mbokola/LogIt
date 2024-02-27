#!/usr/bin/python3
""" Flask application
"""

from flask import Flask, render_template, request, redirect, url_for
from models.log import Log

app = Flask(__name__)
logging = Log()
host = '0.0.0.0'
port = 5001


@app.route('/', strict_slashes=False)
def logs():
    """ Displays logs
    """
    return render_template('index.html')


@app.route('/create', methods=['GET', 'POST'], strict_slashes=False)
def create_log():
    """ Creates a log
    """
    if request.method == 'POST':
        log_name = request.form['Log Name']
        fields = request.form.getlist('text')
        if log_name not in logging.all_logs():
            logging.create_log(log_name, fields)
        return redirect(url_for('logs'))
    return render_template('createlog.html')


@app.route('/logs', strict_slashes=False)
def all_logs():
    """ Retrives all logs
    """
    all_logs = logging.all_logs()
    return all_logs


@app.route('/log/<log_name>', methods=['GET', 'POST'], strict_slashes=False)
def log_fields(log_name):
    """ Retrieves log fields
    """
    log_fields = logging.get_log_field(log_name)
    del log_fields[0]
    if request.method == 'POST':
        data = {}
        for field in log_fields:
            data[field] = request.form[field]
        logging.make_log_entry(log_name, data)

    return render_template('log.html', log_fields=log_fields)

@app.route('/log/view/<log_name>', strict_slashes=False)
def view_logs(log_name):
    """ Retrieves logs of log
    """
    return render_template('show_logs.html')

if __name__ == '__main__':
    app.run(host=host, port=port)
