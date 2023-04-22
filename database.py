"""
    Oracle database connection
    @author: Ricardo Portela
"""
import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy import text
import datetime
from flask import jsonify



class OracleDB:
    """
       OracleDB Database
    """
    def __init__(self):
        self.username = 'tavex'
        self.password = 'tavex'
        self.hostname = 'localhost'
        self.port = '1521'
        self.sid = 'xe'
        self.engine = None
        self.conn = None
        self.rconn = None
        self.oracle_connection_string = ('oracle+cx_oracle://{username}:{password}@' +
            cx_Oracle.makedsn('{hostname}', '{port}', service_name='{service_name}')
        )

    def connect(self):
        try:
            self.engine = create_engine(
                self.oracle_connection_string.format(
                    username=self.username,
                    password=self.password,
                    hostname=self.hostname,
                    port=self.port,
                    service_name=self.sid,
                ), pool_size=100)
            self.conn = self.engine.connect()
            self.rconn = self.engine.raw_connection()
            print("opening connection...")

        except cx_Oracle.DatabaseError as e:
            self.engine = None
            print(e)
            exit(1)

    def getSnapshotList(self):
        res = self.conn.execute(text("SELECT * FROM SNAPSHOTS"))
        payload = []
        content = {}
        for result in res:
            content = {'id': result[0], 'snapshot_date': result[1]}
            payload.append(content)
            content = {}
        return payload

    def getPurchases(self):
        res = self.conn.execute(text("""
                                     select p.item_id
                                          , p.paid
                                          , p.purchase_date
                                          , i.title
                                          , p.id 
                                       from PURCHASES p, ITEMS i
                                      where p.item_id = i.id
                                      order by p.purchase_date
        """))
#                                    select ITEM_ID
#                                         , PAID
#                                         , PURCHASE_DATE
#                                      from PURCHASES         
        payload = []
        content = {}
        for result in res:
            content = {'item_id': result[0], 'paid':result[1], 'purchase_date': result[2], 'name': result[3], 'id':result[4]}
            payload.append(content)
            content = {}
        return payload
    
    def getTrackingForAllItems(self, daysSince):
        res= self.conn.execute(text("""
        select buy
             , sell
             , snapshot_id
             , snapshot_date
             , item_id
          from PRICES t, SNAPSHOTS s
         where t.snapshot_id = s.id
           and s.snapshot_date > sysdate - """ + str(daysSince) + """
         order by s.snapshot_date"""
           ))
        
        payload = []
        content = {}
        for result in res:
            content = {'buy': result[0], 'sell': result[1], 'snapshot_id': result[2], 'snapshot_date':result[3], 'item_id':result[4]}
            payload.append(content)
            content = {}
        return payload

    def getTracking(self, itemId, daysSince):
        res= self.conn.execute(text("""
        select buy
             , sell
             , snapshot_date
          from PRICES t, SNAPSHOTS s
         where t.snapshot_id = s.id
           and t.item_id = """ +  str(itemId) + """
           and s.snapshot_date > sysdate - """ + str(daysSince) + """
         order by s.snapshot_date"""
           ))
        
        payload = []
        content = {}
        for result in res:
            content = {'buy': result[0], 'sell': result[1], 'datum':result[2]}
            payload.append(content)
            content = {}
        return payload
    
    def getItemList(self):
        res = self.conn.execute(text("SELECT * FROM ITEMS"))
        payload = []
        content = {}
        for result in res:
            content = {'id': result[0], 'name': result[1]}
            payload.append(content)
            content = {}
        return payload
    
    def connection_close(self):
        self.conn.close()
        print("closing connection...")


if __name__ == '__main__':
    ora = OracleDB()
    ora.connect()
    ora.resultado()
    ora.connection_close()