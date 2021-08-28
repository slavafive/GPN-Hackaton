import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html', companies=get_companies(), site_title="Camposha.info")

def get_companies():
    companies = [{'Title':'ООО Реформа', 'Address':'Улица', 'Phone': '+79217777777', 'Email':'email@gmail.com', 'Website':'www.site.com'}, {'Title':'ООО Реформа', 'Address':'Улица', 'Phone': '+79217777777', 'Email':'email@gmail.com', 'Website':'www.site.com'}, {'Title':'ООО Реформа', 'Address':'Улица', 'Phone': '+79217777777', 'Email':'email@gmail.com', 'Website':'www.site.com'}]
    return companies

if __name__ == '__main__':
    app.run(debug=True)