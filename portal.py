from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import urllib
import re


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/store/portal/portal.db'
db = SQLAlchemy(app)


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String)
    version = db.Column(db.String)
    ref = db.Column(db.Integer)
    date = db.Column(db.String)
    html = db.Column(db.Text)
    scenarios = db.Column(db.Integer)
    scen_fail = db.Column(db.Integer)
    scen_pass = db.Column(db.Integer)
    steps = db.Column(db.Integer)
    step_fail = db.Column(db.Integer)
    step_pass = db.Column(db.Integer)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/list/')
def list():
    list = None
    list = Result.query.order_by(Result.date).all()
    return render_template('list.html', list=list)


@app.route('/show/<int:id>')
def show(id=None):
    res = None
    if id:
        res = Result.query.get(id)
        if res:
            return res.html


@app.route('/add/')
@app.route('/add/<path:url>')
def add(url=None):
    product = None
    version = None
    ref = False
    date = None
    html = None
    if url is not None:
        if url.find('SM') >= 0:
            product = 'suma'
        if url.find('SM1.7') >= 0:
            version = '1.7'
        if url.find('SM2.1') >= 0:
            version = '2.1'
        if url.find('SM-head') >= 0:
            version = 'head'
        if url.find('REF') >= 0:
            ref = True
        #a.split('/')[-1][0:16].replace('_', '-').split('-')
        date = url.split('/')[-1][0:16]
        html = urllib.urlopen(url).read()
        stats = get_stats(html)
        res = Result(product=product,
                     version=version,
                     ref=ref,
                     date=date,
                     html=html,
                     scenarios=stats[0],
                     scen_fail=stats[1],
                     scen_pass=stats[2],
                     steps=stats[3],
                     step_fail=stats[4],
                     step_pass=stats[5])

        db.session.add(res)
        db.session.commit()
        return html
    else:
        return "Error"

def get_stats(html):
    results = []
    fail = False
    tmp = re.search('\d{1,4}\sscenarios.*\)";', html).group()
    list = re.sub(r'[^a-zA-Z0-9]', ' ', tmp).split()
    list.remove('br')
    if 'failed' in list:
        fail = True
    results.append(list[0])
    if fail:
        results.append(list[2])
        results.append(list[4])
    else:
        results.append(0)
        results.append(list[2])
    if fail:
        results.append(list[6])
        results.append(list[8])
        results.append(list[10])
    else:
        results.append(list[4])
        results.append(0)
        results.append(list[6])
    return results

if __name__ == '__main__':
    host = '0.0.0.0'
    app.debug = True
    app.run(host)
