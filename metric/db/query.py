import datetime

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from metric.db import session


class Query:
    """
    ____class querying____
    """
    __session = session()
    __result = None
    __query = None
    __action = []
    __along = []

    def __del__(self):
        self.__session.close()

    def select(self, options=None, *args):
        """
        ____query intiating with select from____
        """
        if options is not None:
            if options == 'count':
                self.__query = self.__session.query(func.count(self.__class__.id))
        else:
            if not args:
                self.__query = self.__session.query(self.__class__)
            else:
                s = list()
                for i in args:
                    s.append(getattr(self._sa_instance_state.class_, i))
                self.__query = self.__session.query(*s)

        return self

    def add(self, **kwargs):
        """
        adding new record by using dict as parameter
        """
        query = self.__class__(**kwargs)
        self.__session.add(query)
        self.commit(query)
        return query

    def adds(self, *args):
        """
        adding record as bulk list
        """
        query = list()
        for item in args:
            query.append(self.__class__(**item))
        self.__session.add_all(query)
        self.commit()

    def bulk_insert(self, *args):
        query = list()
        for item in args:
            query.append(self.__class__(**item))
        self.__session.bulk_save_objects(query)
        self.commit()

    def update(self, **kwargs):
        self.first()

        for k, v in kwargs.items():
            setattr(self.__result, k, v)
        self.commit(self.__result)
        return self.__result

    def commit(self, query=None):
        try:
            self.__session.commit()

        except SQLAlchemyError as err:
            self.__session.rollback()
            raise err

        else:
            if query is not None:
                self.__session.refresh(query)
                return query

    def along(self, *args):
        """
        ____extend select with calling the relationship____
        """
        self.__along = args
        return self

    def filter(self, col, value):
        get_table = getattr(self._sa_instance_state.class_, col)
        self.__query = self.__query.filter(get_table == value)
        return self

    def where(self, **flt):
        """
        ____filter the selection query with____
        """
        self.__query = self.__query.filter_by(**flt)
        return self

    def grab(self, edge, length):
        """
        ____paginate the query by get the offset and limit based on the page and length____
        """
        self.__query = self.__query.offset(edge * length).limit(length).from_self()
        return self

    def sort(self, col, t):
        """
        ____sort the selecting query, equivalent to order_by____
        """
        if t == 'asc':
            self.__query = self.__query.order_by(getattr(self.__class__, col))
        else:
            self.__query = self.__query.order_by(getattr(self.__class__, col))
        return self

    def all(self):
        """
        ____select everything that appear in result query____
        """
        self.__result = self.__query.all()
        return self

    def first(self):
        """
        ____select only the first one appear in result query____
        """
        self.__result = self.__query.first()
        return self

    def result(self, show_as=None):
        """
        ____just showing the result that already been executed____
        """
        if show_as == 'json':
            self.__converter(self.__result)
        self.commit()
        return self.__result

    def __converter(self, data):
        if data is not None and bool(data):
            if isinstance(data, list):
                self.__dumber_rec(data)
                if self.__along:
                    pass

    def __dumber_rec(self, data):
        temp_list = list()

        for item in data:
            temp_item = item.__dict__

            # ____first thing we need to remove instance from
            # sql-alchemy and just grab the result of ours____
            if '_sa_instance_state' in temp_item:
                del temp_item['_sa_instance_state']
            temp_list.append(self.__dumber_dump(temp_item))
        return temp_list

    def __dumber_dump(self, data):
        temp_dict = dict()

        for k, v in data:
            if isinstance(v, datetime.datetime):
                v = v.strftime('%Y/%m/%d, %H:%M:%S')
            temp_dict[k] = v
        return temp_dict

    def __data_changing(self, data_dict):
        """
        ____work in progress data changing____
        """
        chg = dict()

        for k, v in data_dict.items():
            if isinstance(v, datetime.datetime):
                v = v.strftime('%Y/%m/%d, %H:%M:%S')
            chg[k] = v
        return chg

    def as_json(self):
        if self.__result is not None:
            # ____if the results is all or list or tuple, which mean is not first select____
            if isinstance(self.__result, list) or isinstance(self.__result, tuple):
                pass

        else:
            raise ValueError('You can\'t run this function without finishing the query')

    def __query_converter_list(self):
        """
        ____showing all result based on the query that already been created____
        """
        result = list()
        if self.__query is not None:
            for i in self.__query.all():
                r = None
                if len(self.__along) > 0:
                    r = {}
                    for a in self.__along:
                        r[a] = getattr(i, a)

                i = i.__dict__

                if '_sa_instance_state' in i:
                    del i['_sa_instance_state']

                for k, v in i.items():
                    if isinstance(v, datetime.datetime):
                        v = v.strftime('%Y/%m/%d, %H:%M:%S')
                        i[k] = v

                if bool(r):
                    for x, y in r.items():
                        i[x] = [z.__dict__ for z in y]

                result.append(i)
            return result
