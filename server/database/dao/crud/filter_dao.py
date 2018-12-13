from database.dao.base_dao import BaseDAO
from database.models.filter import Filter


class FilterDAO(BaseDAO):
    def __init__(self, connection):
        super(FilterDAO, self).__init__(connection)
        self._table_name = "filters"

    def create_or_update(self, filter):
        """
        insert filter if no existing filter with same id--otherwise update

        :param filter: Filter object
        :return:
        """
        if filter.id is None:
            filter.id = self.get_filter_id(filter)

        # create or update filter
        # columns to update if filter exists
        update_columns = 'id', 'first_name', 'last_name', 'year', 'college', 'major', 'birth_month', 'birth_day'

        self.create_or_update_query(self._table_name,
                                    self.construct_values(filter),
                                    update_columns)

        return filter.id

    def read_all_filters_for_user(self, user_id):
        """
        return dictionary key = name value = course id
        :return:
        """
        sql = """
        SELECT filters.* 
        FROM filters
        JOIN user_filters
            ON filters.id = user_filters.filter_id
        WHERE user_filters.user_id = {user_id}
        """.format(user_id=user_id)

        # query for all courses
        results = self.query(sql)

        return [
            self.extract_data(result)
            for result in results
        ]

    def delete_filter(self, filter_id):
        return self.delete_query(self._table_name, where={'id': filter_id})

    def get_filter_id(self, filter):
        """
        returns filter id with given name
        """
        filter_id = self.get_hash(filter.first_name, filter.last_name, filter.year, filter.college,
                                  filter.major, filter.birth_month, filter.birth_day)

        return filter_id

    @staticmethod
    def extract_data(result):
        return Filter(
            id=result['id'],
            first_name=result['first_name'],
            last_name=result['last_name'],
            year=result['year'],
            college=result['college'],
            major=result['major'],
            birth_month=result['birth_month'],
            birth_day=result['birth_day']
        )

    def construct_values(self, filter):
        values = {
            'id': filter.id,
            'first_name': filter.first_name,
            'last_name': filter.last_name,
            'year': filter.year,
            'college': filter.college,
            'major': filter.major,
            'birth_month': filter.birth_month,
            'birth_day': filter.birth_day
        }

        # remove None values
        values = self.remove_none_values(values)

        return values