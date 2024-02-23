#!/usr/bin/python3
""" Flask application
"""

from flask import Flask, render_template, request

app = Flask(__name__)

host = '0.0.0.0'
port = 5001


@app.route('/create', methods=['GET', 'POST'], strict_slashes=False)
def create_log():
    """ Creates a log
    """
    return render_template('createlog.html')


if __name__ == '__main__':
    app.run(host=host, port=port)
