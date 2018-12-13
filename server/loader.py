import csv

from database.connection_manager import ConnectionManager
from database.dao.crud.student_dao import StudentDAO
from database.models.student import Student

PATH = "data.csv"

if __name__ == '__main__':
    connection = ConnectionManager.get_db_connection()
    student_dao = StudentDAO(connection)

    with open(PATH, 'r') as data:
        reader = csv.reader(data)
        headers = next(reader, None)

        row_index = 1
        failed_rows = 0
        for row in reader:
            student = Student(
                first_name=row[1],
                last_name=row[2],
                year=int(row[3]),
                college=row[4],
                major=row[5],
                birth_month=int(row[6]),
                birth_day=int(row[7]),
                room=row[8],
                address=row[9],
                latitude=float(row[11]),
                longitude=float(row[12])
            )

            try:
                student_dao.create_or_update(student)
            except:
                print "row {} failed".format(row_index)

            row_index += 1