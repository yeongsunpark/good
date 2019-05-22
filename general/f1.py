# -*- coding: utf-8 -*-
import collections

def f1_score(prediction, ground_truth):
    prediction_tokens = prediction.split()
    print (prediction_tokens)
    ground_truth_tokens = ground_truth.split()
    print (ground_truth_tokens)
    # logging.debug(prediction_tokens)
    # logging.debug(ground_truth_tokens)
    common = collections.Counter(prediction_tokens) & collections.Counter(ground_truth_tokens)
    print ("common:", common)
    num_same = sum(common.values())
    print ("num_same:", num_same)
    if num_same == 0:
        print ("num_same:", num_same)
        return 1234
    precision = 1.0 * num_same / len(prediction_tokens)
    print ("precision:", precision)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    print ("recall:", recall)
    f1 = (2 * precision * recall) / (precision + recall)
    print ("f1:", f1)
    return f1

if __name__ == "__main__":
    f1_score("목적/nng 이/jks 뭐/np 이/vcp 지/ec",
             "만들/vv 어/ec 지/vx ㄴ/etm 목적/nng 이/jks 뭐/np 이/vcp 야/ef ?/sf")