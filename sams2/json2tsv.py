#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by YeongsunPark at 2019-07-17

import json

class abc():
    def main(self, r_json, w_json):
        with open(r_json, "r", encoding='utf-8') as f1:
            json_data1 = json.load(f1)
        f2 = open(w_json, "a")  # w -> a

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
                        confidence = answers["confidence"]  # add
                        item = id, context, question, text, source, source_link, str(confidence)  # add conf
                        f2.write("\t".join(item))
                        f2.write("\n")
        f2.close()
        return 1

if __name__ == "__main__":
    a = abc()
    # read_json = "/home/msl/ys/cute/data/sams2/save/random_questions_from_m4_5_to_6.json"
    read_json = "/home/msl/ys/cute/data/sams2/save/entity_200_all_v2.json"
    write_json = "/home/msl/ys/cute/data/sams2/save/entity_and_random_question.txt"
    b = a.main(read_json, write_json)