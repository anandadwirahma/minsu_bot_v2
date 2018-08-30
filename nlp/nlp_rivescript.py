import json
import re

import Levenshtein
import redis
import requests
from fuzzywuzzy import process
from nltk.util import ngrams


class Nlp:
    def __init__(self):
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        #self.redisconn = redis.StrictRedis(password="1ee5f1d25745de4d5ccc09a69119da6c82636cdb20bed280e595ed16cee6301a")
        self.redisconn = redis.StrictRedis()

    def reply(self, msisdn, mesg):
        params = {'msisdn': msisdn, 'ask': mesg}
        resp = requests.post('http://localhost:3020/reply', data=json.dumps(params), headers=self.headers)
        return resp.text


    def updateNlp(self, rule):
        print "added rule: ", rule
        params = {'trigger': rule}
        resp = requests.post('http://localhost:3020/trigger', data=json.dumps(params), headers=self.headers)
        print "RICESCRIPT RULE ADDED BY AGENT"

    def set_uservar(self, msisdn, param, value):
        params = {'msisdn': msisdn, 'param': param, 'value': value}
        resp = requests.post('http://localhost:3020/setvar', data=json.dumps(params), headers=self.headers)

    def get_uservar(self, msisdn, param):
        params = {'msisdn': msisdn, 'param': param}
        resp = requests.post('http://localhost:3020/getvar', data=json.dumps(params), headers=self.headers)
        return resp.text


    def search_string(self, mesg, dict):
        idx = 0
        found = 0
        for item in dict:
            for subitem in item.split('|'):
                if subitem in mesg.lower():
                    found = 1
            if found == 1:
                return idx
            idx += 1
        if found == 1:
            return idx
        else:
            return -1


    def search_string_match(self, mesg, dict):
        idx = 0
        found = 0
        for item in dict:
            for subitem in item.split('|'):
                if subitem == mesg.lower():
                    found = 1
            if found == 1:
                return idx
            idx += 1
        if found == 1:
            return idx
        else:
            return -1


    def doNlp(self, mesg, msisdn, first_name):
        answer = self.reply(msisdn, mesg)
        if answer.find("<first_name>") > -1:
            answer = answer.replace("<first_name>",first_name)
        # print answer
        return answer

    def convertTitle(self, msg):
        if msg == "tn":
            return "Mr"
        elif msg == "ny":
            return "Mrs"
        elif msg == "nona":
            return "Ms"
        else:
            return "error"

    def validate(self, mesg, dict):
        idx = 0
        found = 0
        for item in dict:
            for subitem in item.split('|'):
                if subitem in mesg.lower():
                    found = 1
            if found == 1:
                return idx
            idx += 1
        if found == 1:
            return idx
        else:
            return -1

    def validate_num(self, mesg, dict, item_idx):
        idx = 0
        loc_key = -1
        for item in dict:
            if idx == item_idx or item_idx == -1:
                for subitem in item.split('|'):
                    loc_key = mesg.find(subitem)
                    if loc_key > -1:
                        break
                if loc_key > -1:
                    break
            idx += 1
        if loc_key > -1:
            x = re.split(r'[-;,\s]\s*',mesg[:loc_key].rstrip(' -'))[-1]
            if x.isdigit():
                return x
        return -1

    def validate_num_last(self, mesg, dict, item_idx):
        idx = 0
        loc_key = -1
        for item in dict:
            if idx == item_idx or item_idx == -1:
                for subitem in item.split('|'):
                    loc_key = mesg.find(subitem)
                    if loc_key > -1:
                        break
                if loc_key > -1:
                    break
            idx += 1
        if loc_key > -1:
            #x = re.split(r'[-;,\s]\s*',mesg[:loc_key].rstrip(' -'))[-1]
            x = mesg[loc_key+len(subitem):]
            if x:
                return x
        return -1

    def convertDate(self, msg):
        mmsg = msg.replace(" ","").replace("-","")
        mth = self.validate(mmsg,self.when)
        if mth != -1:
            dt = self.validate_num(mmsg,self.when,-1)
            yr = self.validate_num_last(mmsg,self.when,-1)
            return yr + "-%02d-" % (mth - 2) + dt.zfill(2)
        else:
            return "x"

    def checkDate(self, msg):
        res = 0
        if len(msg) != 10:
            res = 1
        else:
            j = 0
            for item in msg.split('-'):
                j += 1
                if item.isdigit() == False: res = 1
            if j != 3: res = 1
        return res

    def checkAlpha(self, msg):
        res = 0
        for item in msg.split('+'):
            if item.isalpha() == False: res = 1
        return res

    def spell_correctness3(self, ask):
        p = process.extractOne(ask, self.pool_xtrans)
        return p[0]

    def spell_correctness(self, ask):
        fuzzy_str = {}
        fuzzy_ratio = {}
        new_ask = {}
        fuzzy_str2 = {}
        fuzzy_ratio2 = {}
        new_ask2 = {}

        i = 0
        for word in ask.split(' '):
            ratio = 0
            for pool in self.pool_xtrans:

                if pool.find(word) != -1 and len(word) > 3:
                    x = 0.71
                else:
                    x = Levenshtein.ratio(word, pool)

                if ratio < x:
                    ratio = x
                    fuzzy_str[i] = pool
                    fuzzy_ratio[i] = x
            new_ask[i] = word
            if fuzzy_ratio[i] > 0.7:
                new_ask[i] = fuzzy_str[i]

            i = i + 1
            #print "     answer", fuzzy_str
        #print "     ratio", fuzzy_ratio
        #print "     new ask", new_ask

        #print "-------------------------------"

        #try using bigrams
        bigram = ngrams(ask.split(), 2)
        fuzzy_str2 = {}
        fuzzy_ratio2 = {}
        new_ask2 = {}
        i = 0
        for grams in bigram:
            token = ' '.join(grams)

            ratio = 0
            for pool in self.pool_xtrans:
                x = Levenshtein.ratio(token, pool)
                if ratio < x:
                    ratio = x
                    fuzzy_str2[i] = pool
                    fuzzy_ratio2[i] = x
            new_ask2[i] = token
            if fuzzy_ratio2[i] > 0.7:
                new_ask2[i] = fuzzy_str2[i]

            i = i + 1
        #print "     answer", fuzzy_str2
        #print "     ratio", fuzzy_ratio2
        #print "     new ask", new_ask2

        j = 0
        i = 0
        ask_correction = {}
        ask_array = ask.split(' ')
        words_count = len(ask.split(' '))
        while (i < words_count):
            if i < (words_count -1):
                if fuzzy_ratio[i] <= 0.7 and fuzzy_ratio2[i] <= 0.7:
                    ask_correction[j] = ask_array[i]
                elif fuzzy_ratio[i] <= 0.7 and fuzzy_ratio2[i] > 0.7:
                    ask_correction[j] = fuzzy_str2[i]
                    i = i + 1
                elif fuzzy_ratio[i] > 0.7 and fuzzy_ratio2[i] <= 0.7:
                    ask_correction[j] = fuzzy_str[i]
                elif fuzzy_ratio[i] > 0.7 and fuzzy_ratio2[i] > 0.7:
                    ask_correction[j] = fuzzy_str[i]
                    if fuzzy_ratio2[i] > fuzzy_ratio[i]:
                        ask_correction[j] = fuzzy_str2[i]
            else:
                if fuzzy_ratio[i] <= 0.7:
                    ask_correction[j] = ask_array[i]
                else:
                    ask_correction[j] = fuzzy_str[i]
            i = i + 1
            j = j + 1

        #print ask_correction
        s = ''
        for key, value in ask_correction.iteritems():
            s = s + value + ' '
        #print s
        return s


    def spell_correctness2(self, ask, dictionary):
        final_candidate_str = []
        final_candidate_ratio = []

        for word in ask.split(' '):
            candidate_str = []
            candidate_ratio = []
            for dict in dictionary:
                if word in dict:
                    candidate_str.append(str(dict))
                    candidate_ratio.append(Levenshtein.ratio(word, str(dict)))
            #print "1 ",candidate_str
            #print "1 ",candidate_ratio

            temp_candidate_str = candidate_str
            temp_candidate_ratio = candidate_ratio
            candidate_str = []
            candidate_ratio = []
            i = 0
            for item in temp_candidate_str:
                if (word + " ") in item or (" " + word) in item:
                    candidate_str.append(item)
                    candidate_ratio.append(temp_candidate_ratio[i])
                i = i + 1

            #print "2 ",candidate_str
            #print "2 ",candidate_ratio

            if len(candidate_str) == 1:
                final_candidate_str.append(candidate_str[0])
                final_candidate_ratio.append(candidate_ratio[0])
            elif len(candidate_str) > 1:
                x = 0
                j = 0
                i = 0
                for item in candidate_str:
                    if x < candidate_ratio[i]:
                        x = candidate_ratio[i]
                        j = i
                    i = i + 1
                final_candidate_str.append(candidate_str[j])
                final_candidate_ratio.append(candidate_ratio[j])
            elif len(candidate_str) == 0:
                if len(word) > 3 and len(temp_candidate_str) > 0:
                    x = 0
                    j = 0
                    i = 0
                    for item in temp_candidate_str:
                        if x < temp_candidate_ratio[i]:
                            x = temp_candidate_ratio[i]
                            j = i
                        i = i + 1
                    final_candidate_str.append(temp_candidate_str[j])
                    final_candidate_ratio.append(temp_candidate_ratio[j])
                else:
                    final_candidate_str.append(word)
                    final_candidate_ratio.append(0)

        #print ">>",final_candidate_str
        #print ">>",final_candidate_ratio


        s = ''
        x = ''
        for item in final_candidate_str:
            if x != item:
                s = s + item + ' '
            x = item
        return s
   
   
   
