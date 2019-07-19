#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-17

import json

class abc():
    def __init__(self):
        self.read_json = "/home/msl/ys/cute/data/sams2/entity_200_all_v2.json"
        self.write_json = "/home/msl/ys/cute/data/sams2/entity_200_all_v2.txt"
    def main(self):
        with open(self.read_json, "r", encoding='utf-8') as f1:
            json_data1 = json.load(f1)
        f2 = open(self.write_json, "w")

        for doc in json_data1['data']:
            for p in doc['paragraphs']:
                context = p["context_with_answer"]
                for qa in p["qas"]:
                    question = qa["question"]
                    id = qa["id"]
                    for answers in qa["answers"]:
                        text = answers ["text"]
                        source = answers["source"]
                        source_link = answers["source_link"]
                        item = id, context, question, text, source, source_link
                        f2.write("\t".join(item))
                        f2.write("\n")
        f2.close()

if __name__ == "__main__":
    a = abc()
    b = a.main()