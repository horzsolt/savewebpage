from flask import Flask, request
from pg_helper import PostgresWriter
import logging

#https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04
#curl -X POST -H "Content-Type: application/json" -d @sample.json http://simplerest
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def hello():
    logger.debug("1")
    if request.method == 'POST':
        logger.debug("2")
        with (PostgresWriter()) as pg:
            url = request.json['url_to_parse']
            pg.store(url)
        return "<h1 style='color:blue'>Hello There POST!</h1>"
    else:
        logger.debug("3")
        return "<h1 style='color:blue'>Hello There GET!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')