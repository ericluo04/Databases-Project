import logging
import hashlib


class BaseDAO(object):
    def __init__(self, connection):
        self.connection = connection

        # set up logger
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.INFO)

    def query(self, sql, where=None, order=None, limit=None):
        log_messages = {
            'success': 'Query successful',
            'failure': 'Query failed'
        }
        print sql
        q = self.query_decorator(self.connection.query, log_messages)
        return q(sql, where, order, limit)

    def create_or_update_query(self, table, values, update_columns):
        # TODO: build on top of querybuilder
        log_messages = {
            'success': 'Create or Update on Duplicate successful into {} table'.format(table),
            'failure': 'Create or Update on Duplicate into {} table failed'.format(table)
        }

        set_update_columns = ["{0} = VALUES({0})".format(update_column)
                              for update_column
                              in update_columns]

        print set_update_columns
        sql = """
        INSERT INTO {table} ({columns})
        VALUES ({values})
        ON DUPLICATE KEY UPDATE 
            {updates}
        """.format(table=table,
                   columns=', '.join(values.keys()),
                   values=', '.join(['"{}"'.format(value) if value is not None else 'null'
                              for value in values.values()]),
                   updates=', '.join(set_update_columns))
        print sql
        q = self.query_decorator(self.connection.query, log_messages)
        return q(sql)

    def create_query(self, table, values):
        log_messages = {
            'success': 'Insertion into {} table successful'.format(table),
            'failure': 'Insertion failed into {} table'.format(table)
        }

        q = self.query_decorator(self.connection.insert, log_messages)
        return q(table, values)

    def read_query(self, fields, table, where=None, order=None, limit=None):
        log_messages = {
            'success': 'Selection on {} table successful'.format(table),
            'failure': 'Selection failed on {} table'.format(table)
        }

        q = self.query_decorator(self.connection.select, log_messages)
        return q(fields, table, where, order, limit)

    def update_query(self, table, values, where=None):
        log_messages = {
            'success': 'Update to {} table successful'.format(table),
            'failure': 'Update failed for {} table'.format(table)
        }

        q = self.query_decorator(self.connection.update, log_messages)
        return q(table, values, where)

    def delete_query(self, table, where=None):
        log_messages = {
            'success': 'Deletion on {} table successful'.format(table),
            'failure': 'Deletion failed on {} table'.format(table)
        }

        q = self.query_decorator(self.connection.delete, log_messages)
        return q(table, where)

    def query_decorator(self, query, log_messages):
        def wrapper(*args, **kwargs):
            try:
                # execute query
                ret = query(*args, **kwargs)
                self._logger.info(log_messages['success'])

                return ret
            except Exception as e:
                # insertion failed
                self._logger.exception(log_messages['failure'] +
                                       ", type: {}".format(type(e).__name__))

                # rethrow exception
                raise
        return wrapper

    def construct_values(self, data_object):
       pass

    @staticmethod
    def get_hash(*args):
        return BaseDAO.hash_f(','.join(map(str, args)))

    @staticmethod
    def hash_f(string):
        hash_string = hashlib.sha256(string.lower()).hexdigest()
        truncated_hash = int(hash_string, 16) % 10 ** 9
        return int(truncated_hash)

    @staticmethod
    def remove_none_values(values):
        del_keys = []

        for key, val in values.iteritems():
            if val is None:
                del_keys.append(key)

        for key in del_keys:
            del values[key]

        return values
