from flask import Flask, request, jsonify
import operator


app = Flask(__name__)
def reverse(func):
    def inner():
        data = request.get_json()
        op = data['op']
        inverse = {"+": "-",
                    "-": "+",
                   "*":"/",
                   "/":"*"}
        data['op'] = inverse[op]

        result = func()
        return result
    return inner
@app.route('/task3', methods = ['POST'])
@reverse #decorated
def calculator():
    data = request.get_json()
    op1 = data['op1']
    op2 = data['op2']
    op = data['op']
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
        }

    op_func = ops[op]

    result = op_func(op1, op2)

    return jsonify('result: ',result)



if __name__ == '__main__':
    app.run(debug=True, port=5001)