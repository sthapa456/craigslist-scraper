from mongodb.MongoDbDao import MongoDbDao as mddao

__all__ = ['CraigslistMongoDbDao']


class CraigslistMongoDbDao(mddao):

    def __init__(self, item_database='vehicle'):
        self.item_source = 'craigslist'
        self.file_type = 'html'
        self.item_type = 'motorcycle'
        mddao.__init__(self, item_database)

    def get_item_datamodel(self, item_id, item_title, item_summary):
        return self.get_datamodel(self.file_type, self.item_source, self.item_type, item_id, item_title, item_summary)

    def get_item_record_bydatetime(self, from_datetime, to_datetime, local_timezone):
        return self.get_record_bydatetime(self.item_source, from_datetime, to_datetime, local_timezone)

    def get_item_record(self, item_id, item_title, item_summary):
        return self.get_record(self.file_type, self.item_source, self.item_type, item_id, item_title, item_summary)

    def get_item_record_by_itemid(self, item_id):
        return self.get_record_by_id(self.item_source, item_id)

    def insert_item_record(self, item_id, item_title, item_summary):
        return self.insert_record(self.item_source, self.item_type, item_id, item_title, item_summary)

    def delete_item_record_by_itemid(self, item_id):
        return self.delete_record_by_id(self.item_source, item_id)

    def delete_item_collection(self):
        return self.delete_record_by_collection(self.item_source)

    def check_if_itemid_exists(self, item_id):
        return True if self.get_item_record_by_itemid(item_id).count() > 0 else False

    def get_itemid(self, jsons):
        id_list = filter(self.filter_by_itemid, jsons.items())
        return dict(id_list)['item_id']

    def filter_by_itemid(self, item_tuple):
        id_list = list()
        for key in item_tuple:
            if key == 'item_id':
                id_list.append(item_tuple[1])
            else:
                pass
        return id_list
