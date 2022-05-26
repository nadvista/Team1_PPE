import psycopg2
import os
from typing import List

class Database:
    DB_SCHEMA = 'public'
    DB_TABLE = 'main'
    DB_TXT_FILE = os.path.join(os.curdir + '/static/data.txt')
    def __init__(self, conn_data):
        port = str(conn_data[0])
        host = conn_data[1]
        database = conn_data[2]
        password = conn_data[3]
        user = conn_data[4]
        self.conn = psycopg2.connect(database = database, host = host,
                                     port = port, user = user, password = password)
        self.cursor = self.conn.cursor()
    
    def push(self, data: List, vid_id: str) -> None:
        '''Этот метод пушит данные в бд'''
        query = 'INSERT INTO ' + Database.DB_SCHEMA + '.' + Database.DB_TABLE
        query += ' VALUES '
        query += '(' + vid_id + ', ' + '\'{'
        for rec in data:
            query += str(rec[0]) + ', '
        query = query[:-2]
        query += '}\', \'{'
        for rec in data:
            query += str(rec[1]) + ', '
        query = query[:-2]
        query += '}\', \'{'
        for rec in data:
            query += str(rec[2]) + ', '
        query = query[:-2]
        query += '}\', \'{'
        for rec in data:
            query += str(rec[3]) + ', '
        query = query[:-2]
        query += '}\')'
        self.cursor.execute(query)
        self.conn.commit()
        with open(Database.DB_TXT_FILE, 'a') as db:
            db.write(vid_id + ':' +  data.__repr__() + '\n')


    def _process_data(self, data: List) -> List:
        '''Обработка данных. Изyачально данные поступают в виде массива кортежей (время, id, тип)
           Результат обработки - массив вида: [(время появления, время исчезновения, id, тип объекта)]
        '''
        #отслеживание появления объекта по id
        appeared = []
        processed = []
        for rec in data:
            if rec[1] not in appeared:
                appeared.append(rec[1])
                processed.append(rec)
        appeared_time = []
        sorted_data = []
        for rec in data:
            if rec[0] not in appeared_time:
                appeared_time.append(rec[0])
        
        #приведение данных к новому виду - [(фрейм, [id, тип])]
        for time in appeared_time:
            temp = []
            for rec in data:
                if rec[0] == time:
                    temp.append(rec[1])
            sorted_data.append((time,temp))
        
        sorted_data.append((1.01, [0]))

        #отслеживание исчезновений
        disappears = []
        for i in range(1,len(sorted_data)):
            temp1 = []
            temp2 = []
            for id in sorted_data[i-1][1]:
                temp1.append(id)
            for id in sorted_data[i][1]:
                temp2.append(id)
            for id in temp1:
                if id not in temp2:
                    disappears.append((sorted_data[i-1][0], id))

        processed = sorted(processed, key = lambda rec: rec[1])
        disappears = sorted(disappears, key = lambda rec: rec[1])

        #слияние списков
        merged = []
        for i in range(len(disappears)):
            merged.append((processed[i][0], disappears[i][0], processed[i][1], processed[i][2]))
        return merged