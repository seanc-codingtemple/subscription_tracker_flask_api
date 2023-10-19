from flask import  request, jsonify
from firebase_admin import  auth

from app import db


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    service = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String(255))

    def __init__(self, user_id, service, cost, start_date, renewal_date, notes):
        self.user_id = user_id
        self.service = service
        self.cost = cost
        self.start_date = start_date
        self.renewal_date = renewal_date
        self.notes = notes

@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    # Authenticate the user using Firebase ID token
    try:
        id_token = request.headers['Authorization']
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
    except:
        return jsonify({"error": "Unauthorized"}), 401

    subscriptions = Subscription.query.filter_by(user_id=user_id).all()
    subscription_list = []
    for sub in subscriptions:
        subscription_list.append({
            "id": sub.id,
            "service": sub.service,
            "cost": sub.cost,
            "start_date": sub.start_date.strftime('%Y-%m-%d'),
            "renewal_date": sub.renewal_date.strftime('%Y-%m-%d'),
            "notes": sub.notes
        })
    return jsonify(subscription_list)

@app.route('/subscriptions', methods=['POST'])
def create_subscription():
    # Authenticate the user using Firebase ID token
    try:
        id_token = request.headers['Authorization']
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
    except:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    service = data.get('service')
    cost = data.get('cost')
    start_date = data.get('start_date')
    renewal_date = data.get('renewal_date')
    notes = data.get('notes')

    new_subscription = Subscription(user_id, service, cost, start_date, renewal_date, notes)
    db.session.add(new_subscription)
    db.session.commit()
    return jsonify({"message": "Subscription created successfully"}), 201

@app.route('/subscriptions/<int:id>', methods=['DELETE'])
def delete_subscription(id):
    # Authenticate the user using Firebase ID token
    try:
        id_token = request.headers['Authorization']
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
    except:
        return jsonify({"error": "Unauthorized"}), 401

    subscription = Subscription.query.filter_by(id=id, user_id=user_id).first()
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404

    db.session.delete(subscription)
    db.session.commit()
    return jsonify({"message": "Subscription deleted successfully"}), 200
