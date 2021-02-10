import datetime
from multiprocessing.dummy import Value

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from metric.db import session
from metric.db.errors import AddQueryInvalid
from metric.db.errors import DataValueInvalid
from metric.db.errors import NoneTypeValue


class Query:
    """
    ____class querying____
    """
    __result = None
    __query = None
    __action = []
    q = None
    s = session()

    _a = None

    def __del__(self):
        self.s.close()

    # ** USING JOIN **
    def along(self, *args):
        """
        ____extend select with calling the relationship____
        """
        self._a = args
        return self
    # ** END OF JOIN **

    # ** SHOW RECORD **
    def select(self, *args):
        """
        ____To starting some result you must first follow the select function and then anything else____

        @param: args: List all the column record to shown if not then show all
        @return: self
        """
        if args:
            self.q = self.s.query(*[getattr(self.__class__, i) for i in args])
        else:
            self.q = self.s.query(self.__class__)

        return self

    def count(self):
        """
        ____To show the total of record and it's returning the value directly____

        @return:
        """
        return self.s.query(self.__class__).count()

    def filter(self, col, value, operator='='):
        """
        ____Filter is only work when selecting database, it's equivalent where in SQL____

        @param col: The column you want to filter
        @param value: The value filtered
        @param operator: Operator type for filter
        @return: self
        """
        col = getattr(self.__class__, col)

        if operator == 'like':
            self.q = self.q.filter(col.like(value))
        elif operator == '!=':
            self.q = self.q.filter(col != value)
        elif operator == 'in':
            if isinstance(value, list) or isinstance(value, tuple):
                self.q = self.q.filter(col.in_(value))
            else:
                raise DataValueInvalid(value)
        else:
            self.q = self.q.filter(col == value)

        return self

    def grab(self, edge, length):
        """
        ____Grab means to grab record by edge(offset) and length(limit)____

        @param: edge: The offset of record
        @param: length: Limitation of record
        @return: self
        """
        self.q = self.q.offset(edge * length).limit(length).from_self()
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

    def all(self, result={}):
        """
        ____select everything that appear in result query____

        @param result: Type of result to return
        @return: Based on type result either dict or object, default dict
        """
        self.commit()

        if isinstance(result, dict):
            return [self.to_dict(i) for i in self.q.all()]

        elif isinstance(result, object):
            return [self.to_object(i) for i in self.q.all()]

    def first(self, result={}):
        """
        ____select only the first one appear in result query____
        """
        self.commit()

        if isinstance(result, dict):
            return self.to_dict(self.q.first())

        elif isinstance(result, object):
            return self.to_object(self.q.first())

        else:
            return self.q.first()

    # ** END OF SHOW RECORD **

    # ** ADD RECORD **
    def add(self, result={}, *args, **kwargs):
        """
        ____This function is supposed to insert data either single record or multiple____

        @param result: Is the output you wanted to return
        @param args: If you're looking to add multiple record use lists
        @params kwargs: If you're looking to single add record, just use dict
        """

        # ____if parameter is dictionary the it single add instance____
        if bool(kwargs):
            try:
                query = self.__class__(**kwargs)
            except AddQueryInvalid as err:
                raise AddQueryInvalid(kwargs)
            else:
                self.s.add(query)
                self.commit(query)

                if isinstance(result, dict):
                    return self.to_dict(query)

                elif isinstance(result, object):
                    return self.to_object(query)

        # ____if args is not empty and is list then it multiple add instance____
        elif args:
            print(args)
            try:
                query = list()
                for item in args:
                    print(item)
                    query.append(self.__class__(**item))
            except AddQueryInvalid as err:
                raise AddQueryInvalid(args)
            else:
                print(query)
                self.s.add_all(query)
                self.commit()

    def bulkInsert(self, *args):
        """
        ____Bulk insert is bulk insert but without return result____

        @param args: List with dictionary inside
        """
        query = list()

        for item in args:
            query.append(self.__class__(**item))

        self.s.bulk_save_objects(query)
        self.commit()
    # ** END OF ADD RECORD **

    # ** DELETE RECORD **
    def destruct(self, val):
        """
        ____Destruct is purposely to delete a record by it's ID____

        @param val: id value of the record
        """
        try:
            self.q = self.s.query(self.__class__)
            self.q.filter(self.__class__.id == val).delete()
        except SQLAlchemyError as err:
            raise err
        else:
            self.commit()
            return True

    def edit(self, **kwargs):
        self.first()

        for k, v in kwargs.items():
            setattr(self.__result, k, v)
        self.commit(self.__result)
        return self.__result

    def commit(self, query=None):
        try:
            self.s.commit()

        except SQLAlchemyError as err:
            self.s.rollback()
            raise err

        else:
            if query is not None:
                self.s.refresh(query)
                return query

    def to_dict(self, data):
        """
        ____Converting the result to dictionary data and return it with hidden and deleted instance____

        @param data: The query data you given
        @return: dictionary data
        """
        try:
            data = data.__dict__

            # ____removing instance_state from data dictionary____
            if '_sa_instance_state' in data:
                del data['_sa_instance_state']

            # ____removing key with hidden defined
            for i in self.__class__.hidden():
                del data[i]

            return data

        except AttributeError as err:
            raise NoneTypeValue(data)

    def to_object(self, data):
        """
        ____Converting the result to object, served same as above____

        @param data: The query data you given
        @return: object data
        """
        data_to_object = lambda: None

        for k, v in self.to_dict(data).items():
            setattr(data_to_object, k, v)

        return data_to_object

    def where(self, **flt):
        """
        ____filter the selection query with____
        """
        self.__query = self.__query.filter_by(**flt)
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
