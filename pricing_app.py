from parse_inputs import calculate_inputs
from flask import Flask,render_template,request
import datetime

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])

def index():
    stock = ''
    expiry = ''
    strike_price = ''
    result = ''
    if request.method=="POST" and 'stock' in request.form and 'expiry' in request.form and 'strike_price' in request.form:
        stock = str(request.form.get('stock'))
        expiry = datetime.datetime.strptime(request.form.get('expiry'),'%Y-%m-%d').date()
        strike_price = float(request.form.get('strike_price'))
        # print(type(expiry))
        clean_inputs = calculate_inputs(stock,expiry,strike_price)
        result = clean_inputs.price()
        print(result)
        
    return render_template('index.html',stock=stock,expiry=expiry,strike_price=strike_price,result=result)

if __name__ == '__main__':
    app.run(debug=True,port=5001)