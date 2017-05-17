import unittest
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        '''Defines test variables and initialize app.'''
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Visit London UK'}
        with self.app.app_context():
            db.create_all()

    def test_create_buketlists(self):
        """Tests if API can create a bucketlist (POST request)"""
        method = self.client().post('/bucketlists/1/items/1', data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        self.assertIn('Visit London UK', str(method.data))

    def test_create_buketlists_with_no_name(self):
        """
        Tests if API can create a bucketlist whose name has no value(POST request)
        Checks for (400-bad request) status code response
        """
        bucketlist = {"name": ""}
        method = self.client().post('/bucketlists/1/items/1', data=bucketlist)
        self.assertEqual(method.status_code, 400)
        self.assertIn('Visit London UK', str(method.data))    

    def test_update_bucketlists(self):
        '''Tests if API can udate an existing bucketlist (PUT request)'''
        method = self.client().post('/bucketlists/1/items/1', data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        new_method = self.client().put('/bucketlists/', data={'name': 'Visit London UK and Paris'})
        self.assertEqual(new_method.status_code, 200)
        result = self.client().get('/bucketlists/1')
        self.assertIn('Visit London UK and Paris', str(result.data))

    def test_update_bucketlist_item(self):
        '''
        Tests if API can udate an existing item in the bucketlist (PUT request)
        Creates a new bucket list then updates an item in the bucketlist
        Tests for (200-Ok) status code response
        '''
        method = self.client().post('/bucketlists/1/items/1', data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        new_method = self.client().put('/bucketlists/1/items/1', data={'name': 'Visit London UK and Paris'})
        self.assertEqual(new_method.status_code, 200)

    def test_update_nonexisting_bucketlists(self):
        '''
        Tests if API can udate an existing bucketlist (PUT request)
        Creates a new bucketlist and tries to update a none existing bucketlst
        Tests for (404-not found) status code response
        '''
        method = self.client().post('/bucketlists/1/items/1', data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        result = self.client().put('/bucketlists/2', data={'name': 'Visit London UK and Paris'})
        self.assertEqual(result.status_code, 404)

    def test_get_bucketlists(self):
        """
        Tests if API can get a bucketlist (GET request).
        Creates bucketlist and tests for (201-created) status code response
        Fetches created data and check if content is same as in the one created
        """
        method = self.client().post("/bucketlists/1/items/1", data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        new_method = self.client().get('/bucketlists/1')
        self.assertEqual(new_method.status_code, 200)
        self.assertIn('Visit London UK', str(method.data))

    def test_get_bucketlist_item(self):
        """
        Tests if API can get an item from bucketlist (GET request).
        Creates bucketlist and tests for (201-created) status code response
        Fetches an item from bucket list and tests for (200-Ok) status code
        """
        method = self.client().post("/bucketlists/1/items/1", data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        new_method = self.client().get('/bucketlists/1/items/1')
        self.assertEqual(new_method.status_code, 200)
        self.assertIn('Visit London UK', str(method.data))

    def test_get_nonexisting_bucketlist_item(self):
        """
        Tests if API can get an item that does not exist from bucketlist (GET request).
        Creates bucketlist and tests for (201-created) status code response
        Fetches an item that was not added to the bucket list and checks for (404-not found) status code
        """
        method = self.client().post("/bucketlists/1/items/1", data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        new_method = self.client().get('/bucketlists/1/items/23')
        self.assertEqual(new_method.status_code, 404)   

    def test_get_nonexisting_bucketlists(self):
        """
        Tests if API can get a bucketlist that does not exist (GET request).
        Creates bucketlist and tests for (201-created) status code response
        Fetches a none existing bucketlist then checks for (404-not found) status code response
        """
        method = self.client().post("/bucketlists/1/items/1", data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        new_method = self.client().get('/bucketlists/23')
        self.assertEqual(new_method.status_code, 404)       

    def test_get_bucketlist_by_id(self):
        """
        Tests if API can get a single item from bucketlists using it's id (GET request).
        Creates bucketlist and tests for (201-created) status code response
        Gets jasonified bicketlist data and tests for (200-Ok) status code response
        """
        method = self.client().post("/bucketlists/1/items/1", data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        json_conversion = json.loads(method.data.decode('utf-8').replace("'", "\""))
        result = self.client().get('/bucketlists/{}'.format(json_conversion['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Visit London UK', str(result.data))

    def test_post_existing_buketlists(self):
        """
        Tests if API can create a bucketlist that already exists (POST request)
        Creates a new bucketlist and tests for (201-created) status code response
        Creates a similar bucketlist and tests for (409-conflict) status code response
        """
        method = self.client().post('/bucketlists/1/items/1', data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        result = self.client().post("/bucketlists/", data=self.bucketlist)
        self.assertEqual(result.status_code, 409)

    def test_delete_bucketlist(self):
        """
        Tests if API can delete an existing bucketlist. (DELETE request).
        Creates bucketlist and tests for (201-created) status code response
        Deletes bucketlist and tests for (200-Ok) status code response
        Gets the deleted bucket list and tests for (404-not found) status code response
        """
        method = self.client().post("/bucketlists/1/items/1", data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        delet = self.client().delete('/bucketlists/1')
        self.assertEqual(delet.status_code, 200)
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlist_item(self):
        """
        Tests if API can delete an existing item from bucketlist. (DELETE request).
        Creates bucketlist and tests for (201-created) status code response
        Deletes bucketlist item and tests for (200-Ok) status code response
        Tries to fetch the deleted bucketlist and checks for (404-notfound) status code response
        """
        method = self.client().post("/bucketlists/1/items/1", data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        delet = self.client().delete('/bucketlists/1/items/1')
        self.assertEqual(delet.status_code, 200)
        result = self.client().get('/bucketlists/1/items/1')
        self.assertEqual(result.status_code, 404)    

    def test_delete_nonexisting_bucketlists(self):
        """
        Tests if API can delete a bucketlist that does not exist (DELETE request).
        Creates bucketlist and tests for (201-created) status code response
        Deletes bucketlist that does not exist and tests for (404-not found) status code response
        """
        method = self.client().post("/bucketlists/1/items/1", data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        result = self.client().delete('/bucketlists/2')
        self.assertEqual(result.status_code, 404)

    def test_delete_nonexisting_bucketlist_item(self):
        """
        Tests if API can delete an item that does not exist in bucketlist. (DELETE request).
        Creates bucketlist and tests for (201-created) status code response
        Tries to delet a bucketlist item that was not created and checks for (404-notfound) status code response
        """
        method = self.client().post("/bucketlists/1/items/1", data=self.bucketlist)
        self.assertEqual(method.status_code, 201)
        delet = self.client().delete('/bucketlists/1/items/125')
        self.assertEqual(delet.status_code, 404)


    def tearDown(self):
        """
        Teardown all initialized variables and drop all tables
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()            


