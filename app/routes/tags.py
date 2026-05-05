from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.tag import Tag
from app.database import db
from app.schemas.schemas import tag_schema, tags_schema
from marshmallow import ValidationError

tags_bp = Blueprint('tags', __name__)

@tags_bp.route('', methods=['POST'])
@jwt_required()
def create_tag():
    user_id = get_jwt_identity()
    try:
        data = tag_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if Tag.query.filter_by(name=data['name'], user_id=user_id).first():
        return jsonify({"msg": "Tag already exists"}), 400

    tag = Tag(name=data['name'], user_id=user_id)
    db.session.add(tag)
    db.session.commit()
    return tag_schema.jsonify(tag), 201

@tags_bp.route('', methods=['GET'])
@jwt_required()
def get_tags():
    user_id = get_jwt_identity()
    tags = Tag.query.filter_by(user_id=user_id).all()
    return tags_schema.jsonify(tags)
