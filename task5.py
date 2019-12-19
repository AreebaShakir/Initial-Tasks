from flask import Flask, request, jsonify
import json
import operator
from bson.json_util import dumps
import pymongo
from flask import request
app = Flask(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")  # create client
db = client["my_database"]  # create database
new_collection = db["calc"]  # collection calculations
second_collection = db["lastOperations"]  # collections last operations


@app.route('/task5', methods = ['POST'])
def insertion():
    data = request.get_json() #extracting json data
    op1 = data['op1']
    op2 = data['op2']
    op = data['op']
    #specifying operations
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
        }

    op_func = ops[op]
    result = op_func(op1,op2)
    my_dict = {'op1': op1, 'op2': op2, 'op': op, 'result': result} #create dictionary
    new_collection.insert_one(my_dict) #insert in collection

    new_list = []
    for record in new_collection.find({}):
        new_list.append({"op": record['op'], 'first  operand': record['op1'], 'second operand': record['op2'], 'third operand': record['op'], 'Result': record['result']})
   #work for last operations collection
    operators_dict = {
     "op" :op, "values" : {'op1':op1, 'op2': op2, 'op': op, 'result': result}}
    if second_collection.count({"op": op}) == 0: #check if there is no record for that operation
        second_collection.insert(operators_dict)

    else: #if record exist then update
        second_collection.update({"op": op}, {"$set": {'values.op1':op1, 'values.op2': op2, 'values.op': op, 'values.result': result}})
    for rec in second_collection.find({}):
        print("Last operations", rec)

    return jsonify("Result is",result)

@app.route('/getcalc', methods = ['GET'])
def get_calculations():
    out=[]
    for records in new_collection.find({}):
        out.append({'op1': records['op1'], 'op2': records['op2'], 'op': records['op'], 'result': records['result']})
    total = new_collection.count()#calculate number of records
    return jsonify ("All Records", out, "Total records", total)

if __name__ == '__main__':
    app.run(debug=True, port= 5003)
