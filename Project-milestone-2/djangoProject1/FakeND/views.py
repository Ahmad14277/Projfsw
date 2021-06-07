from django.http import HttpResponseRedirect
from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from django import forms


class NewsForm(forms.Form):
    Insert_News = forms.CharField(label='Insert News', max_length=1000)

df = pd.read_csv(r'C:\Users\Ahmad Ali\news.csv')

labels = df.label

x_train, x_test, y_train, y_test = train_test_split(df['text'], labels, test_size=0.2, random_state=7)

tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
tfidf_train = tfidf_vectorizer.fit_transform(x_train)
tfidf_test = tfidf_vectorizer.transform(x_test)
pac = PassiveAggressiveClassifier(max_iter=50)
pac.fit(tfidf_train, y_train)


def fake_news_det(news):
    input_data = [news]
    vectorized_input_data = tfidf_vectorizer.transform(input_data)
    prediction = pac.predict(vectorized_input_data)
    if prediction == "REAL":
        return "True"
    else:
        return "False"


def Home(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            News = form.cleaned_data['Insert_News']
            ans = fake_news_det(News)
            file1 = open("NEWTEXTFILE.txt", "w")
            file1.write(ans)
            file1.close()
            return HttpResponseRedirect('Result/')
    else:
        form = NewsForm()
    return render(request, 'Home.html', {'form': NewsForm()})


def Result(request):
    file1 = open("NEWTEXTFILE.txt", "r")
    ans = file1.read()
    file1.close()
    if ans == "True":
        ans1 = True
    else:
        ans1 = False
    return render(request, 'Result.html', {'Res': ans1})


def About(request):
    return render(request, 'About.html')
