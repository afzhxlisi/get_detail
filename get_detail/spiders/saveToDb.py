import codecs
import json
import MySQLdb
import datetime
class StoreToDb(object):
    def __init__(self):
        self.file = codecs.open('detail'+datetime.date.today().__str__()+'.json')
        self.conn = MySQLdb.connect(host='localhost', user='root', passwd='12345678', db='test', port=3306, charset='utf8')
        self.cur = self.conn.cursor()

    def process_all(self):
        lines =self.file.readlines();
        items=[]
        length = 100
        times=1;
        for line in lines:
            try:
                item = json.loads(line)
                items.append(item)
                if(len(items)>=length or (times==len(lines))):
                    self.process_items(items)
                    items=[]
                times=times+1
            except Exception,e:
                print e

    def process_items(self,items):
        try:
            cur = self.cur
            cur.execute('select ifnull(max(id),0) id from lianjiadetail')
            result=cur.fetchone()
            idN = result[0]+1
            values=[]

            for i in range(len(items)):
                item =items[i]
                values.append((idN,  item['sevenDaycount'], item['totalCount'], item['fangurl']))

            cur.executemany('insert into lianjiadetail(id,sevenDaycount,totalCount,fangurl,time) values  (%s,%s,%s,%s,now())',values)
            self.conn.commit()

        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def spider_closed(self,spider):
        self.file.close()
        self.cur.close()
        self.conn.close()