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
                    item_list.append("/".join([item[0], item[1].lower()]))  # ['찬란하/va'] # ['찬란하/va', 'ㄴ/etm']
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

if __name__ == "__main__":
    nlp_analyze = NLPAnalyzer()
    content = """찬란한 유산, 시티헌터, 주군의 태양, 닥터 이방인 등"""
    # content = """MBC TV '밥상 차리는 남자'도 메인 연출자가 파업에 동참하면서 촬영이 중단됐다가 지난 14일 재개됐는데 역시 같은 이유다. '밥상 차리는 남자'는 파업 직전인 지난 2일 시작했기 때문에 파업으로 결방되면 방송을 시작하자마자 중단하는 꼴이 된다. 드라마로서는 첫 방송이 연기되는 것보다 방송 도중 결방되는 게 더 큰 타격이다. 흐름이 끊겨버려 안 하느니만 못한 상황이 되기 때문이다. 그로 인해 메인 연출자의 파업 참여 부담이 더 커진다. 반면 예능 프로그램의 경우는 애초 출연자와의 출연 계약 기간이라는 것이 없어 파업으로 결방돼도 계약상 문제가 >발생하는 경우가 거의 없고, 내용도 드라마처럼 연속성이 있는 게 아니라 결방의 부담이 드라마에 비해서는 현저히 적다. MBC노조 관계자는 "아직 확정적으로 말하긴 힘들지만 앞으로 시작하는 드>라마의 경우는 대부분 제때 방송을 시작하기 쉽지 않을 것"이라며 "프로그램마다 사정이 다 복잡한 것은 사실이지만 파업이 길어지면 계획된 일정대로 가기 어렵다"고 전했다."""
    #morp_content = nlp_analyze.get_result_morp_list(content)
    morph_content = nlp_analyze.get_dependency_parser_result(content)
    #dp_content = nlp_analyze.get_dependency_parser_result(content)
    print(morph_content)
    #with open("tmp.json", "w") as f:
    #    json.dump(dp_content, f, sort_keys=True, indent=4)
    #print(json.dumps(dp_content, sort_keys=True, indent=4))
    #print(dp_content)
