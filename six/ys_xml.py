# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Created by YeongsunPark at 2019-06-24

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os, re
import sys
import json
import xml.etree.ElementTree as ET


a = list()
target_dir = sys.argv[1]
open_dir = os.listdir(target_dir)

for files in open_dir:
    with open(target_dir + '/' + files, 'r') as f:


        # tree = ET.parse('4100058_nocut/2018/09/17/04100058.20180917184633001.xml')
        tree = ET.parse(f)
        root = tree.getroot()

        # all_contents = root[2][2][5][1].findtext("DataContent")
        content = root.find("NewsItem").find("NewsComponent").find("NewsComponent").find("ContentItem").findtext("DataContent")
        content = content.replace('\n\n', '\\n')\
            .replace('\n', '').replace('사진= 머니투데이 로고', '')\
            .replace('\\n▶ 기자와 카톡 채팅하기▶ 노컷뉴스 영상 구독하기','')\
            .replace('\\n▶ 기자와 1:1 채팅','')\
            .replace("{IMG:1}", '')\
            .replace('<![CDATA[', '').replace(']]>', '')\
            .replace("lt;", '')\
            .replace("gt;", '')
        content = re.sub(r'\&\w+\;', '', content)
        content = re.sub(r'{IMG:[0-9]}', '', content)
        content = re.sub(r'{VOD:[0-9]}', '', content)
        # content = re.sub('(\\\\n){2,}', '\\n', content)
        if "[앵커]" in content or "■ 방송 " in content or "[스탠딩]" in content:
            content = ""


        title = root.find("NewsItem").find("NewsComponent").find("NewsLines").findtext("HeadLine")
        title = title.replace('<![CDATA[', '').replace(']]>', '')
        title = re.sub(r'\&\w+\;', '', title)
        # print (title)
        if "주요 뉴스]" in title:
            content = ""

        for c in root.find("NewsItem").find("NewsComponent").find("Metadata"):
            for cc in c.iter('Property'):
                for key, value in cc.attrib.items():
                    if value == "PageCategory":
                    # if value == "SubjectInfo":
                        cate = cc.attrib["Value"]
                    # if value == "SubjectInfo":
                        # cate = cc.attrib["Value"]
                    # else:
                        # cate = ""

        result = dict()
        result['data'] = list()
        if 900 > len(content) >= 600 and str(content).count('.') >=5:
            data_dict = dict()
            data_dict['title'] = title
            data_dict['content'] = content.strip().strip("\\n")
            data_dict['cate'] = cate
            data_dict['file_name'] = str(f).split('.')[1]
            result['data'].append(data_dict)
            # print (title[0])
            # with open("/home/minds/maum/resources/MRC/ys_output/" + str(f).split('.')[1] + '.txt', 'w') as fw:
                # fw.write("\t".join([title[0], all_contents[0], cate[0]]))
                # fw.write("\n")
            with open("/home/minds/maum/resources/MRC/ys_output/" + str(f).split('.')[1] + '.json', 'w') as f2:
                json.dump(result, f2, ensure_ascii=False, indent = 2)