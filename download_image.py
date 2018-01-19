#-*- coding: utf-8 -*-
import sys
import urllib2
import json
import codecs
import os
import time 

enable_proxy = True
proxy_handler = urllib2.ProxyHandler({'http': 'http://dev-proxy.oa.com:8080'})
null_proxy_handler = urllib2.ProxyHandler({})

if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)

urllib2.install_opener(opener)

# set path to store the images
save_path = os.path.abspath('./images')
if not os.path.exists(save_path):
    os.mkdir(save_path)


#write image tags into img_tags.txt file with utf-8 
img_tag_file = codecs.open('img_tags.txt', 'w', encoding='utf-8')


img_id = 1
start = time.clock()
with open(sys.argv[1], 'r') as image_json_file:
    if img_id % 1000 == 0:
        print 'cost %d seconds download 1000 images ' % round(time.clock()-start)
        start = time.clock()
    img_infos = image_json_file.readlines()
    for img_info in img_infos:
        img_info = json.loads(img_info)
        img_tags = img_info['img_tags']
        img_src = img_info['img_url'].encode('utf-8')
        try:
            #load image from the url
            r = urllib2.Request(img_src)
            res = urllib2.urlopen(r)
            with open('%s/img%d.jpg'%(save_path, img_id), 'wb') as f:
                f.write(res.read())
        
            #write image tags
            img_tags = ','.join(img_tags)
            img_tag_file.write(img_tags+'\n')
        except:
            print "exception at open url"
            print 'img_url ', img_src
            print 'img_tags ', img_tags 
        
        img_id += 1
        if img_id < 10:
            print img_id

