#!/usr/bin/python
# datademo.py 
# a simple script to pull some data from MySQL

import MySQLdb
ssl={'ca':'/home/yumeya3939/car/python-mysql/ca.pem','key':'/home/yumeya3939/car/python-mysql/client-key.pem','cert':'/home/yumeya3939/car/python-mysql/client-cert.pem'}
db = MySQLdb.connect(host="car.leafu.one", port=3307 , user="car", passwd="81YPOGNXf9Yjaah#", db="test", ssl=ssl)
#db = MySQLdb.connect(host="localhost", port=3306 , user="root", passwd="syhu0630", db="test")

#create a cursor for the select
cur = db.cursor()
#lat = 25.0912315
#lng = 121.4752987
#execute an sql query
#query = ("INSERT INTO gps (gpslat,gpslng,username) VALUES (%s,%s,%s)")
#data = (lat,lng,'car')
#cur.execute(query, data)
#db.commit()

#querye = ("INSERT INTO sensor (gpslat, gpslng, temperature, humidity, username) VALUES (%s,%s,%s,%s,%s)")
#sen = (25.0912315,121.4752987,29,50,'car')
#cur.execute(querye, sen)
#db.commit()
cur.execute("SELECT * FROM account")

##Iterate 
for row in cur.fetchall():
    #print 
    print (row)

# close the cursor
cur.close()

# close the connection
db.close ()
