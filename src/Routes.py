from flask import Flask, render_template, request
from feature_extraction import FeSingleURL
import pickle
import time

url = ''

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


def predict(to_check):
    fes = FeSingleURL(to_check)
    data = fes.main()
    # for index, row in data.iterrows():
    #    print(row)
    # print("url to check: ", to_check)
    prediction = model.predict(data)
    prediction = prediction[0]
    prob = model.predict_proba(data)
    # print("prob=", prob)
    if prediction == 0:
        prob = prob[0][0]
    else:
        prob = prob[0][1]
    prob = round(prob * 100, 2)
    return prob, prediction


@app.route('/', methods=['POST', 'GET'])
def urltest():
    form = request.form
    if request.method == 'POST':
        url_to_check = request.form['url']
        print("got the url: " + url_to_check)
        start_time = time.time()
        prob, prediction = predict(url_to_check)
        # 0 - not phishing, 1 - phishing
        print("time taken:", (time.time() - start_time))
        print("prediction=", prediction, "prob=", prob)
        return render_template('index.html', prediction=prediction, prob=prob, url_to_check=url_to_check)
    return render_template('index.html', form=form, prediction=-1, prob=-1)


if __name__ == '__main__':
    app.run(debug=True)


    # CODE OFF PYTHONANYWHERE
    # from flask import Flask, render_template, request
    # from src.avoidmain import percentage
    # url = ''


    # app = Flask(__name__)

    # @app.route('/', methods = ['POST', 'GET'])
    # def urltest():
    # 	form = request.form
    # 	if request.method == 'POST':
    # 		form = request.form
    # 		url = request.form['url']
    # 		print("got the url: " + url)
    # 		print("the percentage ", percentage(url))
    # 		percent= percentage(url)
    # 		return render_template('index.html', percent = percent)
    # 	return render_template('index.html', form = form)
    # if __name__ == '__main__':
    # 	app.run()
