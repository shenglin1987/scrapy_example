#-*- coding: utf-8 -*-
import sys
import urllib2
import json
import codecs
import os

# set path to store the images
save_path = os.path.abspath('./images')
if not os.path.exists(save_path):
    os.mkdir(save_path)


#write image tags into img_tags.txt file with utf-8 
img_tag_file = codecs.open('img_tags.txt', 'w', encoding='utf-8')


img_id = 1
with open(sys.argv[1], 'r') as image_json_file:
    img_infos = image_json_file.readlines()
    for img_info in img_infos:
        img_info = json.loads(img_info)
        img_tags = img_info['img_tags']
        img_src = img_info['img_url'].encode('utf-8')
        
        #load image from the url
        r = urllib2.Request(img_src)
        res = urllib2.urlopen(r)
        with open('%s/img%d.jpg'%(save_path, img_id), 'wb') as f:
            f.write(res.read())
        
        #write image tags
        img_tags = ','.join(img_tags)
        img_tag_file.write(img_tags+'\n')
        
        img_id += 1

