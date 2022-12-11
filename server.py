from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
from datetime import datetime
import requests
import json
app = Flask(__name__)
host_url = "http://3.133.83.203:5011"
#host_url="http://127.0.0.1:5011"
#composite_url = "http://127.0.0.1:5013"
composite_url = "http://3.133.83.203:5013"
search_cache = set()
location_cache = set()
station_cache = set()

@app.route('/marketorders/', methods=['GET', 'POST'])
def category():
    url = host_url+'/api/marketorders'
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    return render_template('homepage.html' , data = data, name_diction = list(search_cache), location_diction = list(location_cache), station_diction = list(station_cache))

@app.route('/marketorders/<type_id>', methods=['GET', 'POST'])
def marketorders(type_id):
    url = host_url+'/api/marketorders/{}?{}'.format(type_id, request.query_string.decode("utf-8") )
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    search_cache.add(data['type_name'])
    return render_template('orders.html' , data = data)

@app.route('/item/<type_id>', methods=['GET', 'POST'])
def itemdetail(type_id):
    url = host_url+'/api/item/{}'.format(type_id)
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    search_cache.add(data['type_name'])
    return render_template('item.html' , data = data)

@app.route('/marketorders/<type_id>/<station_id>', methods=['GET', 'POST'])
def marketorders_station(type_id,station_id):
    url = host_url+'/api/marketorders/{}/{}?{}'.format(type_id, station_id, request.query_string.decode("utf-8") )
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    search_cache.add(data['type_name'])
    return render_template('orders.html' , data = data)

@app.route('/composite/marketorders/<type_id>', methods=['GET', 'POST'])
def composite_marketorders(type_id):
    url = composite_url+'/api/composite/marketorders/{}?{}'.format(type_id, request.query_string.decode("utf-8") )
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    search_cache.add(data['type_name'])
    return render_template('composite_orders.html' , data = data)

@app.route('/composite/marketorders/<type_id>/<station_id>', methods=['GET', 'POST'])
def composite_marketorders_station(type_id,station_id):
    url = composite_url+'/api/composite/marketorders/{}/{}?{}'.format(type_id, station_id, request.query_string.decode("utf-8") )
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    print(data)
    search_cache.add(data['type_name'])
    return render_template('composite_orders.html' , data = data)

@app.route('/composite/marketorders/<type_id>/by_range/<location_id>', methods=['GET', 'POST'])
def composite_marketorders_range(type_id,location_id):
    url = composite_url+'/api/composite/marketorders/{}/by_range/{}?{}'.format(type_id, location_id, request.query_string.decode("utf-8") )
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    print(data)
    search_cache.add(data['type_name'])
    location_cache.add(data['location_name'])
    return render_template('composite_orders.html' , data = data)

@app.route('/composite/marketorders/<type_id>/station/<station_id>/within/<distance>', methods=['GET', 'POST'])
def composite_marketorders_within(type_id,station_id,distance):
    url = composite_url+'/api/composite/marketorders/{}/station/{}/within{}?{}'.format(type_id, station_id, distance, request.query_string.decode("utf-8") )
    print(url)
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    print(data)
    search_cache.add(data['type_name'])
    station_cache.add(data['station_name'])
    location_cache.add(data['station_name'])
    return render_template('composite_orders.html' , data = data)


if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5012,debug=True)




