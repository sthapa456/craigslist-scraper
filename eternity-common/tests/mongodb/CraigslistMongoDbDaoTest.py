__author__ = 'kowaiyan'

import unittest
from mongodb.CraigslistMongoDbDao import CraigslistMongoDbDao
import json, ast
from bson.json_util import dumps
from bson import json_util
import datetime


class CraigslistMongoDbDaoTest(unittest.TestCase):

    def setUp(self):
        self.item_dao = CraigslistMongoDbDao('test_vehicle')
        self.item_dao.delete_item_collection()

    def _steps(self):
        for name in sorted(dir(self)):
            if name.startswith('step'):
                yield name, getattr(self, name)

    def step_01_insert(self):
        record_id = self.item_dao.insert_item_record("pj_001", "data engineer", "<html></html>")
        self.assertIsNotNone(record_id, 'failed step_01_insert')

    def step_02_delete(self):
        record_id = self.item_dao.insert_item_record("pj_002", "data engineer", "<html></html>")
        result = self.item_dao.delete_item_record_by_itemid("pj_002")
        self.assertEqual(1, result['n'], 'failed step_02_insert')

    def step_03_retrieve(self):
        cursor = self.item_dao.get_item_record("pj_001", "data engineer", "<html></html>")
        self.assertEqual(1, cursor.count(), 'failed step_03_retrieve')

    def step_04_retrieve_byid(self):
        self.assertTrue(self.item_dao.check_if_itemid_exists("pj_001"),
                        'failed step_04_retrieve_byid - pj_001 should exists')
        self.assertFalse(self.item_dao.check_if_itemid_exists("pj_002"),
                         'failed step_04_retrieve_byid - pj_002 should not exists')

    def step_05_retrieve_bydatetime(self):
        # cursor = self.item_dao.get_item_record_bydatetime(datetime.datetime(2018, 5, 10, 11, 3, 00, 125000),
        #                                                       datetime.datetime(2018, 5, 10, 12, 00, 30, 125000), False)
        curent_datetime = datetime.datetime.now()
        until_datetime = curent_datetime + datetime.timedelta(minutes=1)
        record_id = self.item_dao.insert_item_record("pj_003", "data engineer", "<html></html>")
        cursor = self.item_dao.get_item_record_bydatetime(curent_datetime,
                                                              until_datetime, True)
        jsons = self.item_dao.get_jsonmodel(cursor)
        id_list = filter(self.item_dao.filter_by_itemid, jsons.items())
        self.assertEqual(1, cursor.count(), 'failed step_05_retrieve_bydatetime - record count not matched!')
        self.assertTrue(dict(id_list)['item_id'] == "pj_003",
                        'failed step_05_retrieve_bydatetime - record id not matched')

    def step_06_parse(self):
        object = self.item_dao.get_item_datamodel("pj_001", "data engineer", "<html></html>")
        test_json = json.dumps(str(object))
        json_data = ast.literal_eval(test_json)
        js = json.loads(test_json)
        self.assertIsInstance(js, str, 'failed step_06_parse, cannot parse Json from db object')

    def tearDown(self):
        self.item_dao.delete_item_collection()

    def test_steps(self):
        for name, step in self._steps():
            try:
                print('Starting {0}...'.format(name))
                step()
                print('Finished running {0}...'.format(name))
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))


if __name__ == '__main__':
    unittest.main()
