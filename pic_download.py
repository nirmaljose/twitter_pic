#authour="@josenirmal"
import urllib2
import urllib
import os
import time
import httplib
import sys
import json
import re
import string

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
    dumpjson(screen_name,url)

def dumpjson(screen_name,url):
    c =  httplib.HTTPSConnection("twitter.com")
    c.request("GET",url)
    response = c.getresponse()
    print response.status, response.reason, "https://twitter.com%s" % url
    data = response.read().decode("utf-8")
    respc_dic = json.loads(data)
    min_pos =  respc_dic['min_position']
    m = re.findall('data-image-url(.+?)data-element',data)
    for i in range(len(m)):
        parseimgurl(m[i])
    if min_pos:
    		time.sleep(60)
        autoscroll(screen_name,min_pos)

def parseimgurl(image):
    line = str(image).replace("\\","")
    line = line[2:len(line) - 7]
    if downloadpic(line):
        print "Downloaded\t %s" % line
    else:
        Print "Failed\t %s" % line

def downloadpic(pic_url):
    urllib.urlretrieve(pic_url,os.path.basename(pic_url))
    return true

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
    autoscroll(screen_name ,data_min)

if __name__ == "__main__":
    main()
