from flask import Flask, jsonify, request
import math, re, uuid, os

app = Flask(__name__)

# In-memory storage for receipts ("receipt_id": points)
receipts = {}

def calculate_points(receipt_data):
    points = 0

    points += len(re.findall(r'[a-zA-Z0-9]', receipt_data['retailer']))
    total = float(receipt_data['total'])

    if total.is_integer():
        points += 50

    if total % 0.25 == 0:
        points += 25

    item_count = len(receipt_data['items'])
    points += (item_count // 2) * 5

    for item in receipt_data['items']:
        description_length = len(item['shortDescription'].strip())
        if description_length % 3 == 0:
            price = float(item['price'])
            additional_points = math.ceil(price * 0.2 + 0.5)
            points += additional_points

    day = int(receipt_data['purchaseDate'].split('-')[2])
    if day % 2 != 0:
        points += 6

    hour = int(receipt_data['purchaseTime'].split(':')[0])
    if 14 <= hour < 16:
        points += 10

    return points

@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    receipt_data = request.get_json()

    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt_data)

    receipts[receipt_id] = points

    response = {'id': receipt_id}
    return jsonify(response)


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    points = receipts.get(receipt_id)

    if points is None:
        response = {'error': 'No receipt found; Invalid receipt ID'}
    else:
        response = {'points': points}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
