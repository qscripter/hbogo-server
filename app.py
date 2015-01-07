from flask import Flask
from flask import jsonify
from hbo_fetch import HboCatalog
from decorators import *

app = Flask(__name__)
catalog = HboCatalog('http://catalog.lv3.hbogo.com/apps/mediacatalog/rest/productBrowseService/HBO/category/INDB487')


@app.route('/catalog.json')
@jsonp
def catalog_json():
  return jsonify({'data': catalog.features})


if __name__ == "__main__":
  app.run(debug=True)