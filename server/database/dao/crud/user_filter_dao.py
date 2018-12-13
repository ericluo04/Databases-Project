from database.dao.base_dao import BaseDAO
from database.models.user_filter import UserFilter


class UserFilterDAO(BaseDAO):
    def __init__(self, connection):
        super(UserFilterDAO, self).__init__(connection)
        self._table_name = "user_filters"

    def create_or_update(self, user_filter):
        """
        insert user_filter

        :param user_filter: UserFilter object
        :return:
        """
        # create or update user_filter
        # columns to update if user_filter exists
        update_columns = 'user_id', 'filter_id'

        return self.create_or_update_query(self._table_name,
                                           self.construct_values(user_filter),
                                           update_columns)

    def delete_filter(self, user_filter):
        self.query("DELETE FROM {} WHERE user_id = {} AND filter_id = {}".format(
            self._table_name, user_filter.user_id, user_filter.filter_id))

    @staticmethod
    def extract_data(result):
        return UserFilter(
            user_id=result['user_id'],
            filter_id=result['filter_id']
        )

    def construct_values(self, user_filter):
        return {
            'user_id': user_filter.user_id,
            'filter_id': user_filter.filter_id,
        }