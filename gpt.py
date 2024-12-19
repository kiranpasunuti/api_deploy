from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# Configuration for the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@localhost/spareorders'  # Replace with your DB credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class DummyTest(db.Model):
    __tablename__ = 'spare_order'
    id = db.Column(db.Integer, primary_key=True)
    order_key = db.Column(db.Text)
    row_key = db.Column(db.Text)
    grand_total = db.Column(db.Text)
    discount = db.Column(db.Text)
    status = db.Column(db.Text)
    created_by=db.Column(db.Text)
    # data = db.Column(db.Text)
@app.route('/part_name/<int:id>', methods=['GET'])
def get_part_name(id):
    result = DummyTest.query.filter_by(id=id).first()
    if not result:
        return jsonify({"message": "No data found"}), 404
    response = {
        # "id": result.id,
        "order_key": result.order_key,
        "row_key": result.row_key,
        "grand_total":result.grand_total,
        "discount":result.discount,
        "status":result.status,
        "created_by":result.created_by
        # "data": result.data
    }
    return jsonify(response), 200
@app.route('/part_name', methods=['POST'])
def insert_part_name():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        new_entry = DummyTest(
            id=data.get('id'),
            name=data.get('name'),
            email=data.get('email')
            # data=data.get('data')
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True,port=5020)
