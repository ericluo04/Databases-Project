class FilterSerializer:
    def serialize(self, filter):
        return {
            'firstName': filter.first_name,
            'lastName': filter.last_name,
            'classYear': filter.year,
            'college': filter.college,
            'major': filter.major,
            'birthday': filter.birth_day,
            'room': filter.room
        }