from flask import Flask, jsonify, request
import database

app = Flask(__name__)
database.init_db()

@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'API is working!'})

@app.route('/upload', methods=['POST'])
def upload_score():
    data = request.get_json()
    username = data.get('username')
    score = data.get('score')
    time = data.get('time')
    if not username or not isinstance(score, int) or IsInvalid(username):
        return jsonify({'error': 'Invalid input'}), 400
    elif len(username) < 3 or len(username) > 20:
        return jsonify({'error': 'Username must be between 5 and 20 characters'}), 401
    else:
        database.log_score(username, score, time)
        return jsonify({'message': 'Score uploaded'})

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard = database.get_leaderboard()
    return jsonify(leaderboard)



def IsInvalid(username):
    for char in username:
        if char in set(" !@#$%^&*()[]{}|;:'\",.<>?/\\"):
            return True
    return False

if __name__ == '__main__':

    database.init_db()
    app.run(host='0.0.0.0', port=5067, debug=True)