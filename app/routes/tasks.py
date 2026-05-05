from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task import Task
from app.database import db
from app.schemas.schemas import task_schema, tasks_schema
from marshmallow import ValidationError
from sqlalchemy import or_
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    try:
        data = task_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'todo'),
        priority=data.get('priority', 'medium'),
        due_date=data.get('due_date'),
        user_id=user_id
    )

    if 'tag_ids' in data:
        from app.models.tag import Tag
        tags = Tag.query.filter(Tag.id.in_(data['tag_ids']), Tag.user_id == user_id).all()
        task.tags = tags

    db.session.add(task)
    db.session.commit()
    return task_schema.jsonify(task), 201

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    
    # Query Params
    status = request.args.get('status')
    priority = request.args.get('priority')
    search = request.args.get('search')
    due_date = request.args.get('due_date')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)

    query = Task.query.filter_by(user_id=user_id)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))
    if due_date:
        try:
            date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()
            query = query.filter(Task.due_date == date_obj)
        except ValueError:
            pass

    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    
    return jsonify({
        "page": pagination.page,
        "limit": pagination.per_page,
        "total_tasks": pagination.total,
        "total_pages": pagination.pages,
        "data": tasks_schema.dump(pagination.items)
    })

@tasks_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    return task_schema.jsonify(task)

@tasks_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    
    try:
        data = task_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():
        if key == 'tag_ids':
            from app.models.tag import Tag
            tags = Tag.query.filter(Tag.id.in_(value), Tag.user_id == user_id).all()
            task.tags = tags
        else:
            setattr(task, key, value)
    
    db.session.commit()
    return task_schema.jsonify(task)

@tasks_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify({"msg": "Task deleted"}), 200
