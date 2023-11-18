from flask import Flask, make_response, request
from pg_helper import PostgresHelper
import logging
import urllib.parse
from flask_apscheduler import APScheduler


#https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04
#curl -X POST -H "Content-Type: application/json" -d @sample.json http://localhost


logging.basicConfig(level=logging.DEBUG, filename="/home/horzsolt/codes/savewebpage.log", format="%(levelname)s | %(asctime)s | %(message)s")

app = Flask(__name__)

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

@app.before_request
def log_request_info():
    logging.debug('Headers: %s', request.headers)
    logging.debug('Body: %s', request.get_data())

@app.after_request
def after(response):
    logging.debug("============= response =============")
    logging.debug(response.status)
    logging.debug(response.headers)
    logging.debug(response.get_data())
    return response

@app.route("/", methods=['POST', 'GET'])
def hello():
    logging.debug("Receive...")
    if request.method == 'POST':
        with (PostgresHelper()) as pg:
            url = urllib.parse.unquote(request.json['url_to_parse'])
            tags = request.json['tags']
            pg.store(url, tags)

        response = make_response("<h1>Success</h1>")
        response.status_code = 200
        return response
    else:
        return "<h1 style='color:blue'>GET: 1011</h1>"


@scheduler.task('cron', id='check_downloads_job', minute='*')
def check_downloads():
    with (PostgresHelper()) as pg:
        [logging.debug(dlItem) for dlItem in pg.list_urls_to_download()]


if __name__ == "__main__":
    app.run(host='0.0.0.0')