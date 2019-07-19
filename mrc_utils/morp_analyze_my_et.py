#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import grpc
from google.protobuf import empty_pb2
from google.protobuf import json_format

exe_path = os.path.realpath(sys.argv[0])
bin_path = os.path.dirname(exe_path)
lib_path = os.path.realpath(bin_path + '../lib/python')
sys.path.append(lib_path)
sys.path.insert(0, '/home/msl/maum/lib/python')
print(sys.path)
from maum.brain.nlp import nlp_pb2_grpc
from maum.brain.nlp import nlp_pb2
from maum.common import lang_pb2
from common.config import Config
import re

remote = "10.122.64.83:9823"
channel = grpc.insecure_channel(remote)
stub = nlp_pb2_grpc.NaturalLanguageProcessingServiceStub(channel)

class NLPAnalyzer:
    stub = None

    def __init__(self):
        #self.conf = Config()
        #self.conf.init('minds-ta.conf')
        #self.remote = "localhost:9823" + self.conf.get("minds-ta.nlp.3.kor.port")
        self.morp_result = list()
        self.ner_result = list()
        self.sentence_result = list()
        self.morp_result_list = list()

    def __analyze__(self, text):
        # type: (object) -> object
        in_text = nlp_pb2.InputText()
        in_text.text = text
        in_text.lang = lang_pb2.kor
        in_text.split_sentence = True
        in_text.use_tokenizer = False

        message_result = stub.Analyze(in_text)

        morp_result = list()
        ner_result = list()
        sentence_result = list()
        sentence_morp_dict = ()
        for i in range(len(message_result.sentences)):
            sentence = message_result.sentences[i].text
            sentence_result.append(sentence.strip())
            morp_analysis = message_result.sentences[i].morps
            morp = ""
            for j in range(len(morp_analysis)):
                morp = morp_analysis[j].lemma + "/" + morp_analysis[j].type
            morp_result.append(morp.strip())
            self.sentence_morp_dict[sentence] = morp_result
            self.morp_result_list.append(morp_result)

            ner_analysis = message_result.sentences[i].nes

            ner = ""
            for j in range(len(ner_analysis)):
                ner = ner_analysis[j].text + "/" + ner_analysis[j].type
                if not ner:
                    continue
                else:
                    ner = ner.encode('utf-8').strip()
                    ner_result.append(ner.strip())

        self.morp_result = morp_result
        self.ner_result = ner_result
        self.sentence_result = sentence_result

    def __extract_sentence__(self, text):
        in_text = nlp_pb2.InputText()
        in_text.text = text
        in_text.lang = lang_pb2.kor
        in_text.split_sentence = True
        in_text.use_tokenizer = False

        message_result = stub.Analyze(in_text)
        sentence_result = list()

        for i in range(len(message_result.sentences)):
            sentence = message_result.sentences[i].text
            sentence_result.append(sentence.strip())

        return sentence_result

    def __extract_morp__(self, text):
        in_text = nlp_pb2.InputText()
        in_text.text = text
        in_text.lang = lang_pb2.kor
        in_text.split_sentence = True
        in_text.use_tokenizer = False

        message_result = stub.Analyze(in_text)

        morp_result = list()
        for i in range(len(message_result.sentences)):  # 찬란하/VA ㄴ/ETM 유산/NNG ,/SP 시티헌터/NNG ,/SP 주군/NNG 의/JKG 태양/NNG ,/SP 닥터/NNG 이방/NNG 이/VCP ㄴ/ETM 등/NNB
            morp_analysis = message_result.sentences[i].morps
            morp = ""
            for j in range(len(morp_analysis)):
                morp = morp + " " + morp_analysis[j].lemma + "/" + morp_analysis[j].type
            morp = morp.encode('utf-8').strip()
            morp_result.append(morp)  # 찬란하/VA ㄴ/ETM 유산/NNG ,/SP 시티헌터/NNG ,/SP 주군/NNG 의/JKG 태양/NNG ,/SP 닥터/NNG 이방/NNG 이/VCP ㄴ/ETM 등/NNB

        return morp_result

    def __extract_ner__(self, text):
        in_text = nlp_pb2.InputText()
        in_text.text = text
        in_text.lang = lang_pb2.kor
        in_text.split_sentence = True
        in_text.use_tokenizer = False

        message_result = stub.Analyze(in_text)

        ner_result = list()
        for i in range(len(message_result.sentences)):
            ner_analysis = message_result.sentences[i].nes
            for j in range(len(ner_analysis)):
                ner = ner_analysis[j].text + "/" + ner_analysis[j].type
                if not ner:
                    continue
                else:
                    ner = ner.encode('utf-8').strip()
                    ner_result.append(ner.strip())

        return ner_result

    def __extract_sentence_morp__(self, text):
        in_text = nlp_pb2.InputText()
        in_text.text = text
        in_text.lang = lang_pb2.kor
        in_text.split_sentence = True
        in_text.use_tokenizer = False

        message_result = stub.Analyze(in_text)

        sentence_morp_dict = dict()
        for i in range(len(message_result.sentences)):
            sentence = message_result.sentences[i].text
            morp_analysis = message_result.sentences[i].morps

            morp = ""
            for j in range(len(morp_analysis)):
                morp = morp_analysis[j].lemma + "/" + morp_analysis[j].type
            morp = morp.encode('utf-8').strip()

            sentence_morp_dict[morp] = dict

        return sentence_morp_dict

    def __extract_sentence_morp__(self, text):
        in_text = nlp_pb2.InputText()
        in_text.text = text
        in_text.lang = lang_pb2.kor
        in_text.split_sentence = True
        in_text.use_tokenizer = False

        message_result = stub.Analyze(in_text)
        sentence_morp_dict = dict()
        for i in range(len(message_result.sentences)):
            sentence = message_result.sentences[i].text
            morp_analysis = message_result.sentences[i].morps

            morp = ""
            for j in range(len(morp_analysis)):
                morp = morp + " " + morp_analysis[j].lemma + "/" + morp_analysis[j].type
            morp = morp.encode('utf-8').strip()
            sentence_morp_dict[morp] = sentence

        return sentence_morp_dict

    def __extract_sentence_morp__(self, text, flag):
        in_text = nlp_pb2.InputText()
        in_text.text = text
        in_text.lang = lang_pb2.kor
        in_text.split_sentence = True
        in_text.use_tokenizer = False

        message_result = stub.Analyze(in_text)
        sentence_morp_dict = dict()
        morp_result = list()
        for i in range(len(message_result.sentences)):
            sentence = message_result.sentences[i].text.strip()
            morp_analysis = message_result.sentences[i].morps

            morp = ""
            for j in range(len(morp_analysis)):
                morp = morp + " " + morp_analysis[j].lemma + "/" + morp_analysis[j].type
            morp = morp.encode('utf-8').strip()
            morp_result.append(morp)
            sentence_morp_dict[morp] = sentence

        return sentence_morp_dict, morp_result

    def __extract_dependency_parser__(self, text):
        in_text = nlp_pb2.InputText()
        in_text.text = text
        in_text.lang = lang_pb2.kor
        in_text.split_sentence = True
        in_text.use_tokenizer = False

        message_result = stub.Analyze(in_text)

        dependency_result_list = list()
        for i in range(len(message_result.sentences)):
            dependency_result = message_result.sentences[i].dependency_parsers

            for j in range(len(dependency_result)):
                dependency_dict = dict()
                dependency_dict["id"] = dependency_result[j].seq
                dependency_dict["text"] = dependency_result[j].text
                dependency_dict["head"] = dependency_result[j].head
                dependency_dict["label"] = dependency_result[j].label
                dependency_dict["weight"] = dependency_result[j].weight
                if len(dependency_result[j].mods) == 0:
                    dependency_dict["mods"] = list()
                else:
                    mods_list = list()
                    for k in range(len(dependency_result[j].mods)):
                        mods_list.append(dependency_result[j].mods[k])
                    dependency_dict["mods"] = mods_list

                dependency_result_list.append(dependency_dict)

        return dependency_result_list

    def get_dependency_parser_result(self, text):
        return self.__extract_dependency_parser__(text)

    def get_result_sentence_list(self, text):
        return self.__extract_sentence__(text)

    def get_result_morp_list(self, text):
        return_list = list()
        for temp in self.__extract_morp__(text):  # 찬란하/VA ㄴ/ETM 유산/NNG ,/SP 시티헌터/NNG ,/SP 주군/NNG 의/JKG 태양/NNG ,/SP 닥터/NNG 이방/NNG 이/VCP ㄴ/ETM 등/NNB
            print (temp)
            tokens = temp.decode('utf-8').split()
            for token in tokens:  # 찬란하/VA
                item = token.split("/")
                if len(item) > 2:
                    item = ["/"] + [item[-1]]
                return_list.append("/".join([item[0], item[1].lower()]))  # ['찬란하/va']
        return return_list

    def get_result_morp_str(self, text):
        result = ""
        for temp in self.__extract_morp__(text):
            result = result + " " + temp.decode('utf-8')
        return result.strip()

    def get_result_ner_list(self, text):
        return self.__extract_ner__()

    def get_result_sentence_morp_dict(self, text, flag):
        if flag == "sentence_morp":
            return self.__extract_sentence_morp__(text)
        elif flag == "both":
            return self.__extract_sentence_morp__(text, flag)

    def get_tree_result(self, content, original_token=False, sentence_list=False):
        ret = self.get_all_result(content)
        final_list = list()
        word_list = list()
        original_sent_list = list()
        for sent in ret.sentences:
            original_sent = list()
            if original_token:
                for word in sent.words:
                    word_list.append(word.text)
            if sentence_list:
                for word in sent.words:
                    original_sent.append(word.text)
                original_sent_list.append(" ".join(original_sent))
            sent_list = list()
            for morph in sent.morph_evals:  # target: 찬란한 # result: 찬란하/VA+ㄴ/ETM # m_end: 1
                tokens = morph.result.replace("+", "\t").replace("\t/SW", "+/SW").split("\t")  # ['찬란하/VA', 'ㄴ/ETM']
                item_list = list()
                for token in tokens:  # 찬란하/VA
                    item = token.split("/")  # ['찬란하', 'VA']
                    if len(item) > 2:
                        item = ["/"] + [item[-1]]
                    # item_list.append("/".join([item[0], item[1].lower()]))  # ['찬란하/va'] # ['찬란하/va', 'ㄴ/etm']
                    item_list.append("/".join([item[0], item[1]]))  # ['찬란하/va'] # ['찬란하/va', 'ㄴ/etm']
                sent_list.append(item_list)
            final_list.append(sent_list)
        if original_token and sentence_list:
            return final_list, word_list, original_sent_list
        elif original_token and not sentence_list:
            return final_list, word_list
        elif not original_token and sentence_list:
            return final_list, original_sent_list
        else:
            return final_list

    def get_all_result(self, text):
        in_text = nlp_pb2.InputText()
        in_text.text = text
        in_text.lang = lang_pb2.kor
        in_text.split_sentence = True
        in_text.use_tokenizer = False
        in_text.level = 1
        in_text.keyword_frequency_level = 0
        ret = stub.Analyze(in_text)
        return ret

    def for_line(self, ff):
        for line in ff:
            line = line.replace("\n", "")
            abc = re.compile(r"\[.\]")
            line = abc.sub("", line)
            content = line
            morph_content = nlp_analyze.get_tree_result(content)
            first = list()
            for mc in morph_content:
                first.extend(mc)
            second = list()
            second.append(first)

            for m in second:
                fin = ""
                for n in m:
                    fin += "+".join(n)
                    fin += " "
                f2.write("\t".join([content, fin]))
            f2.write("\n")

    def sentence_split(self, content, original_token=True, sentence_list=True):
        ret = self.get_all_result(content)
        original_sent_list = list()
        for sent in ret.sentences:
            original_sent = list()
            for word in sent.words:
                original_sent.append(word.text)
            original_sent_list.append(" ".join(original_sent))
        return original_sent_list


if __name__ == "__main__":
    nlp_analyze = NLPAnalyzer()
    f = open("/home/msl/ys/cute/data/morp/건축학개론_split.txt", "r")
    f2 = open("/home/msl/ys/cute/data/morp/건축학개론_split_result.txt", "w")
    typ = "nlp"
    # typ = "split_sentence"
    if typ == "nlp":
        ff = f.readlines()
        nlp_analyze.for_line(ff)
    if typ == "split_sentence":
        first = list()
        for line in f:
            line = line.replace("\n", "")
            abc = re.compile(r"\[.\]")
            line = abc.sub("", line)
            content = line
            split_sentences = nlp_analyze.sentence_split(content)
            for split_sentence in split_sentences:
                first.append(split_sentence)
        # sorted_first = sorted(first, key=len, reverse=True)
        for sf in first:
            if str(sf).count(' ')>=2:
                f2.write(sf)
                f2.write("\n")
    f.close()
    f2.close()
