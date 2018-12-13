from database.dao.base_dao import BaseDAO
from database.dao.crud.filter_dao import FilterDAO
from database.models.student import Student


class StudentDAO(BaseDAO):
    def __init__(self, connection):
        super(StudentDAO, self).__init__(connection)
        self._table_name = "students"

    def create_or_update(self, student):
        """
        insert student if no existing student with same id--otherwise update

        :param student: Student object
        :return:
        """
        if student.id is None:
            student.id = self.get_student_id(student)

        # create or update student
        # columns to update if student exists
        update_columns = 'id', 'first_name', 'last_name', 'year', 'college', 'major', \
                         'birth_month', 'birth_day', 'address', 'room', 'latitude', 'longitude'

        return self.create_or_update_query(self._table_name,
                                           self.construct_values(student),
                                           update_columns)

    def read(self, filter):
        fields = 'id', 'first_name', 'last_name', 'year', 'college', 'major', \
                 'birth_month', 'birth_day', 'address', 'room', 'latitude', 'longitude'
        results = self.read_query(fields, self._table_name, FilterDAO(self.connection).construct_values(filter))

        return [
            self.extract_data(result)
            for result in results
        ]

    def get_student_id(self, student):
        """
        compute student id as hash of fields
        """
        return self.get_hash(student.first_name, student.last_name, student.year, student.college,
                             student.address, student.major, student.birth_month, student.birth_day)

    @staticmethod
    def extract_data(result):
        return Student(
            id=result['id'],
            first_name=result['first_name'],
            last_name=result['last_name'],
            year=result['year'],
            college=result['college'],
            major=result['major'],
            birth_month=result['birth_month'],
            birth_day=result['birth_day'],
            address=result['address'],
            room=result['room'],
            longitude=result['longitude'],
            latitude=result['latitude']
        )

    def construct_values(self, student):
        values = {
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'year': student.year,
            'college': student.college,
            'major': student.major,
            'birth_month': student.birth_month,
            'birth_day': student.birth_day,
            'address': student.address,
            'room': student.room,
            'longitude': student.longitude,
            'latitude': student.latitude
        }

        # remove None values
        values = self.remove_none_values(values)

        return values