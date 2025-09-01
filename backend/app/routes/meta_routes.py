from flask import Blueprint, jsonify
from app.categories import all_categories
from app import db

meta_bp = Blueprint("meta_bp", __name__)

@meta_bp.route("/categories", methods=["GET"])
def get_categories():
    return jsonify(all_categories())

@meta_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@meta_bp.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

