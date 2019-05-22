import os
import xml.etree.ElementTree as etree
from datetime import datetime

data_dir = "/data1/we_eng/"
page_files_dir = "pages/"
title_file = "enwiki_title_170220.tsv"

data_file = [x for x in os.listdir(data_dir) if x.endswith("xml")][0]
print("Start file %s..." % data_file)
tree = etree.parse("%s%s" % (data_dir, data_file))
print("Finish parsing wiki file...")
root = tree.getroot()
ns_format = "{http://www.mediawiki.org/xml/export-0.10/}"
i = 0
id = ""
title = ""
ns = ""
for child1 in root:
    if i % 1000 == 0:
        print("Article %i start..." % i)
        print(datetime.now())
    if child1.tag == ("%spage" % ns_format):
        for child2 in child1:
            if child2.tag == ("%stitle" % ns_format):
                title = child2.text
            elif child2.tag == ("%sns" % ns_format):
                ns = child2.text
            elif child2.tag == ("%sid" % ns_format):
                id = child2.text
            elif child2.tag == ("%srevision" % ns_format):
                if ns == "0":
                    for child3 in child2:
                        if child3.tag == ("%stext" % ns_format):
                            with open("%s%s%s.txt" % (data_dir, page_files_dir, id), "w") as f:
                                f.write(child3.text)
                            with open("%s%s" % (data_dir, title_file), "a") as f2:
                                f2.write("%s\t%s\n" % (id, title))
                            print("Finish file id: %s, title: %s" % (id, title))
    i += 1

print("All finished")
print(datetime.now())

