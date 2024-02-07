from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.app_context().push()

db = SQLAlchemy(app)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(200), nullable=False)
    total = db.Column(db.Integer(), default=0)
    price = db.Column(db.Integer(), default=0)

    def __repr__(self):
        return '<Inventory %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        items = request.form['item']
        totals = request.form['total']
        prices = request.form['price']
        new_item = Inventory(item=items, total=totals, price=prices)

        try:
            db.session.add(new_item)
            db.session.commit()  
            return redirect('/')  
        except:
            return 'There was a issue bogok'
        
    else:
        item = Inventory.query.order_by(Inventory.price).all()
        return render_template('index.html', items=item)

@app.route('/delete/<int:id>')
def delete(id):
    delete_item = Inventory.query.get(id)

    try:
        db.session.delete(delete_item)
        db.session.commit()
        return redirect('/')
    except:
        return 'Agay'
    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    update_item = Inventory.query.get(id)

    if request.method == 'POST':
        update_item.item = request.form['item']
        update_item.total = request.form['total']
        update_item.price = request.form['price']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There's a Error"


    else:
        return render_template('edit.html', item=update_item)



if __name__ == "__main__":
    app.run(debug=True)