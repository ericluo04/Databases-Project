class StudentSerializer:
    def serialize(self, student):
        return {
            'firstName': student.first_name,
            'lastName': student.last_name,
            'classYear': student.year,
            'college': student.college,
            'major': student.major,
            'birthDay': student.birth_day,
            'birthMonth': student.birth_month,
            'room': student.room,
            'address': student.address,
            'longitude': student.longitude,
            'latitude': student.latitude
        }