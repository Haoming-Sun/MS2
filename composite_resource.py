import pymysql

class Composite:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        usr = "admin"
        pw = "team_lol"
        h = "database-lol.chy7cu9rusdl.us-east-2.rds.amazonaws.com"

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_orders_by_range(type_id,station_list,limit,offset,sorted,sorted_by):
        sort_dict = {'is_buy_order':'DESC','price':'DESC','duration':'DESC','station_id':'DESC','last_modified':'DESC','volume_remain':'DESC','volume_total':'DESC'}
        if sorted:
            sorted = list(sorted.split(','))
        if sorted_by:
            sorted_by = list(sorted_by.split(','))
        if len(sorted_by) != len(sorted):
            return None

        sort_param = ""
        for i in range(len(sorted)):
            del sort_dict[sorted_by[i]]
            sort_param = sort_param + sorted_by[i] + ' '+ sorted[i] + ','
        for i,v in sort_dict.items():
            sort_param = sort_param + i + ' '+ v + ','
        sort_param = sort_param[:-1]

        sql = """
             SELECT COUNT(*) AS total
             FROM (
                  SELECT * FROM microService_2.Type_Name where type_id= %s
             ) AS t1
             LEFT JOIN microService_2.Market_Orders AS t2
             ON t1.type_id = t2.type_id
             WHERE station_id in (""" +"""%s,"""*(len(station_list)-1)+ """%s)
             """
        key = [type_id]+station_list
        conn = Composite._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql,args = key)
        result = cur.fetchall()
        total_record= result[0]['total']

        sql =  """
               SELECT t1.type_name AS type_name, t1.type_id AS type_id, station_id, duration, is_buy_order, issued, price, volume_total, volume_remain, last_modified
               FROM (
                    SELECT * FROM microService_2.Type_Name where type_id= %s
               ) AS t1
               LEFT JOIN microService_2.Market_Orders AS t2
               ON t1.type_id = t2.type_id
               WHERE station_id in (""" +"""%s,"""*(len(station_list)-1)+ """%s)
               ORDER BY """+sort_param+"""
               LIMIT %s OFFSET %s;
               """
        key = [type_id]+station_list+[int(limit),int(offset)]
        conn = Composite._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql,args = key)
        result = cur.fetchall()

        return result,total_record
