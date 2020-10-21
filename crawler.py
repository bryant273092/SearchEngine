import logging
import re
from urllib.parse import urlparse, urljoin, parse_qs
from corpus import Corpus
import os
import lxml
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier, index):
        self.frontier = frontier
        self.corpus = Corpus()
        self.history = []
        self.subdomain = {}
        self.outLinks = {}
        self.traps = []
        self.index = index

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.fetch_url(url)

            self.outLinks[url_data['url']] = 0
            temp = urlparse(url_data['url']).hostname
            self.subdomain[temp] = 1

            for next_link in self.extract_next_links(url_data):
                if self.corpus.get_file_name(next_link) is not None:
                    if self.is_valid(next_link):
                        self.outLinks[url_data['url']] = self.outLinks[url_data['url']] + 1
                        self.subdomain[temp] = self.subdomain[temp] + 1
                        self.frontier.add_url(next_link)

        self.index.write_to_file()
#         self.analytics()

    def fetch_url(self, url):
        """
        This method, using the given url, should find the corresponding file in the corpus and return a dictionary
        containing the url, content of the file in binary format and the content size in bytes
        :param url: the url to be fetched
        :return: a dictionary containing the url, content and the size of the content. If the url does not
        exist in the corpus, a dictionary with content set to None and size set to 0 can be returned.
        """
        file_address = self.corpus.get_file_name(url)
        if(file_address != None):
            file_bytes = open(file_address, "rb")

            file_size = os.stat(file_address).st_size

            url_data = {
                "url": url,
                "file_addy": file_address,
                "content": file_bytes,
                "size": file_size
            }
        else:
            url_data = {
                "url": url,
                "file_addy": None,
                "content": None,
                "size": 0
            }
        return url_data

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        outputLinks = []

        soup = BeautifulSoup(url_data["content"], 'html.parser')
    
        

        for link in soup.find_all('a'):
            relab = link.get('href')

            if(relab == None or len(relab) == 0):
                continue
            elif(relab[:4] == 'http'):
                outputLinks.append(relab)
            else:
                outputLinks.append(urljoin(url_data["url"], relab))

        self.index.start_scan(soup, url_data, len(outputLinks))
        return outputLinks

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        try:
            if ".ics.uci.edu" in parsed.hostname and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|" \
                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                + "|thmx|mso|arff|rtf|jar|csv" \
                + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):

                if parsed.path in self.history:
                    self.traps.append(url)
                    self.history.clear()
                    return False

                directories = parsed.path.split('/')

                if len(directories) == len(set(directories)):
                    if parsed.path not in self.history:
                        self.history.append(parsed.path)

                    return True

            return False

        except TypeError:
            print("TypeError for ", parsed)
            return False

#     def analytics(self):
#         """
#         Writes out to a file the necessary data needed for analytics section
#         """
#         data = open("crawler_analytics.txt", "w")
# 
#         data.write("1. Subdomains visited / URLs processed\n")
#         for sub in self.subdomain.keys():
#             data.write("\t%s: %d\n" % (sub, self.subdomain[sub]))
# 
#         v = list(self.outLinks.values())
#         k = list(self.outLinks.keys())
#         maxed = k[v.index(max(v))]
#         data.write("\n2. Page with most valid out links:\n%s: %d\n" % (maxed, self.outLinks[maxed]))
# 
#         data.write("\n3. Lists of downloaded URLs and traps identified\nURLs:\n%s\n\nTraps:\n%s" % (set(self.outLinks.keys()), set(self.traps)))

