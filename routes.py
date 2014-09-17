from datetime import datetime
from flask import render_template, g, request, flash, redirect, url_for, jsonify

from app import app, db, auth
from models import User

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/api/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User(username=username, password=password)
    if user is None:
        abort(400)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username}), 201

@app.route('/api/token', methods=['POST'])
@auth.login_required
def token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token}), 201

@app.route('/api/greeting')
@auth.login_required
def greeting():
    return jsonify({'data': 'Hello {0}'.format(g.user.username)})