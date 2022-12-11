from flask import Flask, Response, request, render_template, jsonify,redirect
from composite_resource import Composite
from flask_cors import CORS
from datetime import datetime
import requests
import json

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)

MS2_url = "http://3.133.83.203:5011"
#MS2_url = "http://127.0.0.1:5011"
MS1_url = "http://54.165.212.118:5011"

cate_cache = dict()
is_item_cache = dict()

@app.route("/api/composite/marketorders/<type_id>", methods = ["GET"])
def get_orders_composite(type_id):
    url = request.path.replace("/composite","")
    url = MS2_url+url
    print(url)

    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    if data:
        for i in range(len(data['orders'])):
            curr_station_id = data['orders'][i]['station_id']
            url = MS1_url+"/api/stationparent/"+curr_station_id
            print(url)
            try:
                uResponse = requests.get(url)
            except requests.ConnectionError:
                return "Connection Error"
            Jresponse = uResponse.text
            station_detail = json.loads(Jresponse)
            data['orders'][i]['station_name'] = station_detail['name']
            data['orders'][i]['station_security'] = station_detail['security']
            data['orders'][i]['system'] = station_detail['system_name']
            data['orders'][i]['system_id'] = station_detail['system_id']
            data['orders'][i]['cons'] = station_detail['constellation_name']
            data['orders'][i]['cons_id'] = station_detail['constellation_id']
            data['orders'][i]['region'] = station_detail['region_name']
            data['orders'][i]['region_id'] = station_detail['region_id']
        rsp = Response(json.dumps(data), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/composite/marketorders/<type_id>/<station_id>", methods = ["GET"])
def get_orders_station_composite(type_id,station_id):
    url = request.path.replace("/composite","")
    url = MS2_url+url
    print(url)
    links = []
    links.append( {"href": '/item/'+type_id, "rel":"item detail", "type": "GET"})
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    if data:
        for i in range(len(data['orders'])):
            curr_station_id = data['orders'][i]['station_id']
            url = MS1_url+"/api/stationparent/"+curr_station_id
            print(url)
            try:
                uResponse = requests.get(url)
            except requests.ConnectionError:
                return "Connection Error"
            Jresponse = uResponse.text
            station_detail = json.loads(Jresponse)
            data['orders'][i]['station_name'] = station_detail['name']
            data['orders'][i]['station_security'] = station_detail['security']
            data['orders'][i]['system'] = station_detail['system_name']
            data['orders'][i]['system_id'] = station_detail['system_id']
            data['orders'][i]['cons'] = station_detail['constellation_name']
            data['orders'][i]['cons_id'] = station_detail['constellation_id']
            data['orders'][i]['region'] = station_detail['region_name']
            data['orders'][i]['region_id'] = station_detail['region_id']
        data['links'] = links
        rsp = Response(json.dumps(data), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/composite/marketorders/<type_id>/by_range/<location_id>", methods=["GET"])
def get_orders_by_range(type_id,location_id):
    limit = request.args.get('limit',default = 20)
    offset = request.args.get('offset',default = 0)
    sorted = request.args.get('sorted',default='')
    sorted_by = request.args.get('sorted_by',default='')
    if not sorted or sorted == 'DESC':
        sort_flag = 0
    else:
        sort_flag = 1

    url = MS1_url+"/api/childstation/"+location_id
    try:
        uResponse = requests.get(url)
    except uResponse.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    print(data)
    station_list = [i['station_id'] for i in data['station_list']]
    curr_name = data['name']

    links = []
    links.append( {"href": '/item/'+type_id, "rel":"item detail", "type": "GET"})
    links.append( {"href": '/marketorders/'+type_id, "rel":"sort", "type": "GET"} )

    rt, total_record = Composite.get_orders_by_range(type_id,station_list,limit,offset,sorted,sorted_by)

    for i in range(len(rt)):
        curr_station_id = rt[i]['station_id']
        url = MS1_url+"/api/stationparent/"+curr_station_id
        print(url)
        try:
            uResponse = requests.get(url)
        except requests.ConnectionError:
            return "Connection Error"
        Jresponse = uResponse.text
        station_detail = json.loads(Jresponse)
        rt[i]['station_name'] = station_detail['name']
        rt[i]['station_security'] = station_detail['security']
        rt[i]['system'] = station_detail['system_name']
        rt[i]['system_id'] = station_detail['system_id']
        rt[i]['cons'] = station_detail['constellation_name']
        rt[i]['cons_id'] = station_detail['constellation_id']
        rt[i]['region'] = station_detail['region_name']
        rt[i]['region_id'] = station_detail['region_id']

    if rt:
        result = dict()
        result['type_name'] = rt[0]['type_name']
        result['type_id'] = rt[0]['type_id']
        result['location_id'] = location_id
        result['location_name'] = curr_name
        result['order_num'] = len(rt)
        result['links'] = links
        result['orders'] = rt
        result['sort_index'] = sorted_by
        result['sort_flag'] = sort_flag
        result['limit'] = limit
        result['offset'] = offset
        if len(rt)<int(limit) or int(offset)+int(limit)>=total_record:
            result['next']=0
        else:
            result['next']=1


        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/composite/marketorders/<type_id>/station/<station_id>/within/<distance>", methods=['GET'])
def get_orders_by_distance(type_id,station_id,distance):
    limit = request.args.get('limit',default = 20)
    offset = request.args.get('offset',default = 0)
    sorted = request.args.get('sorted',default='')
    sorted_by = request.args.get('sorted_by',default='')
    if not sorted or sorted == 'DESC':
        sort_flag = 0
    else:
        sort_flag = 1

    url = MS1_url+"/api/station/"+station_id+"/within/"+distance

    try:
        uResponse = requests.get(url)
    except uResponse.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    station_list = list(data['station_list'].keys())
    curr_name = data['name']

    links = []
    links.append( {"href": '/item/'+type_id, "rel":"item detail", "type": "GET"})
    links.append( {"href": '/marketorders/'+type_id, "rel":"sort", "type": "GET"} )

    rt, total_record = Composite.get_orders_by_range(type_id,station_list,limit,offset,sorted,sorted_by)

    for i in range(len(rt['orders'])):
        curr_station_id = rt[i]['station_id']
        url = MS1_url+"/api/stationparent/"+curr_station_id
        print(url)
        try:
            uResponse = requests.get(url)
        except requests.ConnectionError:
            return "Connection Error"
        Jresponse = uResponse.text
        station_detail = json.loads(Jresponse)
        rt[i]['station_name'] = station_detail['name']
        rt[i]['station_security'] = station_detail['security']
        rt[i]['system'] = station_detail['system_name']
        rt[i]['system_id'] = station_detail['system_id']
        rt[i]['cons'] = station_detail['constellation_name']
        rt[i]['cons_id'] = station_detail['constellation_id']
        rt[i]['region'] = station_detail['region_name']
        rt[i]['region_id'] = station_detail['region_id']

    if rt:
        result = dict()
        result['type_name'] = rt[0]['type_name']
        result['type_id'] = rt[0]['type_id']
        result['station_id'] = station_id
        result['station_name'] = curr_name
        result['order_num'] = len(rt)
        result['links'] = links
        result['orders'] = rt
        result['sort_index'] = sorted_by
        result['sort_flag'] = sort_flag
        result['limit'] = limit
        result['offset'] = offset
        if len(rt)<int(limit) or int(offset)+int(limit)>=total_record:
            result['next']=0
        else:
            result['next']=1


        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5013,debug=True)


