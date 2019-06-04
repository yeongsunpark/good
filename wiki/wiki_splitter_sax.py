import os
import logging
import xml.sax
from datetime import datetime

import custom_logger

# https://www.tutorialspoint.com/python3/python_xml_processing.htm (이거 참고)
class WikiContentHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.cnt = 0
        self.data_dir = "/data1/we_kor/"
        self.page_files_dir = "pages/"
        if not os.path.exists(os.path.join(self.data_dir, self.page_files_dir)):
            os.makedirs(os.path.join(self.data_dir, self.page_files_dir))
        self.title_file = "kowiki_title_170620.tsv"
        self.reset_var()
        self.logger = self.set_logger()

    def set_logger(self):
        logger = logging.getLogger('root')
        logger.setLevel("INFO")
        logger.addHandler(custom_logger.MyHandler())
        return logger

    def reset_var(self):
        self.ispage = False
        self.istitle = False
        self.isns = False
        self.isid = False
        self.isrevision = False
        self.istext = False
        self.var_dict = dict()
        self.var_dict["text"] = list()

    def startElement(self, name, attrs):
        if name == "page":    # name 이 <page {attrs} = "{}"> 어찌구 </page>
            #print("startElement '" + name + "'")
            self.ispage = True
        elif name == "title":
            if self.isrevision is False:
                self.istitle = True
        elif name == "ns":
            self.isns = True
        elif name == "id":
            if self.isrevision is False:
                self.isid = True
        elif name == "revision":
            self.isrevision = True
        elif name == "text":
            self.istext = True

    def characters(self, content):
        if self.ispage:
            if self.istitle is True:
                self.var_dict["title"] = content
                self.istitle = False
            elif self.isns is True:
                self.var_dict["ns"] = content
                self.isns = False
            elif self.isid is True:
                self.var_dict["id"] = content
                self.isid = False
            elif self.isrevision is True:  # revision 이 있었다면 append 해서 붙여넣기 함.
                if self.istext is True:
                    self.var_dict["text"].append(content)

    def endElement(self, name):
        if name == "page":
            if self.var_dict["ns"] == "0":
                with open("%s%s%s.txt" % (self.data_dir, self.page_files_dir, self.var_dict["id"]), "a") as f:
                    f.write("".join(self.var_dict["text"]))
                with open("%s%s" % (self.data_dir, self.title_file), "a") as f2:
                    f2.write("%s\t%s\n" % (self.var_dict["id"], self.var_dict["title"]))
                self.logger.debug("Finish file id: %s, title: %s" % (self.var_dict["id"], self.var_dict["title"]))
            self.reset_var()
            self.cnt += 1
            #if self.cnt == 2:
            #    exit()
        elif name == "text":
            self.istext = False


def main(sourceFileName):
    source = open(sourceFileName)
    xml.sax.parse(source, WikiContentHandler())
    source.close()


if __name__ == "__main__":
    data_dir = "/data1/we_kor/"
    page_files_dir = "pages/"
    data_file = [x for x in os.listdir(data_dir) if x.endswith("xml")][0]
    print("Start file %s..." % data_file)

    main(data_dir + data_file)
    print("All finished")
    print(datetime.now())

