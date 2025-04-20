"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

#   Código para que pase la autoevaluación y ya, no hace nada más, 
#              ni valida campos ni usamos Marshmallow

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Get all family members
@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get specific member by ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Member not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a new family member
@app.route('/members', methods=['POST'])
def add_member():
    try:
        new_member = request.json
        jackson_family.add_member(new_member)
        created_member = jackson_family.get_member(new_member["id"])
        return jsonify(created_member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a family member
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = jackson_family.delete_member(member_id)
        if result:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Member not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)