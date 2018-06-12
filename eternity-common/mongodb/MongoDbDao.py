from mongodb.MongoDbDriver import MongoDbDriver as mdd
import datetime
import uuid
import pytz
from bson.json_util import dumps
import json


class MongoDbDao(object):

    def __init__(self, database_name):
        self.db = mdd().get_database(database_name)

    def get_jsonmodel(self, cursor):
        for item in list(cursor):
            bson_item = dumps(item)
            return json.loads(bson_item)

    def get_datamodel(self, file_type, source, type, id, title, pending_record):
        self.validate_getmodel_parameters(file_type, source, type, id, title, pending_record)
        utcnow = datetime.datetime.utcnow()
        return {
            "item_id": id,
            "item_title": title,
            "date": utcnow,
            "engine": source,
            "tags": [source, type],
            "file_type": file_type,
            "uuid": str(uuid.uuid4().hex),
            "item_summary": pending_record
        }

    def get_retrive_datamodel(self, file_type, source, type, id, title, pending_record):
        self.validate_getmodel_parameters(file_type, source, type, id, title, pending_record)
        return {
            "item_id": id,
            "item_title": title,
            "engine": source,
            "tags": [source, type],
            "file_type": file_type,
            "item_summary": pending_record
        }

    def get_retrive_datamodel_by_id(self, id):
        self.validate_getmodel_by_single_parameter(id)
        return {
            "item_id": id
        }

    def get_record_bydatetime(self, source, from_datetime, to_datetime, local_timezone=True):
        self.validate_getmodel_by_basic_parameters(from_datetime, to_datetime)
        self.validate_getmodel_by_single_parameter(source)
        collection = self.db[source]
        if not isinstance(from_datetime, datetime.datetime):
            raise Exception('from_datetime is Not datetime type!')
        if not isinstance(to_datetime, datetime.datetime):
            raise Exception('to_datetime is Not datetime type!')
        if local_timezone:
            from_date = from_datetime.astimezone(pytz.utc)
            to_date = to_datetime.astimezone(pytz.utc)
            # from_date = datetime.datetime(2018, 5, 10, 12, 00, 30, 125000).astimezone(pytz.utc)
            # to_date = datetime.datetime(2018, 5, 10, 17, 00, 00, 125000).astimezone(pytz.utc)
        else:
            from_date = from_datetime
            to_date = to_datetime
            # from_date = datetime.datetime(2018, 5, 10, 12, 00, 30, 125000)
            # to_date = datetime.datetime(2018, 5, 11, 00, 34, 49, 125000)
        return collection.find({"date": {"$gte": from_date, "$lt": to_date}})

    def get_record(self, file_type, source, type, id, title, pending_record):
        self.validate_getmodel_parameters(file_type, source, type, id, title, pending_record)
        collection = self.db[source]
        doc = self.get_retrive_datamodel(self.file_type, source, type, id, title, pending_record)
        return collection.find(doc)

    def get_record_by_id(self, source, id):
        self.validate_getmodel_by_basic_parameters(source, id)
        collection = self.db[source]
        doc = self.get_retrive_datamodel_by_id(id)
        return collection.find(doc)

    def delete_record_by_id(self, source, id):
        self.validate_getmodel_by_basic_parameters(source, id)
        collection = self.db[source]
        doc = self.get_retrive_datamodel_by_id(id)
        return collection.remove(doc)

    def delete_record_by_collection(self, source):
        self.validate_getmodel_by_single_parameter(source)
        collection = self.db[source]
        return collection.drop()

    def insert_record(self, source, type, id, title, pending_record):
        self.validate_insertmodel_parameters(source, type, id, title, pending_record)
        collection = self.db[source]
        doc = self.get_datamodel(self.file_type, source, type, id, title, pending_record)
        return collection.insert_one(doc).inserted_id
        # return collection.insert(BSON.encode(doc)).inserted_id
        # record_id = collection.insert_one(pending_record).inserted_id

    def validate_insertmodel_parameters(self, source, type, id, title, pending_record):
        if not self.file_type:
            raise Exception('Missing file type!')

    def validate_getmodel_parameters(self, file_type, source, type, id, title, pending_record):
        if not (file_type and source and type and id and title and pending_record):
            raise Exception('Missing some common parameters!')

    def validate_getmodel_by_basic_parameters(self, source, id):
        if not source or not id:
            raise Exception('Missing basic parameters!')

    def validate_getmodel_by_single_parameter(self, id):
        if not id:
            raise Exception('Missing id parameters!')
