from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from datetime import datetime
import requests
import json
app = Flask(__name__)
host_url = "http://3.133.83.203:5011"

search_cache=set()

# ROUTES
# @app.get("/marketorders/")
# def get_health():
#     t = str(datetime.now())
#     msg = {
#         "welcome": "Welcome to EVE marketer order board",
#         "at time": t
#     }
#
#     # DFF TODO Explain status codes, content type, ... ...
#     result = Response(json.dumps(msg), status=200, content_type="application/json")
#
#     return result

@app.route('/marketorders/', methods=['GET', 'POST'])
def category():
    url = host_url+'/api/marketorders/'
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    return render_template('homepage.html' , data = data, name_diction = list(search_cache))

@app.route('/marketorders/<type_name>', methods=['GET', 'POST'])
def marketorders(type_name):
    url = host_url+'/api/marketorders/{}?{}'.format(type_name, request.query_string.decode("utf-8") )
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    return render_template('orders.html' , data = data)

@app.route('/item/<type_name>', methods=['GET', 'POST'])
def itemdetail(type_name):
    url = host_url+'/api/item/{}'.format(type_name)
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    return render_template('item.html' , data = data)

@app.route('/marketorders/<type_name>/<station_id>', methods=['GET', 'POST'])
def marketorders_station(type_name,station_id):
    url = host_url+'/api/marketorders/{}/{}?{}'.format(type_name, station_id, request.query_string.decode("utf-8") )
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    return render_template('orders.html' , data = data)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5012,debug=True)




