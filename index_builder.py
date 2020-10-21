'''
Created on May 28, 2019

@author: Bryant Hernandez
'''
from collections import defaultdict
import json
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import pickle
import math


class IndexBuilder:
    stop_words = [
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
        "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", 
        "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", 
        "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", 
        "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", 
        "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by",
        "for", "with", "about", "against", "between", "into", "through", "during", "before", "after",
        "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under",
        "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all",
        "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not",
        "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don",
        "should", "now", "title", "strong"," ", "  ",",", ".",'',"p","class","span", "id", "href",
        "h1","h2","h3","h4","h5", "ul", "http", "li","www","a", "login", "password", "home", "php", "https"
        ,"src", "font", "style","text","javascript", "div", " ", ''
        ]

    def __init__(self,):
        self.url_list = set()
        nest_d= lambda: defaultdict(dict)
        self.token_f_dict = defaultdict(nest_d)
        self.db_file = None
        self.url_doc_key = {}
        
       

    def start_scan(self, soup, url_data, outputLinks):
        print("scanning....doc - ", url_data['url'])
        self.url_list.add(url_data['url'])
        self.file_address = url_data['file_addy']
        self.url_doc_key[self.file_address] = url_data['url']
        token_count, token_freq= self.extract_tokens(soup)
        self.write_to_index(token_count, token_freq, outputLinks)
        print('URLs Searched: ', len(self.url_list))
        print('Words Found; ', len(self.token_f_dict.keys()))
    
                
        
        
    
    def write_to_index(self, token_count, token_freq, outputlinks):
        for token in token_freq.keys():
                    if token != '':
                        self.token_f_dict[token][self.file_address]  = {
                            "TF" : 1 + math.log(token_freq[token]), 
                            "Outlinks": outputlinks,
                            "Rank": 0
                            }

        
    
    
    def extract_tokens(self, soup):
        token_freq = defaultdict(int)
        token_count = 0
        #tokenss = []
        
        line = soup.get_text()
        if line != None:
            for token in re.findall("[a-zA-Z0-9]*", str(line)):
                #tokenss.append(token)
                if token.lower() not in self.stop_words and len(token) > 2 and token !=None:
                    
                    token_freq[token.lower()] +=1
                    token_count +=1
        return token_count, token_freq
        
    
                
            
        
        
    
    def calc_idf(self):
        url_count = len(self.url_list)
        for token in self.token_f_dict.keys():
            for doc in self.token_f_dict[token].keys():
                self.token_f_dict[token][doc]['Tf-IDf'] =(self.token_f_dict[token][doc]["TF"] * math.log(url_count/len(self.token_f_dict[token].keys())))
    
    def write_to_file(self):
        self.calc_idf()
        pickle.dump(dict(self.token_f_dict), open('db_file.pkl', 'wb'))
        pickle.dump(self.url_doc_key,open('key_file.pkl','wb'))
       
    
    def load_index(self):
        try:
            self.token_f_dict = pickle.load(open('db_file.pkl', 'rb'))
            self.url_doc_key = pickle.load(open('key_file.pkl','rb'))
            return True
        except:
            return False
#         self.print_db()
#     
#     def print_db(self):
#         db_file_txt = open('db_file_text.txt', 'w')
#         for token in self.token_f_dict.keys():
#             print(token)
#             db_file_txt.write("Token: "+token +"\n")
#             db_file_txt.write("Tf-IDf: "+str(self.token_f_dict[token]['Tf-IDf'])+"\n")
#             for doc in self.token_f_dict[token]['documents'].keys():
#                 db_file_txt.write("DOC-ID: "+str(doc)+"\n")
#                 db_file_txt.write("Attribute Tuple:  "+str(self.token_f_dict[token]['documents'][doc])+"\n")
#         print("dict2: ", len(self.token_f_dict.keys()))
            
            
        
        
        
        
    
        
       
        