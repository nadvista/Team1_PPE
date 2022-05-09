import psycopg2
from typing import Dict, List

class Database:
    LARGE_DB_ITER_COUNT = 5
    LARGE_DB_SCHEMA = 'public'
    SMALL_DB_SCHEMA = 'public'
    LARGE_DB_TABLE = 'main'
    SMALL_DB_TABLE = 'main'
    def __init__(self, port, host, database, password, user):
        self.conn = psycopg2.connect(database = database, host = host,
                                     port = port, user = user, password = password)
        self.cursor = self.conn.cursor()

    def push(self, data: List, method: str, vid_id: str) -> None:
        #более полная статка, инфа о 5 точках с наименьшим количеством объектов каждого класса
        #и 5 точках с наибольшим количеством объектов каждого класса
        if method == 'large':
            data = self._process_data_large(data)
            self._push_data_large(vid_id, data)
        #наибольшее количество объектов каждого класса
        elif method == 'small':
            data = self._process_data_small(data)
            self._push_data_small(vid_id, data)

    def _push_data_small(self, vid_id: str, data: Dict) -> None:
        #БД: id, char info[(объект, количество, время)]
        query = "INSERT INTO " + Database.SMALL_DB_SCHEMA
        query += "." + Database.SMALL_DB_TABLE + ' VALUES '
        query += '(' + '\'' + vid_id + '\'' + ', ARRAY ['
        for key in data.keys():
            query += '\'' + key + ';' + str(data[key][0]) + ';' + str(data[key][1]) + '\','
        query = query[:-1]
        query += ']);'
        self.cursor.execute(query)
    
    def _push_data_large(self, vid_id: str, data: Dict) -> None:
        #БД: id, float helmet[[количество, время]], float gloves[[количество, время]]
        #float mask[[количество, время]]
        query = "INSERT INTO " + Database.LARGE_DB_SCHEMA
        query += "." + Database.LARGE_DB_TABLE + ' VALUES '
        query += '(' + '\'' + vid_id + '\'' + ', '
        for key in data.keys():
            query_part = '{'
            for i in range(2 * Database.LARGE_DB_ITER_COUNT):
                query_part += '{' + data[key][i][0] + ',' + float(data[key][i][1]) + '},'
            query += query_part[:-1] + '},'
        query = query[:-1]
        query += '});'
        self.cursor.execute(query)

    def _process_data_small(self, data: List) -> List:
        #0 - количество, 1 - время
        max_nums = {
            'helmet':[0,-1],
            'mask':[0,-1],
            'gloves':[0,-1]
        }
        for record in data:
            keys = record[1].keys()
            for key in keys:
                if record[1][key] > max_nums[key][0]:
                    max_nums[key][0] = record[1][key]
                    max_nums[key][1] = record[0]
        return max_nums
    
    def _process_data_large(self, data: List) -> List:
        graphs = {
            'helmet':[],
            'mask':[],
            'gloves':[]
        }
        for record in data:
            for key in graphs.keys():
                try:
                    graphs[key].append((record[0],record[1][key]))
                except:
                    pass
        
        red_graphs = {
            'helmet':[],
            'mask':[],
            'gloves':[]
        }
        for key in graphs.keys():
            curlist = graphs[key]
            timests = []
            vals = []
            
            for timest, val in curlist:
                timests.append(timest)
                vals.append(val)

            for _ in range(Database.LARGE_DB_ITER_COUNT):
                try:
                    red_graphs[key].append((timests[vals.index(max(vals))],max(vals)))
                    timests.pop(vals.index(max(vals)))
                    vals.remove(max(vals))
                except:
                    red_graphs[key].append((-1,0))
                try:
                    red_graphs[key].append((timests[vals.index(min(vals))],min(vals)))
                    timests.pop(vals.index(min(vals)))
                    vals.remove(min(vals))
                except:
                    red_graphs[key].append((-1,0))

        return red_graphs