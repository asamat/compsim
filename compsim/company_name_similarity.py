import csv
import os
from collections import defaultdict
import sys
import difflib
import string
from time import time
import random
import re
import datetime
import pickle
import decimal
from company_score_tfidf import keyword_score_map

class CompanyNameSimilarity:
    
    def preprocess(self, field):
        return field.encode('utf-8').lower().replace('\n','').replace("'",' ').replace('\r','').replace('/',' ').\
            replace('&','  ').replace('-',' ').replace('|','').replace(',','').replace('.',' ').replace('@',' ').replace('#',' ')

    def normalize_company_name(self, company_name):
        stop_list = ["organisation","org","inc", "ltd", "labs", "lab", "llc",
                     "llp", "corporation", "corp","fed","plc","inc", "co", "svc","services","service", "company",
                     "dept","department","assoc","association","limited","incorporation"]
        abbreviate = {
            "cu":"credit union"
            }
        return " ".join([self.preprocess(word).strip() if self.preprocess(word) not in abbreviate else abbreviate[self.preprocess(word)] \
                             for word in company_name.split() if self.preprocess(word).strip() not in stop_list])
                

    def is_company_approx_contained(self, str1, str2):
            approx_contained_threshold = 0.3
            if len(str1) == 0:
                    return False
            str1_set = set([x.lower().strip() for x in str1.split()])
            str2_set = set([x.lower().strip() for x in str2.split()])
            if len(list(str1_set)) == 0 or len(list(str2_set)) == 0:
                    return False
            score_num = len(str1_set & str2_set)
            score_den1 = len(str1_set)
            score_den2 = len(str2_set)
            return ((float(score_num) / float(score_den1))+(float(score_num)/float(score_den2)))/2 > approx_contained_threshold

  
    def match_score(self, str1, str2, mode = 'reflex'):
            str1 = self.normalize_company_name(str1)
            str2 = self.normalize_company_name(str2)
            if len(str1) == 0:
                    return 0
            str1_set = set([x.lower().strip() for x in str1.split()])
            str2_set = set([x.lower().strip() for x in str2.split()])
            if len(list(str1_set)) == 0 or len(list(str2_set)) == 0:
                    return 0
            if not self.is_company_approx_contained(str1,str2):
                 return 0
            mismatch_set1=[elem for elem in str1.split() if elem not in (str1_set & str2_set)]
            mismatch_set2=[elem for elem in str2.split() if elem not in (str1_set & str2_set)]
            partial_match_score_1 = self.compute_partial_match_score(mismatch_set1,mismatch_set2)
            partial_match_score_2 = self.compute_partial_match_score(mismatch_set2,mismatch_set1)
            score_num = len(str1_set & str2_set)
            score_den1 = len(str1_set)
            score_den2 = len(str2_set)
            if mode == 'non-reflex':
                return float(score_num + partial_match_score_1) / float(score_den1)
            if mode == 'reflex':
                return ((float(score_num + partial_match_score_1) / float(score_den1))+(float(score_num + partial_match_score_2)/float(score_den2)))/2


    def compute_partial_match_score(self, set_str1,set_str2):
        set_compute = set_str1
        set_check = set_str2
        if len(set_compute)==0:
            return 0
        score=0
        for word in set_compute:
            check_word_list=difflib.get_close_matches(word,set_check, n=1, cutoff=0.6)
            score += (-float(self.score_company_name(set([word])))) if len(check_word_list) == 0 \
                                                                    else difflib.SequenceMatcher(None,word, check_word_list[0] ).ratio()
            if len(check_word_list) > 0:
               if check_word_list[0] in set_check: set_check.remove(check_word_list[0])
        return score

    def score_company_name(self,word_set):
        score = 0
        for word in list(word_set):
            if not  word in keyword_score_map:
                score += 1.0
            else:
                score += float(keyword_score_map[word])
        return score   