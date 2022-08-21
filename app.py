from flask import Flask, json
from flask_restful import Api, Resource, request
from model import Model
import sys

datamodelcfg = {
    "product_id": "product_id",
    "name": "name",
    "props": "props",
    "reference_id": "reference_id"
}

app = Flask(__name__)

api = Api(app)

app.debug = True

def LookUpForId(productstr):
    predict_model = Model()
    predict_model.fit('agora_hack_products.json') 
    return predict_model.predict(productstr)

class ProductMatch(Resource):        
    def post(self):
        data = []
        length = len(request.json)
        for i in range(length):
            app.logger.info(i)
            productstr = request.json
            isproperstr = True


            reference_id = LookUpForId(productstr)
            idstr = datamodelcfg["product_id"]
            data.append({idstr: productstr[idstr], 
            datamodelcfg["reference_id"]: reference_id,} if isproperstr else {})

        response = app.response_class(
            response = json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response

# class predict(Resource):
#     def post(self):
#         predict_model = Model.fit('agora_hack_products.json')

api.add_resource(ProductMatch, '/match_products')
# api.add_resource(ProductMatch, '/predict')

if __name__ == '__main__':
    app.run(host='localhost', port=8100)