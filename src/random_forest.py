import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import numpy as np
import pickle


class RandomForestMain:
    def __init__(self, phishing_csv_path, legitimate_csv_path):
        self.phishing_csv_path = phishing_csv_path
        self.legitimate_csv_path = legitimate_csv_path

    def main(self):
        phishing_urls = pd.read_csv(self.phishing_csv_path)
        legitimate_urls = pd.read_csv(self.legitimate_csv_path)

        # have to merge the two files together
        urls = legitimate_urls.append(phishing_urls)

        # drop unnecessary columns
        urls = urls.drop(['Domain', 'Path', 'Protocol', 'Subdomain'], axis=1)

        # shuffling the rows in the dataset so that when splitting the train and test set are equally distributed
        urls = urls.sample(frac=1).reset_index(drop=True)

        urls_without_labels = urls.drop('Label', axis=1)
        labels = urls['Label']

        data_train, data_test, labels_train, labels_test = \
            train_test_split(urls_without_labels, labels, test_size=0.30, random_state=110)

        random_forest_classifier = RandomForestClassifier()
        random_forest_classifier.fit(data_train, labels_train)

        prediction_label = random_forest_classifier.predict(data_test)
        confusion_matrix_ = confusion_matrix(labels_test, prediction_label)

        print("Random Forest Confusion Matrix: ", confusion_matrix_)

        accuracy = accuracy_score(labels_test, prediction_label)
        print("Random Forest Accuracy: ", accuracy)

        feature_importances = random_forest_classifier.feature_importances_
        indices = np.argsort(feature_importances)[::1]

        # print feature importances
        for i in range(data_train.shape[1]):
            print(i+1, '. ', data_train.columns[indices[i]], ' : ', feature_importances[indices[i]])

        # Plot the feature importances of the forest
        plt.rcParams.update({'font.size': 14})
        plt.figure()
        plt.title("Feature importance for random forest")
        plt.bar(range(data_train.shape[1]), feature_importances[indices],
               color="g", align="center")

        plt.xticks(range(data_train.shape[1]), data_train.columns[indices], rotation = 45)
        plt.xlim([-1, data_train.shape[1]])
        plt.show()

        # Saving model to disk
        pickle.dump(random_forest_classifier, open('model.pkl', 'wb'))
