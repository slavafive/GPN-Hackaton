import pandas as pd
import numpy as np
import json
from sklearn.neighbors import KNeighborsClassifier as kNN
from ml.vectorizer import vectorize_text


with open('../data/companies.json') as file:
    companies = json.load(file)

df_google = pd.read_csv('../data/vec_google.csv')
df_rbk = pd.read_csv('../data/vec_rbk.csv')
df = pd.concat([df_google, df_rbk]).sort_values(by=['name']).reset_index(drop=True)
df = df_rbk.sort_values(by=['name']).reset_index(drop=True)

features = [feature for feature in df.columns.values if feature.isdigit()]
target = 'name'

X = df[features]
y = df[target]
model = kNN(n_neighbors=25, metric='euclidean')
model.fit(X, y)


def cosine(x, y):
    return np.dot(x, y) / np.sqrt(np.linalg.norm(x) * np.linalg.norm(y))


def get_top_company_by_text(text):
    text = vectorize_text(text)
    pred = model.predict([text])
    return pred[0]


def predict_top_n_companies_by_text(text, n):
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
                'address': company.get('address')
            }
            if company_info.get('phone') is not None:
                company_info['phone'] = company_info['phone'].replace(' ', '')
    return company_info


def query(text, n=3, k=30):
    top_n_list = list(predict_top_n_companies_by_text(text=text, n=k)[0])
    top_n_companies = get_top_n_companies_from_list(top_n_list, n=n)
    companies_info = []
    for company_name in top_n_companies:
        companies_info.append(get_info_by_company(company_name))
    return companies_info


print(query(text='Нефть газ россия газпром национальное достояние'))
