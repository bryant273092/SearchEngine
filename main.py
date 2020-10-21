import atexit
import logging

from crawler import Crawler
from frontier import Frontier
from query_retrieval import Query
from index_builder import IndexBuilder
import sys

if __name__ == "__main__":
    # Configures basic logging
    logging.basicConfig(format='%(asctime)s (%(name)s) %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)
  
    
    # Instantiates frontier and index
    frontier = Frontier()
    index = IndexBuilder()
    # If theres no index, frontier is loaded, and crawling begins
    if not index.load_index():
        
        
        frontier.load_frontier()
        # Registers a shutdown hook to save frontier state upon unexpected shutdown
        atexit.register(frontier.save_frontier)
    
        # Instantiates a crawler object and starts crawling
        
        crawler = Crawler(frontier, index)
        crawler.start_crawling()  
    while True:
        query = Query(input("Enter search query: "), index)
    
    print('done')
    
    
