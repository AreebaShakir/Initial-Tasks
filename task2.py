from flask import Flask, request, jsonify
import json
import operator
app = Flask(__name__)
@app.route('/task2', methods = ['POST'])
def calculator():
    data = request.get_json()
    op1 = data['op1']
    op2 = data['op2']
    op = data['op']
    ops = {
        "+": operator.add,
        "-": operator.sub}

    op_func = ops[op]

    result = op_func(op1, op2)

    return jsonify('result: ',result)


if __name__ == '__main__':
    app.run(debug=True, port= 5000)