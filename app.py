import os
# from functions_internal import check_firefox_version, compare_versions, take_data
# print(os.environ['PATH'])
from helpers import crawl_data
from flask import Flask, render_template
from helpers import fetch_sreality_data

# check_firefox_version() -- check firefox version
# compare_versions() -- if needed to debug the browser version

# crawl the data
crawl_data()

# using Flask to render the data
app = Flask(__name__)

@app.route('/')
def home():
    data = fetch_sreality_data()
    return render_template('app.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)