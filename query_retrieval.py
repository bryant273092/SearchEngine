'''
Created on May 31, 2019

@author: Bryant Hernandez
'''

class Query():
    


    def __init__(self, query, index):
        
        self.query = query.split(" ")
        self.len_query = len(query)
        self.index = index.token_f_dict
        self.url_key = index.url_doc_key
        self.search_results = None
        self.pos_docs = {}
        self.search_token()
        
        
    def search_token(self):
        for token in self.query:
            try: 
                self.pos_docs = self.index[token.lower()]
                for doc_id in self.pos_docs.keys():
                    self.rank_documents(doc_id)
                self.print_urls()
            except:
                print('No Results')
    def rank_documents(self, doc_id):
        self.pos_docs[doc_id]['Rank'] =(1/1+ self.pos_docs[doc_id]['Outlinks']) * self.pos_docs[doc_id]['Tf-IDf']
        self.search_results =[entry for entry in sorted(self.pos_docs.items(), key = lambda entry: entry[1]['Rank'], reverse = True)]
        
    def print_urls(self):
        print(len(self.search_results))
        print('Best Matches Are for:' +str(self.query)+' \n')
        if self.search_results != None:
            for file in self.search_results[:20]:
                print(self.url_key[file[0]])       
            
            
        
        
            
        