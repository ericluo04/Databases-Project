import json

from flask import Flask, request
from flask_cors import CORS, cross_origin

from database.connection_manager import ConnectionManager
from database.dao.application_dao import ApplicationDAO
from database.dao.crud.filter_dao import FilterDAO
from database.dao.crud.student_dao import StudentDAO
from database.dao.crud.user_dao import UserDAO
from database.dao.crud.user_filter_dao import UserFilterDAO
from database.models.filter import Filter
from database.models.user import User
from database.models.user_filter import UserFilter
from database.serializers.filter_serializer import FilterSerializer
from database.serializers.student_serializer import StudentSerializer

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def ping():
    return "ping"

@app.route('/register', methods=['POST'])
def register():
    connection = ConnectionManager().get_db_connection()
    user_id = UserDAO(connection).create_or_update(User(
        username=request.form['username'],
        password=request.form['password']
    ))
    return json.dumps({'user_id': user_id})


@app.route('/login', methods=['GET'])
def login():
    connection = ConnectionManager().get_db_connection()
    user_id = UserDAO(connection).read(User(
        username=request.args.get('username', None),
        password=request.args.get('password', None)
    ))
    return json.dumps({'user_id': user_id})


@app.route('/people', methods=['GET'])
def people():
    connection = ConnectionManager().get_db_connection()
    students = StudentDAO(connection).read(Filter(
        first_name=request.args.get('firstName', None),
        last_name=request.args.get('lastName', None),
        year=request.args.get('classYear', None),
        college=request.args.get('college', None),
        major=request.args.get('major', None),
        birth_month=request.args.get('birthMonth', None),
        birth_day=request.args.get('birthDay', None)
    ))

    return json.dumps([StudentSerializer().serialize(student) for student in students])


@app.route('/filter', methods=['GET', 'POST', 'DELETE'])
def filter():
    connection = ConnectionManager().get_db_connection()
    if request.method == 'GET':
        filters = FilterDAO(connection).read_all_filters_for_user(int(request.args.get('userId')))
        return json.dumps([FilterSerializer().serialize(filt) for filt in filters])
    elif request.method == 'POST':
        filter_id = ApplicationDAO(connection).create_filter(filter=Filter(
            first_name=request.form['firstName'] if 'firstName' in request.form else None,
            last_name=request.form['lastName'] if 'lastName' in request.form else None,
            year=int(request.form['classYear']) if 'classYear' in request.form else None,
            college=request.form['college'] if 'college' in request.form else None,
            major=request.form['major'] if 'major' in request.form else None,
            birth_month=int(request.form['birthMonth']) if 'birthMonth' in request.form else None,
            birth_day=int(request.form['birthDay']) if 'birthDay' in request.form else None
        ), user_id=request.form['userId'])

        return json.dumps({'filterId': filter_id})
    elif request.method == 'DELETE':
        UserFilterDAO(connection).delete_filter(
            UserFilter(user_id=request.form['userId'], filter_id=request.form['filterId']))
        return json.dumps({'status': "success"})
    else:
        print "wrong http method type"


if __name__ == '__main__':
    app.run()
