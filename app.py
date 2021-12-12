from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging
from datetime import datetime

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)

##################################################################################################################

# This path simply echoes to check that the app is working.
# The path is /health and the only method is GETs
@app.route("/health", methods=["GET"])
def health_check():
    rsp_data = {"status": "healthy", "time": str(datetime.now())}
    rsp_str = json.dumps(rsp_data)
    rsp = Response(rsp_str, status=200, content_type="app/json")
    return rsp

@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'

@app.route('/api/E6156player/<table_name>/fullName/<prefix>')
def get_by_prefix(table_name, prefix, column_name="fullName", db_schema="E6156player"):
    if request.args.get('limit'):
        limit = request.args.get('limit')
    else:
        limit = "10"
        
    if request.args.get('offset'):
        offset = request.args.get('offset')
    else:
        offset = "0"
        
    if request.args.get('field'):
        field_list = request.args.get('field').split(',')
    else:
        field_list = None
    
    res = RDBService.get_by_prefix(db_schema, table_name, column_name, prefix, limit, offset)
    for i in range(len(res)):
        res[i]["links"] = [
            {"rel": "self", "href": f"/api/E6156player/{table_name}/id/{res[i]['id']}"}
        ]
        if field_list is not None:
            try:
                res[i] = { key: res[i][key] for key in field_list}
            except KeyError:
                rsp = Response("404 not found", status=404, content_type="application/json")
                return rsp
    if len(res):
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    else:
        rsp = Response("404 not found", status=404, content_type="application/json")
    return rsp

@app.route('/api/E6156player/<table_name>/id/<id>')
def get_by_id(table_name, id, column_name="id", db_schema="E6156player"):
        
    if request.args.get('field'):
        field_list = request.args.get('field').split(',')
    else:
        field_list = None
    
    res = RDBService.find_by_template(db_schema, table_name, {"id": id})

    for i in range(len(res)):
        res[i]["links"] = [
            {"rel": "self", "href": f"/api/E6156player/{table_name}/id/{res[i]['id']}"}
        ]
        if field_list is not None:
            try:
                res[i] = { key: res[i][key] for key in field_list}
            except KeyError:
                rsp = Response("404 not found", status=404, content_type="application/json")
                return rsp
    if len(res):
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    else:
        rsp = Response("404 not found", status=404, content_type="application/json")
    return rsp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
