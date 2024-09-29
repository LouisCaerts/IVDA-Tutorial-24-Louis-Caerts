from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .model import Company, Poem, CompanyAnalysis
from .llm.groq_llm import GroqClient
from flask import request
import pandas as pd


# Configure Flask & Flask-PyMongo:
app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
# add your mongodb URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/companiesdatabase"
pymongo = PyMongo(app)
# Get a reference to the companies collection.
companies: Collection = pymongo.db.companies
api = Api(app)


class CompaniesList(Resource):
    def get(self, args=None):
        # retrieve the arguments and convert to a dict
        args = request.args.to_dict()
        print(args)
        # If the user specified category is "All" we retrieve all companies
        if args['category'] == 'All':
            cursor = companies.find()
        # In any other case, we only return the companies where the category applies
        else:
            cursor = companies.find(args)
        # we return all companies as json
        return [Company(**doc).to_json() for doc in cursor]


class Companies(Resource):
    def get(self, id):
        from statsmodels.tsa.ar_model import AutoReg
        # search for the company by ID
        cursor = companies.find_one_or_404({"id": id})
        company = Company(**cursor)
        # retrieve args
        args = request.args.to_dict()
        # retrieve the profit
        profit = company.profit
        # add to df
        profit_df = pd.DataFrame(profit).iloc[::-1]
        if args['algorithm'] == 'random':
            # retrieve the profit value from 2021
            prediction_value = int(profit_df["value"].iloc[-1])
            # add the value to profit list at position 0
            company.profit.insert(0, {'year': 2022, 'value': prediction_value})
        elif args['algorithm'] == 'regression':
            # create model
            model_ag = AutoReg(endog=profit_df['value'], lags=1, trend='c', seasonal=False, exog=None, hold_back=None,
                            period=None, missing='none')
            # train the model
            fit_ag = model_ag.fit()
            # predict for 2022 based on the profit data
            prediction_value = fit_ag.predict(start=len(profit_df), end=len(profit_df), dynamic=False).values[0]
            # add the value to profit list at position 0
            company.profit.insert(0, {'year': 2022, 'value': prediction_value})
        return company.to_json()


class Poem(Resource):
    def get(self, id):
        company_name = self.get_company_name(id)

        if not company_name:
            return {'message': 'Company not found'}, 404

        poem = self.generate_poem(company_name)

        if poem:
            return {'poem': poem}, 200
        else:
            return {'message': 'Failed to generate poem'}, 500

    def get_company_name(self, id):
        cursor = companies.find_one_or_404({"id": id})
        company = Company(**cursor)
        return company.to_json()["name"]

    def generate_poem(self, company_name):
        gc = GroqClient()
        poem = gc.generate_poem(company_name)
        return poem


class CompanyAnalysis(Resource):
    def get(self, id):
        company_name = self.get_company_name(id)
        company_category = self.get_company_category(id)
        company_profits = self.get_company_profits(id)

        if not company_name:
            return {'message': 'Company (name) not found'}, 404
        if not company_category:
            return {'message': 'Company (category) not found'}, 404
        if not company_profits:
            return {'message': 'Company (profits) not found'}, 404

        analysis = self.generate_analysis(company_name, company_category, company_profits)

        if analysis:
            return {'analysis': analysis}, 200
        else:
            return {'message': 'Failed to analyze company'}, 500

    def get_company_name(self, id):
        cursor = companies.find_one_or_404({"id": id})
        company = Company(**cursor)
        return company.to_json()["name"]

    def get_company_category(self, id):
        cursor = companies.find_one_or_404({"id": id})
        company = Company(**cursor)
        return company.to_json()["category"]

    def get_company_profits(self, id):
        cursor = companies.find_one_or_404({"id": id})
        company = Company(**cursor)
        return company.to_json()["profit"]

    def generate_analysis(self, company_name, company_category, company_profits):
        gc = GroqClient()
        analysis = gc.generate_analysis(company_name, company_category, company_profits)
        return analysis


api.add_resource(CompaniesList, '/companies')
api.add_resource(Companies, '/companies/<int:id>')
api.add_resource(Poem, '/llm/groq/poem/<int:id>')
api.add_resource(CompanyAnalysis, '/llm/groq/analysis/<int:id>')