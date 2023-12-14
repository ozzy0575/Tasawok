from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shoppinglist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ShoppingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    weight_quantity = db.Column(db.String(80), nullable=False)
    person = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(80), nullable=False)
    processed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Item %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        item = ShoppingItem(
            name=request.form['name'],
            weight_quantity=request.form['weight_quantity'],
            person=request.form['person'],
            price=float(request.form['price']),  # Ensure correct data type
            location=request.form['location']

        )
        db.session.add(item)
        db.session.commit()

    items = ShoppingItem.query.all()  # Retrieve all items from the database
    return render_template('index.html', shopping_list=items)
# Route to delete an item
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    item = ShoppingItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('home'))

# Route to mark an item as processed
@app.route('/process/<int:item_id>')
def process_item(item_id):
    item = ShoppingItem.query.get_or_404(item_id)
    item.processed = not item.processed  # Toggle the processed state
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
