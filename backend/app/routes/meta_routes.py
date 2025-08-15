from flask import Blueprint, jsonify
from app.categories import all_categories

meta_bp = Blueprint("meta_bp", __name__)

@meta_bp.route("/categories", methods=["GET"])
def get_categories():
    return jsonify(all_categories())