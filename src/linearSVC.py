import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import confusion_matrix, accuracy_score


class LinearSVCMain:
    def __init__(self, phishing_csv_path, legitimate_csv_path):
        self.phishing_csv_path = phishing_csv_path
        self.legitimate_csv_path = legitimate_csv_path

    def main(self):
        phishing_urls = pd.read_csv(self.phishing_csv_path)
        legitimate_urls = pd.read_csv(self.legitimate_csv_path)

        urls = legitimate_urls.append(phishing_urls)

        # drop unnecessary columns
        urls = urls.drop(['Domain', 'Path', 'Protocol', 'Subdomain'], axis=1)

        # shuffling the rows in the dataset so that when splitting the train and test set are equally distributed
        urls = urls.sample(frac=1).reset_index(drop=True)

        legitimate_urls.head(6)
        phishing_urls.head(6)

        # shuffling the rows in the dataset so that when splitting the train and test set are equally distributed
        urls = urls.sample(frac=1).reset_index(drop=True)

        # Removing class variable from the dataset
        urls_without_labels = urls.drop('Label', axis=1)
        urls_without_labels.columns
        labels = urls['Label']

        # splitting the data into train data and test data
        data_train, data_test, labels_train, labels_test = \
            train_test_split(urls_without_labels, labels, test_size=0.30, random_state=110)

        print("Lengths of data trained and data tested", len(data_train), len(data_test), len(labels_train),
              len(labels_test))

        labels_train.value_counts()
        labels_test.value_counts()

        # creating the model and fitting the data into the model
        model = LinearSVC()
        model.fit(data_train, labels_train)

        # Predicting the results for test data
        pred_label = model.predict(data_test)

        # Creating confusion matrix and checking/printing the accuracy
        cm = confusion_matrix(labels_test, pred_label)
        print("LinearSVC Confusion Matrix: ", cm)
        accuracy = accuracy_score(labels_test, pred_label)
        print("LinearSVC Accuracy: ", accuracy)
