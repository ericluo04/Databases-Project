class FilterSerializer:
    def serialize(self, filter):
        return {
            'filterId': filter.id,
            'firstName': filter.first_name,
            'lastName': filter.last_name,
            'classYear': filter.year,
            'college': filter.college,
            'major': filter.major,
            'birthDay': filter.birth_day,
            'birthMonth': filter.birth_month
        }