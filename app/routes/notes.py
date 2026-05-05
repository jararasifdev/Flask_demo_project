from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.note import Note
from app.models.task import Task
from app.database import db
from app.schemas.schemas import note_schema, notes_schema
from marshmallow import ValidationError

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/<int:task_id>/notes', methods=['POST'])
@jwt_required()
def add_note_to_task(task_id):
    task = Task.query.get_or_404(task_id)
    try:
        data = note_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    note = Note(content=data['content'], task_id=task.id)
    db.session.add(note)
    db.session.commit()
    return note_schema.jsonify(note), 201

@notes_bp.route('/<int:task_id>/notes', methods=['GET'])
@jwt_required()
def get_task_notes(task_id):
    task = Task.query.get_or_404(task_id)
    return notes_schema.jsonify(task.notes)

@notes_bp.route('/<int:task_id>/tags', methods=['POST'])
@jwt_required()
def add_tag_to_task(task_id):
    from app.models.tag import Tag
    task = Task.query.get_or_404(task_id)
    tag_name = request.json.get('name')
    if not tag_name:
        return jsonify({"msg": "Tag name is required"}), 400

    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.session.add(tag)

    if tag not in task.tags:
        task.tags.append(tag)
        db.session.commit()

    return jsonify({"msg": f"Tag '{tag_name}' added to task"}), 200
