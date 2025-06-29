from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    budget = db.session.query(db.func.sum(Budget.amount)).scalar() or 0
    expenses = Expense.query.all()
    total_expense = sum(e.amount for e in expenses)
    return jsonify({
        'budget': budget,
        'total_expense': total_expense,
        'budget_left': budget - total_expense,
        'expenses': [{'id': e.id, 'title': e.title, 'amount': e.amount} for e in expenses]
    })

@app.route('/api/add_budget', methods=['POST'])
def add_budget():
    amount = float(request.json['amount'])
    db.session.add(Budget(amount=amount))
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/api/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    db.session.add(Expense(title=data['title'], amount=float(data['amount'])))
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/api/delete_expense/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return jsonify({'status': 'deleted'})

@app.route('/api/reset_budget', methods=['DELETE'])
def reset_budget():
    Budget.query.delete()
    db.session.commit()
    return jsonify({'status': 'budget_reset'})

if __name__ == '__main__':
    with app.app_context():       
        db.create_all()
    app.run(debug=True)

