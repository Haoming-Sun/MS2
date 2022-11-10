from flask import Flask, Response, request, render_template, jsonify,redirect
from microservice2_resource import MicroService2
from flask_cors import CORS
from datetime import datetime
import json

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)

cate_cache = dict()
is_item_cache = dict()

@app.route("/api/marketorders/<type_id>", methods=["GET"])
def get_orders_by_name(type_id):
    limit = request.args.get('limit',default = 20)
    offset = request.args.get('offset',default = 0)
    sorted = request.args.get('sorted',default='')
    sorted_by = request.args.get('sorted_by',default='')
    if not sorted or sorted == 'DESC':
        sort_flag = 0
    else:
        sort_flag = 1

    links = []

    links.append({"href": '/marketorders/'+type_id, "rel":"sort", "type": "GET"} )
    links.append({"href": '/item/'+type_id, "rel":"item detail", "type": "GET"})

    rt,total_record = MicroService2.get_orders_by_name(type_id,limit,offset,sorted,sorted_by)

    if rt:
        result = dict()
        result['type_name'] = rt[0]['type_name']
        result['type_id'] = rt[0]['type_id']
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


@app.route("/api/item/<type_id>", methods=["GET"])
def get_item_by_name(type_id):

    links = []
    item_link = {"href": '/marketorders/'+type_id, "rel":"market order", "type": "GET"}
    links.append(item_link)
    rt = MicroService2.get_item_by_name(type_id)

    if rt:
        result = dict()
        result['type_name'] = rt[0]['type_name']
        result['type_id'] = rt[0]['type_id']
        result['mass'] = rt[0]['mass']
        result['volume'] = rt[0]['volume']
        result['description'] = rt[0]['description']
        result['links'] = links
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp

@app.route("/api/marketorders/<type_id>/<station_id>", methods=["GET"])
def get_orders_by_name_station(type_id,station_id):
    limit = request.args.get('limit',default = 20)
    offset = request.args.get('offset',default = 0)
    sorted = request.args.get('sorted',default='')
    sorted_by = request.args.get('sorted_by',default='')
    if not sorted or sorted == 'DESC':
        sort_flag = 0
    else:
        sort_flag = 1


    links = []
    links.append( {"href": '/item/'+type_id, "rel":"item detail", "type": "GET"})
    links.append( {"href": '/station/'+station_id, "rel":"station detail", "type": "GET"} )
    links.append( {"href": '/marketorders/'+type_id+'/'+station_id, "rel":"sort", "type": "GET"} )

    rt, total_record = MicroService2.get_orders_by_name_station(type_id,station_id,limit,offset,sorted,sorted_by)

    if rt:
        result = dict()
        result['type_name'] = rt[0]['type_name']
        result['type_id'] = rt[0]['type_id']
        result['station_id'] = station_id
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

@app.route("/api/marketorders", methods=['GET', 'POST'])
def get_cate():
    if request.method=='POST':
        jdata = request.get_json()
        parent = jdata['parent']
    else:
        parent = 'None'

    if parent in cate_cache:
        rt = cate_cache[parent]
        is_item = is_item_cache[parent]
    else:
        rt,is_item= MicroService2.get_child(parent)

    cate_cache[parent] = rt
    is_item_cache[parent] = is_item

    result = dict()
    result['data'] = rt
    result['is_item'] = is_item
    rsp = Response(json.dumps(result), status=200, content_type="application.json")

    return rsp

@app.route("/api/name2id/<type_name>", methods=['GET'])
def get_id(type_name):
    rt = MicroService2.get_id(type_name)
    if rt:
        result = dict()
        result['id'] = rt[0]['type_id']
        result['name'] = rt[0]['type_name']
        links = []
        links.append( {"href": '/item/'+str(result['id']), "rel":"item detail", "type": "GET"})
        links.append( {"href": '/marketorders/'+str(result['id']), "rel":"market orders", "type": "GET"} )
        result['links'] = links
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/api/getallitem", methods=['GET'])
def get_all():
    rt = MicroService2.get_all_item()

    result = dict()

    tmp = []
    for item in rt:
        tmp.append(item['type_name'])
    result['item_list'] = tmp
    print(result)
    rsp = Response(json.dumps(result), status=200, content_type="application.json")

    return rsp




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011,debug=True)


