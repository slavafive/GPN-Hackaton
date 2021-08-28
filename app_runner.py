from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    key_words = request.args.get('text')
    if key_words == None:
        #Код обучения
    else:
        #query()
    print(key_words)
    return render_template('index.html', companies=get_companies(key_words))

def get_companies(key_words):
    companies = [{'Title':f'ООО {key_words}', 'Address':'Улица', 'Phone': '+79217777777', 'Email':'email@gmail.com', 'Website':'www.site.com'}, {'Title':'ООО Реформа', 'Address':'Улица', 'Phone': '+79217777777', 'Email':'email@gmail.com', 'Website':'www.site.com'}, {'Title':'ООО Реформа', 'Address':'Улица', 'Phone': '+79217777777', 'Email':'email@gmail.com', 'Website':'www.site.com'}]
    return companies

if __name__ == '__main__':
    app.run(debug=True)