import logging
import re
import os

import custom_logger

home_dir = "/home/msl/data/mrc/kowiki/"
input_file = os.path.join(home_dir, "kowiki_pages_170620.tsv")
output_file = os.path.join(home_dir, "kowiki_plain_170620.tsv")
re_splitter = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s")


if __name__ == '__main__':
    logger = logging.getLogger('root')
    logger.setLevel("DEBUG")
    logger.addHandler(custom_logger.MyHandler())

    f = open(input_file)
    f_out = open(output_file, "a")
    pre_num = 0
    temp_list = list()
    cnt = 0
    for line in f:
        cnt += 1
        if cnt%10000 == 1 and cnt != 1:
            logger.info("%i start" % cnt)
        item = line.strip().split("\t")
        num = int(item[0])
        if num == pre_num and pre_num != 0:
            # write into file
            f_out.write("\n".join(temp_list))
            f_out.write("\n")
            temp_list = list()
        for senten in re_splitter.split(item[3]):
            temp_list.append(senten.strip())
        pre_num = num

    f_out.write("\n".join(temp_list))
    f_out.write("\n")
    f.close()
    f_out.close()
    logger.info("All finished")
