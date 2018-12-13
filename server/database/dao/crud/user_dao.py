from database.dao.base_dao import BaseDAO
from database.models.user import User


class UserDAO(BaseDAO):
    def __init__(self, connection):
        super(UserDAO, self).__init__(connection)
        self._table_name = "users"

    def create_or_update(self, user):
        """
        insert user if no existing user with same id--otherwise update

        :param user: User object
        :return:
        """
        if user.id is None:
            user.id = self.get_user_id(user)

        # create or update user
        # columns to update if user exists
        update_columns = 'id', 'username', 'password'

        self.create_or_update_query(self._table_name,
                                    self.construct_values(user),
                                    update_columns)

        return user.id

    def read(self, user):
        """
        check if user exists
        :param user: User object
        :return: Boolean
        """
        fields = 'id', 'username', 'password'
        result = self.read_query(fields, self._table_name, self.construct_values(user))

        if len(result) > 1:
            raise Exception("multiple users with same username/password")

        return result[0]['id']

    def get_user_id(self, user):
        """
        computes user id
        """
        return self.get_hash(user.username, user.password)

    @staticmethod
    def extract_data(result):
        return User(
            id=result['id'],
            username=result['username'],
            password=result['password']
        )

    def construct_values(self, user):
        values = {
            'id': user.id,
            'username': user.username,
            'password': user.password
        }

        # remove None values
        values = self.remove_none_values(values)

        return values