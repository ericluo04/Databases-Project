from database.dao.base_dao import BaseDAO
from database.dao.crud.filter_dao import FilterDAO
from database.dao.crud.user_filter_dao import UserFilterDAO
from database.models.user_filter import UserFilter


class ApplicationDAO(BaseDAO):
    def __init__(self, connection):
        super(ApplicationDAO, self).__init__(connection)

    def create_filter(self, filter, user_id):
        self.connection.begin()

        try:
            filter_dao = FilterDAO(self.connection)
            user_filter_dao = UserFilterDAO(self.connection)

            if filter.id is None:
                filter.id = filter_dao.get_filter_id(filter)

            filter_id = filter_dao.create_or_update(filter)
            user_filter_dao.create_or_update(UserFilter(user_id=user_id, filter_id=filter.id))

            self.connection.commit()

            return filter_id
        except Exception:
            # exception has already been logged
            # rollback transaction and rethrow exception
            self.connection.rollback()
            raise
