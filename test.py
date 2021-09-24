import unittest
from app import app


class PostTestCase(unittest.TestCase):

    # Ensure that ping sends back correct json data
    def test_ping_json(self):
        tester = app.test_client(self)
        response = tester.get('/api/ping')
        self.assertEqual(response.get_json(), {'success': True})

    # Ensure that ping sends back correct status code
    def test_ping_status(self):
        tester = app.test_client(self)
        response = tester.get('/api/ping')
        self.assertEqual(response.status_code, 200)

    # Ensure that posting a post is working properly
    # Commented out since there already exists a post with id 10
    # def test_post_post(self):
    #     tester = app.test_client(self)
    #     response = tester.post('/api/posts',
    #                            json={"id": 10, "author": "Rylee Paul", "authorId": 9, "likes": 960,
    #                                  "popularity": 0.13, "reads": 50361, "tags": ["tech", "health"]})
    #     self.assertEqual(response.status_code, 201)

    # Ensure that posting post with pre-existing id generates error
    def test_post_error(self):
        tester = app.test_client(self)
        response = tester.post('/api/posts',
                               json={"id": 10, "author": "Rylee Paul", "authorId": 9, "likes": 960, "popularity": 0.13,
                                     "reads": 50361, "tags": ["tech", "health"]})
        self.assertEqual(response.get_json()["error"], 'Post with same id already exists')

    # Ensure that getting posts with valid parameters works successfully
    def test_get_post(self):
        tester = app.test_client(self)
        response = tester.get('/api/posts?tags=science,tech&sortBy=likes&direction=desc')
        self.assertEqual(response.status_code, 200)

    # Ensure that getting posts without tag parameters returns an intended error message
    def test_get_no_tag(self):
        tester = app.test_client(self)
        response = tester.get('/api/posts?sortBy=likes&direction=desc')
        self.assertEqual(response.get_json()["error"], 'Tags parameter is required')

    # Ensure that getting posts with invalid sortby parameter returns an intended error message
    def test_get_invalid_sortby(self):
        tester = app.test_client(self)
        response = tester.get('/api/posts?tags=science,tech&sortBy=hi&direction=desc')
        self.assertEqual(response.get_json()["error"], 'sortBy parameter is invalid')

    # Ensure that getting posts with invalid direction parameter returns an intended error message
    def test_get_invalid_dir(self):
        tester = app.test_client(self)
        response = tester.get('/api/posts?tags=science,tech&sortBy=likes&direction=des')
        self.assertEqual(response.get_json()["error"], 'direction parameter is invalid')


if __name__ == '__main__':
    unittest.main()
