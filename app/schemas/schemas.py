from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))

class TagSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))

class NoteSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    task_id = fields.Int(dump_only=True)

class TaskSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str()
    status = fields.Str(validate=validate.OneOf(['todo', 'in_progress', 'done']))
    priority = fields.Str(validate=validate.OneOf(['low', 'medium', 'high']))
    due_date = fields.Date()
    created_at = fields.DateTime(dump_only=True)
    tags = fields.List(fields.Nested(TagSchema), dump_only=True)
    tag_ids = fields.List(fields.Int(), load_only=True)
    notes = fields.List(fields.Nested(NoteSchema), dump_only=True)

user_schema = UserSchema()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)
