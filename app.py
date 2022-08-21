from flask import Flask, json
from flask_restful import Api, Resource, request
from model import Model
import sys

datamodelcfg = {
    "product_id": "id",
    "name": "name",
    "props": "props",
    "reference_id": "reference_id"
}

app = Flask(__name__)

api = Api(app)

app.debug = True

predict_model = Model()
predict_model.fit('agora_hack_products.json')

def LookUpForId(productstr):
    # json_file = open('agora_hack_products.json')
    return predict_model.predict(json.dumps(productstr))

class ProductMatch(Resource):        
    def post(self):


        final_json = LookUpForId(request.json)

        response = app.response_class(
            response = final_json,
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