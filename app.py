from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

# Sample data
transactions = [
    {"id": 1, "date": "2023-06-01", "amount": 100},
    {"id": 2, "date": "2023-06-02", "amount": -200},
    {"id": 3, "date": "2023-06-03", "amount": 300},
]


@app.get("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


@app.route("/create", methods=["GET", "POST"])
def add_transaction():
    if request.method == "GET":
        return render_template("form.html")
    else:
        date = request.form["date"]
        amount = request.form["amount"]
        transactions.append(
            {
                "id": len(transactions) + 1,
                "date": date,
                "amount": float(amount),
            }
        )
        return redirect(url_for("get_transactions"))


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_transaction(id):
    if request.method == "POST":
        date = request.form["date"]
        amount = float(request.form["amount"])
        for transaction in transactions:
            if transaction["id"] == id:
                transaction["amount"] = amount
                transaction["date"] = date
                return redirect(url_for("get_transactions"))
    for transaction in transactions:
        if transaction["id"] == id:
            return render_template("edit.html", transaction=transaction)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_transaction(id):
    for transaction in transactions:
        if transaction["id"] == id:
            transactions.remove(transaction)
            return redirect(url_for("get_transactions"))


@app.route('/search',methods=["GET","POST"])
def search_transaction():
    if(request.method=='POST'):
        min=float(request.form['min_amount'])
        max=float(request.form['max_amount'])
        transaction_in_range=[]
        for transaction in transactions:
            if(transaction["amount"]>=min and transaction["amount"]<=max):
                transaction_in_range.append(transaction)
        return render_template('transactions.html',transactions=transaction_in_range)
    return render_template('search.html')
        
@app.get('/balance')
def balance_of_transactions():
    total_balance=0
    for transaction in transactions:
        total_balance=total_balance+transaction['amount']

    return render_template('transactions.html',transactions=transactions,total_balance=total_balance)    
# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
