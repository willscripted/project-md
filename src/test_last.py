import random
import unittest
import toJson


class TestLastFunction(unittest.TestCase):

    def setUp(self):
      print "\n"

    # last([]) should => Missing project
    def test_last_of_empty(self):
        list = []
        last = toJson.last(list)
        self.assertEqual(last, toJson.missingHeaders[1])

    # last([{t: project, c: []}])             => {t: project, c: []}
    def test_last_one_project(self):
        project = {"type": "project", "content": []}
        list = [project]
        last = toJson.last(list)
        self.assertEqual(last, project)

    # last([{t: project, c: [{ t: obj, c: []}]}]) => {t: obj, c: []}
    def test_last_one_obj(self):
        obj =  {"type": "objective", "content": []}
        project = {"type": "project", "content": [obj]}
        list = [project]
        last = toJson.last(list)
        self.assertEqual(last, obj)

    # last([{t: project, c:  t: obj, c: []}, {t: project, c: []}]) => {t: project, c: []}
    def test_last_two_projects(self):
        obj =  {"type": "objective", "content": []}
        project = {"type": "project", "content": [obj]}
        project2 = {"type": "project", "content": []}
        list = [project, project2]
        last = toJson.last(list)
        self.assertEqual(last, project2)

if __name__ == '__main__':
    unittest.main()
