from flask import Flask, Response
# from analysis import loadData, createChart, showTopWords
from analysis import loadData, createChart

#  = loadData(zipcode)
app = Flask(__name__, static_url_path='', static_folder='.')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

@app.route('/vis/<zipcode>')
def visualize(zipcode):
    df = loadData(zipcode)
    response = ''
    if df is not None:
        #response = showTopWords(df[df.rating==rating]['content']).to_json()
        response = createChart(df, zipcode).to_json()

    return Response(response,
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

if __name__ == '__main__':
    app.run(port=8002)
