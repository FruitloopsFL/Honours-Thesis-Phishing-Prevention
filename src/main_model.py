from feature_extraction import FeMain, FeSingleURL
from random_forest import RandomForestMain
from decision_tree import DecisionTreeMain
from logistic_reg import LogisticRegMain
from naive_bayes import NaiveBayesMain
from adaboost import AdaBoostMain
from knn import KNNMain
from linearSVC import LinearSVCMain
import os
import time

def initialise():
    os.makedirs('../extracted_csv_files/', exist_ok=True)

    # path constants
    INPUT_PHISHING_PATH = '../raw_datasets/data_phishing_2000.csv'
    INPUT_LEGITIMATE_PATH = '../raw_datasets/data_legitimate_2000.csv'
    OUTPUT_PATH = '../extracted_csv_files/'

    # QUICK WAY (use if csv's are already extracted and compiled) 

    # run random forest on generated output files
    # global rf
    # rf = RandomForestMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
    # dt = DecisionTreeMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
    # lr = LogisticRegMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
    # nb = NaiveBayesMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
    # ab = AdaBoostMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
    global knn 
    knn = KNNMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')
    # lsvc = LinearSVCMain('../extracted_csv_files/phishing-urls.csv', '../extracted_csv_files/legitimate-urls.csv')

    # # LONG WAY (use if csv's haven't been extracted or to run with a different dataset specified in path constants)
    # # run random forest on generated output files
    # # instantiate feature extraction main object
    # fe = FeMain(INPUT_PHISHING_PATH, INPUT_LEGITIMATE_PATH, OUTPUT_PATH)

    # # run feature extraction on raw phishing URLs data file
    # fe.main(bool_phishing=True)
    # # run feature extraction on raw legitimate URLs data file
    # fe.main(bool_phishing=False)

    # run algorithms on generated output files
    # rf = RandomForestMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
    # dt = DecisionTreeMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
    # lr = LogisticRegMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
    # nb = NaiveBayesMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
    # ab = AdaBoostMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
    # knn = KNNMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)
    # lsvc = LinearSVCMain(fe.output_phishing_file.name, fe.output_legitimate_file.name)


    # KNN was chosen as it had the highest accuracy rate and we only need a single model to be used
    # rf.main()
    # dt.main() 
    # lr.main()
    # nb.main()
    # ab.main()
    knn.main()
    # lsvc.main()


# url = "https://www.google.com/"
# url = "google.com"

# feSingle = FeSingleURL(url)
# testDF = feSingle.main()
# # print(testDF)
# result = knn.test(testDF)

# if (result == [0]):
#     result = "Legit website"
# else:
#     result = "Phishing website"
# print(result)




def eval(url):
    feSingle = FeSingleURL(url)
    testDF = feSingle.main()

    result = knn.test(testDF)

    # if (result == [0]):
    #     result = "Legit website"
    # else:
    #     result = "Phishing website"
    return result[0]


# Used for testing

# start = time.perf_counter()
# initialise()
# end = time.perf_counter()
# print(f"Time taken to initialise: {end - start:0.4f} seconds")
# url = "https://steamcommumity.co/profiles/thenumberone"
# print(eval(url))
    