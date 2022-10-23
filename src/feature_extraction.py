# File for performing feature extraction on given urls
from urllib.parse import urlparse
import urllib.request
from urllib.error import HTTPError
import pandas as pd
from bs4 import BeautifulSoup
import tldextract
from data_preprocessing.main import DataPreprocessing
import re
import time


def word_length_list(word_list):
    return [len(word) for word in word_list]


# SCALE: 0 - Not phishing, 1 - phishing, 2 - suspicious
class FeatureExtraction:
    def __init__(self):
        pass

    def get_protocol(self, url):
        return urlparse(url).scheme

    def get_domain(self, url):
        return tldextract.extract(url).domain

    def get_path(self, url):
        return urlparse(url).path

    def get_suffix(self, url):
        return tldextract.extract(url).suffix

    def get_subdomain(self, url):
        return tldextract.extract(url).subdomain

    # checks URL length, phishing urls typically have greater length
    def url_length(self, url):
        if len(url) < 54:
            return 0  # legitimate
        elif 54 <= len(url) <= 75:
            return 2  # suspicious
        else:
            return 1  # phishing

    def domain_length(self, url):
        domain_length = len(self.get_domain(url))
        if domain_length < 10:
            return 0
        else:
            return 1

    def has_IP(self, url):
        match = re.search('(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  #IPv4
                    '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)'  #IPv4 in hexadecimal
                    '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',url)     #Ipv6
        if match:
            return 1            # phishing
        else:
            return 0            # legitimate

    def uses_HTTPS(self, url):
        protocol = self.get_protocol(url).upper()
        if protocol == 'HTTPS':
            return 1
        else:
            return 0

    def subdomain_length(self, url):
        subdomain_length = len(self.get_subdomain(url))
        if 0 < subdomain_length < 10:
            return 0
        elif 10 <= subdomain_length < 17:
            return 2
        else:
            return 1

    def path_length(self, url):
        path_length = len(self.get_path(url))
        if path_length == 1:
            return 0
        elif 2 <= path_length < 16:
            return 2
        else:
            return 1

    # check number of subdomains in URL, more than 3 likely phishing
    def num_sub_domains(self, url):
        if self.get_domain(url).count(".") == 0:
            return 0  # legitimate
        else:
            return 1  # phishing

    # check Alexa rank
    def alexa_rank(self, url):
        try:
            rank = \
                BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(),
                              "xml").find("REACH")['RANK']
        except TypeError:
            return 1
        except HTTPError:
            return 2
        rank = int(rank)
        if rank < 100000:
            return 0
        else:
            return 2

    def known_tld(self, url):
        suffix = self.get_suffix(url)
        if suffix in open('../input/known_tld.txt').read():
            return 1
        else:
            return 0

    def brand_name_count(self, count):
        return 1 if count >= 1 else 0

    def similar_brand_count(self, count):
        return 0 if count < 1 else 0

    def brand_check(self, url):
        domain = self.get_domain(url)
        return 0 if domain in open('../input/brands.txt').read() else 1

    def random_word_count(self, count):
        if count <= 3:
            return 0
        elif 3 < count < 5:
            return 2
        else:
            return 1

    def keyword_count(self, count):
        if count <= 2:
            return 2
        elif count > 5:
            return 1
        else:
            return 0

    def similar_keyword_count(self, count):
        return 0 if count < 1 else 1

    def other_word_count(self, count):
        return 0 if count < 2 else 1

    def raw_word_count(self, count):
        return 0 if count < 4 else 1

    def word_length_list(self, word_list):
        return [len(word) for word in word_list]

    def avg_word_len(self, word_list):
        word_len_list = word_length_list(word_list)
        avg_word_len = sum(word_len_list) / len(word_list)
        if avg_word_len < 9:
            return 0
        elif 9 <= avg_word_len < 12:
            return 2
        else:
            return 1

    def longest_word_len(self, word_list):
        word_len_list = word_length_list(word_list)
        max_len = max(word_len_list)
        if max_len > 11:
            return 1
        else:
            return 0

    def shortest_word_len(self, word_list):
        word_len_list = word_length_list(word_list)
        min_len = min(word_len_list)
        if min_len < 3:
            return 1
        else:
            return 0

    def random_domain(self, bool_rand):
        return 0 if bool_rand else 1

    def special_chars(self, url):
        domain = self.get_domain(url)
        subdomain = self.get_subdomain(url)
        domain_chars = len(domain) - len(re.findall('[\w]', domain))
        subdomain_chars = len(subdomain) - len(re.findall('[\w]', subdomain))
        special_char_count = domain_chars + subdomain_chars
        if special_char_count < 2:
            return 0
        elif 2 <= special_char_count < 4:
            return 2
        else:
            return 1



class FeSingleURL:
    def __init__(self, url_to_check):
        self.url_to_check = url_to_check

    def main(self):
        # create feature extraction object
        fe = FeatureExtraction()
        dp = DataPreprocessing()
        
        url = self.url_to_check
        url_length = fe.url_length(url)
        subdomain_length = fe.subdomain_length(url)
        path_length = fe.path_length(url)
        domain_length = fe.domain_length(url)
        num_sub_domains = fe.num_sub_domains(url)
        has_ip = fe.has_IP(url)
        uses_https = fe.uses_HTTPS(url)
        # alexa_rank = fe.alexa_rank(url)
        known_tld = fe.known_tld(url)
        # from the data preprocessing module
        dp.main(url)
        brand_name_count = fe.brand_name_count(dp.brand_name_count)
        similar_brand_count = fe.similar_brand_count(len(dp.similar_brand_list))
        similar_keyword_count = fe.similar_keyword_count(len(dp.similar_keyword_list))
        brand_check = fe.brand_check(url)
        random_word_count = fe.random_word_count(dp.random_word_count)
        random_domain_check = fe.random_domain(dp.has_random_domain)
        keyword_count = fe.keyword_count(dp.keyword_count)
        other_word_count = fe.other_word_count(len(dp.found_word_list))
        raw_word_count = fe.raw_word_count(dp.raw_word_count)
        avg_word_len = fe.avg_word_len(dp.raw_word_list)
        longest_word_len = fe.longest_word_len(dp.raw_word_list)
        shortest_word_len = fe.shortest_word_len(dp.raw_word_list)
        special_chars = fe.special_chars(url)
        d = {'URL len': pd.Series(url_length), '#SC': pd.Series(special_chars),
             'Domain len': pd.Series(domain_length), 'Subdomain len': pd.Series(subdomain_length),
             'Path len': pd.Series(path_length), '#Subdomains': pd.Series(num_sub_domains),
             'IP': pd.Series(has_ip), 'HTTPS': pd.Series(uses_https),
            #  'Alexa': pd.Series(alexa_rank), 
             'Known TLD': pd.Series(known_tld),
             '#Brand': pd.Series(brand_name_count), '#Similar brand': pd.Series(similar_brand_count),
             '#Similar keyword': pd.Series(similar_keyword_count), 'Brand check': pd.Series(brand_check),
             '#Random word': pd.Series(random_word_count), 'Random domain': pd.Series(random_domain_check),
             '#Keyword': pd.Series(keyword_count), '#Other word': pd.Series(other_word_count),
             '#Raw word': pd.Series(raw_word_count), 'Avg word len': pd.Series(avg_word_len),
             'Long word len': pd.Series(longest_word_len), 'Short word len': pd.Series(shortest_word_len)}
        # print("add to DF")
        data = pd.DataFrame(d)
        return data


class FeMain:
    def __init__(self, input_phishing_path, input_legitimate_path, output_folder_path):
        self.input_phishing_path = input_phishing_path
        self.input_legitimate_path = input_legitimate_path
        self.output_folder_path = output_folder_path
        self.output_phishing_file = open("{path}{name}.csv".format(path=self.output_folder_path,
                                                                   name='phishing-urls'), 'w')
        self.output_legitimate_file = open("{path}{name}.csv".format(path=self.output_folder_path,
                                                                     name='legitimate-urls'), 'w')

    def main(self, bool_phishing):
        if bool_phishing:
            input_data_path = self.input_phishing_path
            output_file = self.output_phishing_file
            output_analysis_file = '../extracted_csv_files/analysis_data_phishing.csv'
        else:
            input_data_path = self.input_legitimate_path
            output_file = self.output_legitimate_file
            output_analysis_file = '../extracted_csv_files/analysis_data_legitimate.csv'

        raw_data = pd.read_csv(input_data_path, header=None, names=['urls'], nrows=3000)

        # features
        protocol = []
        domain = []
        subdomain = []
        path = []
        domain_length = []
        subdomain_length = []
        path_length = []
        url_length = []
        num_sub_domains = []
        has_ip = []
        uses_https = []
        # alexa_rank = []
        known_tld = []
        brand_name_count = []
        similar_brand_count = []
        brand_check = []
        random_word_count = []
        random_domain_check = []
        keyword_count = []
        similar_keyword_count = []
        other_word_count = []
        raw_word_count = []
        avg_word_len = []
        shortest_word_len = []
        longest_word_len = []

        path_length_ = []
        url_length_ = []
        domain_length_ = []
        num_sub_domains_ = []
        subdomain_length_ = []
        brand_name_count_ = []
        random_word_count_ = []
        has_random_domain = []
        keyword_count_ = []
        similar_keyword_count_ = []
        other_word_count_ = []
        raw_word_count_ = []
        avg_word_len_ = []
        longest_word_len_ = []
        shortest_word_len_ = []
        similar_brand_count_ = []
        raw_word_stdev = []
        special_chars = []

        # create feature extraction object
        fe = FeatureExtraction()
        dp = DataPreprocessing()

        time_count = 0
        for i in range(0, len(raw_data["urls"])):
            start_time = time.time()
            url = raw_data["urls"][i]
            print('Extracting features for ', i, ':', url)
            protocol.append(fe.get_protocol(url))
            path.append(fe.get_path(url))
            domain.append(fe.get_domain(url))
            subdomain.append(fe.get_subdomain(url))
            url_length.append(fe.url_length(url))
            subdomain_length.append(fe.subdomain_length(url))
            path_length.append(fe.path_length(url))
            domain_length.append(fe.domain_length(url))

            num_sub_domains.append(fe.num_sub_domains(url))
            has_ip.append(fe.has_IP(url))
            uses_https.append(fe.uses_HTTPS(url))
            # alexa_rank.append(fe.alexa_rank(url))
            known_tld.append(fe.known_tld(url))

            # from the data preprocessing module
            dp.main(url)
            brand_name_count.append(fe.brand_name_count(dp.brand_name_count))
            similar_brand_count.append(fe.similar_brand_count(len(dp.similar_brand_list)))
            similar_keyword_count.append(fe.similar_keyword_count(len(dp.similar_keyword_list)))
            brand_check.append(fe.brand_check(url))
            random_word_count.append(fe.random_word_count(dp.random_word_count))
            random_domain_check.append(fe.random_domain(dp.has_random_domain))
            keyword_count.append(fe.keyword_count(dp.keyword_count))
            other_word_count.append(fe.other_word_count(len(dp.found_word_list)))
            raw_word_count.append(fe.raw_word_count(dp.raw_word_count))
            avg_word_len.append(fe.avg_word_len(dp.raw_word_list))
            longest_word_len.append(fe.longest_word_len(dp.raw_word_list))
            shortest_word_len.append(fe.shortest_word_len(dp.raw_word_list))
            special_chars.append(fe.special_chars(url))

            # for analysis
            path_length_.append(len(fe.get_path(url)))
            url_length_.append(len(url))
            domain_length_.append(len(fe.get_domain(url)))
            num_sub_domains_.append(fe.get_domain(url).count("."))
            brand_name_count_.append(dp.brand_name_count)
            random_word_count_.append(dp.random_word_count)
            has_random_domain.append(dp.has_random_domain)
            keyword_count_.append(dp.keyword_count)
            similar_keyword_count_.append(len(dp.similar_keyword_list))
            other_word_count_.append(len(dp.found_word_list))
            raw_word_count_.append(dp.raw_word_count)
            subdomain_length_.append(len(fe.get_subdomain(url)))
            raw_word_stdev.append(dp.raw_word_stdv)

            word_lens = fe.word_length_list(dp.raw_word_list)
            avg_word = sum(word_lens) / len(word_lens)
            avg_word_len_.append(avg_word)
            longest_word_len_.append(max(word_lens))
            shortest_word_len_.append(min(word_lens))
            similar_brand_count_.append(len(dp.similar_brand_list))

            total_time = time.time() - start_time
            time_count += total_time
            print("--- %s seconds ---" % total_time)

        label = [1 if bool_phishing is True else 0 for _ in range(0, len(raw_data["urls"]))]

        d = {'Protocol': pd.Series(protocol), 'Domain': pd.Series(domain), 'Path': pd.Series(path),
             'Subdomain': pd.Series(subdomain), 'URL len': pd.Series(url_length),
             'Domain len': pd.Series(domain_length), 'Subdomain len': pd.Series(subdomain_length),
             'Path len': pd.Series(path_length), '#Subdomains': pd.Series(num_sub_domains),
             'IP': pd.Series(has_ip), 'HTTPS': pd.Series(uses_https),
            #  'Alexa': pd.Series(alexa_rank), 
             'Known TLD': pd.Series(known_tld),
             '#Brand': pd.Series(brand_name_count), '#Similar brand': pd.Series(similar_brand_count),
             '#Similar keyword': pd.Series(similar_keyword_count), 'Brand check': pd.Series(brand_check),
             '#Random word': pd.Series(random_word_count), 'Random domain': pd.Series(random_domain_check),
             '#Keyword': pd.Series(keyword_count), '#Other word': pd.Series(other_word_count),
             '#Raw word': pd.Series(raw_word_count), 'Avg word len': pd.Series(avg_word_len),
             'Long word len': pd.Series(longest_word_len), 'Short word len': pd.Series(shortest_word_len),
             '#SC': pd.Series(special_chars), 'Label': pd.Series(label)}

        data = pd.DataFrame(d)
        data.to_csv(output_file, index=False, encoding='UTF-8')

        print("AVG TIME PER URL (s): ", (time_count / len(raw_data["urls"])))

        # analysis data

        da = {'Protocol': pd.Series(protocol), 'Domain': pd.Series(domain), 'Path': pd.Series(path),
              'Subdomain': pd.Series(subdomain), 'Path len': pd.Series(path_length_), 'URL len': pd.Series(url_length_),
              'Dom len': pd.Series(domain_length_), 'Sbd len': pd.Series(subdomain_length_),
              '# SBD': pd.Series(num_sub_domains_), '#Brands': pd.Series(brand_name_count_),
              '#SimBrs': pd.Series(similar_brand_count_), '#Key': pd.Series(keyword_count_),
              '#SimKey': pd.Series(similar_keyword_count_), '#Rand': pd.Series(random_word_count_),
              'RandD': pd.Series(has_random_domain), '#Oth': pd.Series(other_word_count_),
              '#Raw': pd.Series(raw_word_count_), 'AvgWL': pd.Series(avg_word_len_),
              'MaxWL': pd.Series(longest_word_len_), 'MinWL': pd.Series(shortest_word_len_),
              'STDV': pd.Series(raw_word_stdev),
              'Label': pd.Series(label)}

        analysis_data = pd.DataFrame(da)
        analysis_data.to_csv(output_analysis_file, index=False, encoding='UTF-8')