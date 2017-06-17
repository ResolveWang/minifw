import logging
from .base_db import (
                    select,
                    execute
)


__author__ = 'ResolveWang'


def format_args(num):
    args = []
    for n in range(num):
        args.append('?')
    return ', '.join(args)


def format_where(where):
    if "'" in where:
        return where
    start = where.find('=')
    return "{}'{}'".format(where[0:start+1], where[start+1:])


class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __repr__(self):
        return '<{}, {}:{}>'.format(self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self, name=None, column_type='varchar(100)', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)


class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)


class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        table_name = attrs.get('__table__', None) or name
        logging.info('found model:{} (table: {})'.format(name, table_name))
        mappings = dict()
        fields = list()
        primary_key = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                #logging.info('found mapping:{} => {}'.format(k, v))
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise RuntimeError('Duplicate primary key for field: {}'.format(k))
                    primary_key = k
                else:
                    fields.append(k)
        if not primary_key:
            raise RuntimeError('Primary key not found')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`{}`'.format(f), fields))
        attrs['__mappings__'] = mappings
        attrs['__table__'] = table_name
        attrs['__primary_key__'] = primary_key
        attrs['__fields__'] = fields
        attrs['__select__'] = 'select `{}`, {} from `{}`'.format(primary_key, ', '.join(escaped_fields), table_name)
        attrs['__delete__'] = 'delete from `{}` where `{}`=?'.format(table_name, primary_key)
        attrs['__insert__'] = 'insert into `{}` ({}, `{}`) values ({})'.format(
            table_name, ', '.join(escaped_fields), primary_key, format_args(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `{}` set {} where `{}`=?'.format(
            table_name, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primary_key)
        return type.__new__(cls, name, bases, attrs)


# todo: remove the pool args from the code below
class Model(dict, metaclass=ModelMetaClass):
    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("Model object has no attribute {}".format(key))

    def __setattr__(self, key, value):
        self[key] = value

    def get_value(self, key):
        return getattr(self, key, None)

    def get_value_or_default(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default or not None:
                value = field.default() if callable(field.default) else field.default
                setattr(self, key, value)
        return value

    @classmethod
    async def find(cls, pool, key):
        rs = await select(pool, '{} where `{}`=?'.format(cls.__select__, cls.__primary_key__), [key], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    @classmethod
    async def find_all(cls, pool, where=None, args=None, **kw):
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(format_where(where))
        if args is None:
            args = []
        order_by = kw.get('orderBy', None)
        if order_by:
            sql.append('order by')
            sql.append(order_by)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(pool, ' '.join(sql), args)
        return [cls(**r) for r in rs]

    async def save(self, pool):
        args = list(map(self.get_value_or_default, self.__fields__))
        args.append(self.get_value_or_default(self.__primary_key__))
        rows = await execute(pool, self.__insert__, args)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: {}'.format(rows))
        return rows

    async def update(self, pool):
        args = list(map(self.get_value, self.__fields__))
        args.append(self.get_value(self.__primary_key__))
        rows = await execute(pool, self.__update__, args)
        if rows != 1:
            logging.warning('failed to update by primary key: affected rows: {}'.format(rows))
        return rows

    async def remove(self, pool):
        args = [self.get_value(self.__primary_key__)]
        rows = await execute(pool, self.__delete__, args)
        if rows != 1:
            logging.warning('failed to remove by primary key: affected rows: {}'.format(rows))
        return rows

__all__ = (Model, StringField, FloatField, BooleanField, IntegerField, TextField)