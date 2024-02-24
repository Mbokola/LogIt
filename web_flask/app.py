#!/usr/bin/python3
""" Flask application
"""

from flask import Flask, render_template, request
from models.log import Log

app = Flask(__name__)
logging = Log()
host = '0.0.0.0'
port = 5001


@app.route('/create', methods=['GET', 'POST'], strict_slashes=False)
def create_log():
    """ Creates a log
    """
    if request.method == 'POST':
        log_name = request.form['Log Name']
        fields = request.form.getlist('text')
        if log_name not in logging.all_logs():
            logging.create_log(log_name, fields)
    return render_template('createlog.html')


if __name__ == '__main__':
    app.run(host=host, port=port)
