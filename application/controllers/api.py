from flask import Blueprint
from flask_restplus import Resource, fields
from application.extensions import api
from application.models import Todo as TodoDB

api_v1 = Blueprint('api', __name__, url_prefix='/api')


ns = api.namespace('todos', description='TODO operations')

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

todo = api.model('Todo', {
    'task': fields.String(required=True, description='The task details')
})

listed_todo = api.model('ListedTodo', {
    'id': fields.String(required=True, description='The todo ID'),
    'todo': fields.Nested(todo, description='The Todo')
})


def abort_if_todo_doesnt_exist(todo_id):
    todo = TodoDB.query.filter_by(id=todo_id).first()
    if todo is None:
        api.abort(404, "Todo {} doesn't exist".format(todo_id))

parser = api.parser()
parser.add_argument('task', type=str, required=True, help='The task details', location='form')


@ns.route('/<string:todo_id>')
@api.doc(responses={404: 'Todo not found'}, params={'todo_id': 'The Todo ID'})
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.doc(description='todo_id should be in {0}'.format(', '.join(TODOS.keys())))
    @api.marshal_with(todo)
    def get(self, todo_id):
        '''Fetch a given resource'''
        abort_if_todo_doesnt_exist(todo_id)
        cur_todo = TodoDB.query.filter_by(id=todo_id).first()
        ret = {'task': cur_todo.title}
        return ret

    @api.doc(responses={204: 'Todo deleted'})
    def delete(self, todo_id):
        '''Delete a given resource'''
        abort_if_todo_doesnt_exist(todo_id)
        print todo_id
        todo = TodoDB.query.filter_by(id=todo_id).first()
        if todo:
            todo.delete_todo()
        return '', 204

    @api.doc(parser=parser)
    @api.marshal_with(todo)
    def put(self, todo_id):
        '''Update a given resource'''
        args = parser.parse_args()
        todo = TodoDB.query.filter_by(id=todo_id).first()
        if todo:
            todo.title = args['task']
            todo.store_to_db()
        task = {'task': args['task']}
        return task


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @api.marshal_list_with(listed_todo)
    def get(self):
        '''List all todos'''
        todo = TodoDB.query.order_by('-id')
        for item in todo:
            print item.title
        return [{'id': item.id, 'todo': {'task': item.title}} for item in todo]

    @api.doc(parser=parser)
    @api.marshal_with(todo, code=201)
    def post(self):
        '''Create a todo'''
        args = parser.parse_args()
        todo_id = 'todo%d' % (len(TODOS) + 1)
        todo = TodoDB()
        todo.id = todo_id
        todo.title = args['task']
        todo.store_to_db()
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
