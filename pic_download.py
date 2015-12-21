#authour="@josenirmal"
import urllib2
import urllib
import os
import time
import httplib
import sys
import json
from BeautifulSoup import BeautifulSoup
import re
import string
import hashlib
import sqlite3

def data_position(data_item):
    find_1text = "data-max-position"
    len_find_1text = len(find_1text)
    find_2text = "data-min-position"
    len_find_2text = len(find_2text)
    start1 = data_item.find(find_1text)
    start2 = data_item.find(find_2text)
    data_max = data_item[start1+len_find_1text+2:start2-2]
    data_min = data_item[start2+len_find_2text+2:len(data_item)-1]
    return data_min

def autoscroll(screen_name,data_min):
    url = "/i/profiles/show/%s/timeline?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false" % (screen_name,data_min)
    downscroll(screen_name,url)

def downscroll(screen_name,url):
    c =  httplib.HTTPSConnection("twitter.com")
    c.request("GET",url)
    response = c.getresponse()
    print response.status, response.reason, "https://twitter.com%s" % url
    data = response.read().decode("utf-8")
    respc_dic = json.loads(data)
    min_pos =  respc_dic['min_position']
    parsejson(screen_name,data,min_pos)

def parsejson(screen_name,data,min_pos):
    m = re.findall('data-image-url(.+?)data-element',data)
    for i in range(len(m)):
        parseimgurl(screen_name, m[i],min_pos)
    sys.exit(1)
    if min_pos:
        print "Wait for 60 Sec"
        time.sleep(60)
        autoscroll(screen_name,min_pos)

def parseimgurl(screen_name,image,min_pos):
    line = str(image).replace("\\","")
    line = line[2:len(line) - 7]
    sqlite_add(screen_name,line,min_pos)

def sqlite_add(screen_name,image_url,min_pos):
    if min_pos:
        min_pos = min_pos
    else:
        min_pos = 0
    md51 = hashlib.md5(image_url)
    md5_value = md51.hexdigest()
    print md5_value
    location = "twipic"
    table_name = "md5"
    conn = sqlite3.connect(location)
    c = conn.cursor()
    c.execute("create table if not exists {tablename} (md5sum TEXT,screenname TEXT,position INT)".format(tablename=table_name))
    c.execute("select * from md5 WHERE md5sum= ?", (md5_value,))
    row = c.fetchone()
    if row is None:
        c.execute('insert into md5 values (?,?,?)', (screen_name,md5_value,min_pos,))
        conn.commit()
        downloadpic(image_url)
        c.close()
        conn.close()
    else:
        c.close()
        conn.close()
        sys.exit(1)

def downloadpic(pic_url):
    urllib.urlretrieve(pic_url,os.getcwd()+"\\"+os.path.basename(pic_url))

def main():
    screen_name = sys.argv[1]
    c = httplib.HTTPSConnection("twitter.com")
    c.request("GET","/%s" % screen_name)
    response = c.getresponse()
    print response.status, response.reason
    data = response.read()
    file_o = open("temp.txt","wb")
    file_o.write(data)
    file_o.close()
    lines = [line.rstrip('\n') for line in open("temp.txt")]
    os.remove("temp.txt")
    a = 1
    data_min = 0
    for i in lines:
        if i.find("data-max-position") != -1:
            data_min = data_position(i)
        a += 1
    for i in lines:
        if i.find('data-image-url') != -1:
            imgurl = i[len('data-image-url')+4:len(i)-1]
            sqlite_add(screen_name,imgurl,data_min)
    autoscroll(screen_name ,data_min)

if __name__ == "__main__":
    main()
