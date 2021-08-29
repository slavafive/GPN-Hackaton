import pandas as pd
import numpy as np
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier as kNN
from ml.vectorizer import vectorize_text
from python_scripts.text_processing import clean_text

with open('../data/companies.json') as file:
    companies = json.load(file)


TFIDF = False

df_text = pd.read_csv('../data/companies.csv').rename(columns={'corpus': 'text'})
df = pd.read_csv('../data/vec_rbk.csv').merge(df_text, on='name').sample(frac=1).reset_index(drop=True)

if TFIDF:
    corpus = []
    for company in companies:
        activities = []
        for activity in company['activities']:
            activities.append(activity['description'])
        activities = ' '.join(activities)
        corpus.append(activities)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus).toarray()
    features = vectorizer.get_feature_names()
else:
    features = [feature for feature in df.columns.values if feature.isdigit()]
    X = df[features]

target = 'name'

y = df[target]
model = kNN(n_neighbors=30, metric='euclidean')
model.fit(X, y)


def get_top_company_by_text(text):
    text = clean_text(text, normalize=True)
    text = vectorize_text(text)
    pred = model.predict([text])
    return pred[0]


def predict_top_n_companies_by_text(text, n):
    if TFIDF:
        text = vectorizer.transform([text]).toarray()[0]
    else:
        text = vectorize_text(text)
    probs = model.predict_proba([text])
    best_n = np.argsort(probs, axis=1)[:, -n:]
    return best_n


def get_top_n_companies_from_list(top_n_list, n):
    df_top = df.iloc[top_n_list]
    return list(df_top.name)[-n:]


def get_info_by_company(company_name):
    company_info = None
    for company in companies:
        if company_name == company['name']:
            company_info = {
                'name': company.get('name'),
                'link': company.get('link'),
                'email': company.get('email'),
                'phone': company.get('phone'),
                'address': company.get('address'),
                'activities': company.get('activities')
            }
            if company_info.get('phone') is not None:
                company_info['phone'] = company_info['phone'].replace(' ', '')
    return company_info


def get_df_top_with_scores(df_top, text):
    text = text.lower()
    if re.search('or', text, re.IGNORECASE):
        text_parts = re.split('or', text, flags=re.IGNORECASE)
        operator = 'or'
    elif re.search('and', text, re.IGNORECASE):
        text_parts = re.split('and', text, flags=re.IGNORECASE)
        operator = 'and'
    else:
        df_top['scores'] = 0
        return
    text_parts = list(map(str.strip, text_parts))
    scores = []
    for index, row in df_top.iterrows():
        score = 0
        try:
            if operator == 'or':
                for text_part in text_parts:
                    if text_part in df_top.loc[index, 'text']:
                        score += 1
            elif operator == 'and':
                score = 1
                for text_part in text_parts:
                    if text_part not in df_top.loc[index, 'text']:
                        score = 0
                        break
        except Exception as e:
            pass
        scores.append(score)
    df_top['scores'] = scores
    return df_top


def query(text, n=3, k=100):
    if re.search('or', text, re.IGNORECASE) and re.search('and', text, re.IGNORECASE):
        return 'Неправильный формат ввода'
    top_n_list = list(predict_top_n_companies_by_text(text=text, n=k)[0])
    df_top = df.iloc[top_n_list]
    df_top = get_df_top_with_scores(df_top, text)
    scores = list(df_top['scores'])
    top_scores_indices = list(np.argsort(scores)[-n:])
    top_n_companies = list(df_top.iloc[top_scores_indices]['name'])
    companies_info = []
    for company_name in top_n_companies:
        companies_info.append(get_info_by_company(company_name))
    return companies_info


print(query(text='уголь or древесина or машина'))
