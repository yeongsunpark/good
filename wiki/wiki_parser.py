import os
import re
import logging
import html

import custom_logger

class WikiParser():
    # represent wikipedia parser

    def __init__(self):
        self.home_dir = "/data1/we_kor/"
        self.pages_dir = os.path.join(self.home_dir, "pages/")
        self.output_dir = os.path.join(self.home_dir, "pages_processed/")
        self.output_file = os.path.join(self.home_dir, "kowiki_pages_170620_sent_chunk_10.tsv")
        self.printUnit = "sent_chunk"       #para, doc, sent_chunk
        self.num_sent_chunk = 10
        self.remove_oneline = True      # remove line start with special character regardless of the length
        self.isFilter = True        # for special order, please set False
        self.extract_titles_location = "/data1/wiki_ko_10000"     # for special reason
        self.title_file = os.path.join(self.home_dir, "kowiki_title_170620.tsv")
        self.header_list = [re.compile(r"\=+\s*참고\s*문헌\s*\=+"), re.compile(r"\=+\s*바깥\s*고리\s*\=+"),
                            re.compile(r"\=+\s*같이\s*보기\s*\=+")]
        self.id_start = None       # or None
        self.p_id = ""
        self.title = ""
        self.no_title_idx = 0
        self.logger = self.set_logger()
        # comment entity(<!-- -->)
        self.re9 = re.compile(r"\<\!\-\-(?:(?!\-\-\>)(?:.|\n))*\-\-\>")
        # file entity
        self.re1 = re.compile(r"\[\[\D{1,10}:(?:(?!\[\[)(?:.|\n))*(\[\[(?:(?!\]\])(?:.|\n))*\]\](?:(?!\[\[)(?:.|\n))*)*\]\]")
        # any html entity entity(close only)
        self.re7 = re.compile(r"\<[^\<]+\/\>")
        # any html entity entity(open - close)
        self.re2 = re.compile(r"\<[^\>]+\>(?:(?!\<\/)(?:.|\n))*\<\/[^\>]+\>")
        # http link entity
        self.re13 = re.compile(r"\[https*\:\/\/[^\]]+\]")
        # information box entity
        self.re3 = re.compile(r"\{\{[^\{\{]*(\{\{[^\{\{]*\}\}[^\{\{]*)*\}\}")
        # any wiki description annotation
        self.re11 = re.compile(r"\{\{[^\{\{]*\|([^\}\}\|]*)\}\}")
        # wiki table entity
        self.re4 = re.compile(r'\{\|\s*class="?wikitable"?[^\}]*\}')
        # image table entity
        self.re8 = re.compile(r'\{\|[^\}]*\}')
        # hyperlink description entity
        self.re5 = re.compile(r"\[\[((?:(?!\]\])(?:.|\n))*)\|((?:(?!\]\])(?:.|\n))*)\]\]")
        # header entity
        self.re6 = re.compile(r"=+[^=]*=+")
        # incomplete br tag
        self.re10 = re.compile(r"\<br[^\>]*\>")
        # table delimiter ----
        self.re12 = re.compile(r"^\-{2,}$")
        # empty parenthesis (, , )
        self.re14 = re.compile(r"\([, ]+\)")
        # parenthesis ({{본명|, 1972년 2월 21일 ~ )
        self.re15 = re.compile(r"\({+.+\)")
        self.re_splitter = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s")

    def set_logger(self):
        logger = logging.getLogger('root')
        logger.setLevel("INFO")
        logger.addHandler(custom_logger.MyHandler())
        return logger

    def create_dict(self, input_file):
        output_dict = dict()
        with open(input_file) as f:
            for line in f.readlines():
                item = line.strip().split("\t")
                try:
                    output_dict[item[0]] = item[1]
                except IndexError:
                    self.no_title_idx += 1
        return output_dict

    def rm_wiki_entity(self, input_text):
        output_text = input_text.replace("#REDIRECT", self.title).replace("#redirect", self.title).replace("#넘겨주기", self.title)
        output_text = self.re9.sub("", output_text)
        output_text = self.re1.sub("", output_text)
        output_text = self.re7.sub("", output_text)
        output_text = self.re2.sub("", output_text)
        #replaced_url = " ".join(re.search(self.re13, output_text).group(0)[1:-1].split(" ")[1:])
        output_text = self.re13.sub("", output_text)
        output_text = self.re3.sub("", output_text)
        output_text = self.re11.sub(r"\1", output_text)
        output_text = self.re4.sub("", output_text)
        output_text = self.re8.sub("", output_text)
        output_text_list = output_text.strip().split("\n")
        rm_idx = -1
        for header in self.header_list:
            i = 0
            while i < len(output_text_list):
                if re.match(header, output_text_list[i]):
                    rm_idx = i
                    break
                i += 1
            if rm_idx != -1:
                break
        if rm_idx == -1:
            output_text = "\n".join(output_text_list)
        else:
            output_text = "\n".join(output_text_list[:rm_idx])
        output_text = html.unescape(output_text)
        output_text = self.re5.sub(r"\2(\1)", output_text)
        output_text = self.re6.sub("", output_text)
        output_text = self.re10.sub("", output_text)
        output_text = self.re14.sub("", output_text)
        output_text = self.re15.sub("", output_text)
        return output_text.replace("[[", "").replace("]]", "").replace("'''", "").replace("''", "")\
            .replace("<onlyinclude>", "").replace("__NOTOC__", "").replace("()", "")

    def rm_short_line(self, input_text):
        return_list = [x.strip() for x in input_text.split("\n") if x.strip() != ""]
        i = 0
        while i < len(return_list):
            if self.remove_oneline:
                if return_list[i].startswith("*") or return_list[i].startswith(";") or\
                return_list[i].startswith(":") or return_list[i].startswith("#") or\
                return_list[i].startswith("|") or return_list[i].startswith("{") or\
                self.re12.match(return_list[i]) is not None:
                    del return_list[i]
                    i -= 1
                elif len(return_list[i]) <= 20:
                    del return_list[i]
                    i -= 1
            else:
                if ((return_list[i].startswith("*") or return_list[i].startswith(";") or
                    return_list[i].startswith(":") or return_list[i].startswith("#") or
                     return_list[i].startswith("{")) and
                        len(return_list[i]) <= 35) or \
                        return_list[i].startswith("|") or \
                        self.re12.match(return_list[i]) is not None:
                    del return_list[i]
                    i -= 1
                elif len(return_list[i]) <= 20:
                    del return_list[i]
                    i -= 1
            i += 1
        return return_list

if __name__ == "__main__":
    is_test = False
    wp = WikiParser()

    pages_list = os.listdir(wp.pages_dir)
    wp.logger.info("Number of pages: %i" % len(pages_list))

    title_dict = wp.create_dict(wp.title_file)
    wp.logger.info("Finish creating title file..")

    if wp.isFilter:
        filter_titles = os.listdir(wp.extract_titles_location)

    i = 0
    for page_file in pages_list:
        wp.p_id = page_file.split(".")[0]
        if wp.id_start is not None:
            if int(wp.p_id) <= wp.id_start:
                continue
        if i != 0 and (i % 10000 == 0):
            wp.logger.info("%i files processed..." % i)
        wp.title = title_dict[wp.p_id]
        if wp.isFilter:
            if wp.title.replace(" ", "_") not in filter_titles:
                wp.logger.debug("Skip doc not in extraction list..")
                continue
            filter_titles.remove(wp.title.replace(" ", "_"))
        wp.logger.debug("Start id: %s, title: %s" % (wp.p_id, wp.title))
        with open("%s%s" % (wp.pages_dir, page_file), "r") as f:
            body = f.read()
        output_body = wp.rm_wiki_entity(body)
        output_body_list = wp.rm_short_line(output_body)
        if is_test is False:
            with open(wp.output_file, "a") as f:
                p_idx = 1
                if wp.printUnit == "para":
                    for p in output_body_list:
                        f.write("%s\t%s\t%i\t%s\n" % (wp.p_id, wp.title, p_idx, p))
                        p_idx += 1
                elif wp.printUnit == "doc":
                    f.write("%s\t%s\t%i\t%s\n" % (wp.p_id, wp.title, p_idx, " ".join(output_body_list)))
                elif wp.printUnit == "sent_chunk":
                    print_list = list()
                    temp_list = list()
                    wp.logger.debug(output_body_list)
                    for p in output_body_list:
                        for senten in wp.re_splitter.split(p):
                            if len(temp_list) >= wp.num_sent_chunk:
                                print_list.append(temp_list)
                                temp_list = list()
                            else:
                                temp_list.append(senten.strip())
                    wp.logger.debug(print_list)
                    if len(temp_list) < wp.num_sent_chunk-1:
                        if len(print_list) > 0:
                            print_list[-1].extend(temp_list)
                        else:
                            print_list.append(temp_list)
                    else:
                        print_list.append(temp_list)
                    for p_idx in range(len(print_list)):
                        f.write("%s\t%s\t%i\t%s\n" % (wp.p_id, wp.title, p_idx+1, " ".join(print_list[p_idx])))
        else:
            for p in output_body_list:
                wp.logger.debug(p)
        i += 1

    if wp.isFilter:
        with open("missing_titles.txt", "w") as f:
            f.write("\n".join(filter_titles))
        wp.logger.info("The number of missing title: %i" % len(filter_titles))
    wp.logger.info("No title count: %i" % wp.no_title_idx)
    wp.logger.info("Processed title count: %i" % i)
    wp.logger.info("All finished...")
