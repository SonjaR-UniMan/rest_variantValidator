from locust import HttpLocust, TaskSet, task, between
import test_set

"""
Run locust against local dev server:

Activate the API in dev mode in a terminal

$ python wsgi.py

Run locust in a second terminal

$ locust -f locust/locust.py

Perform test at http://127.0.0.1:8089 (docs at https://docs.locust.io/en/latest/quickstart.html)


# Run locust against app on a server

"""

class UserBehavior(TaskSet):
    """
    Endpoint load-testing for the VariantValidator REST API

    Current tasks:
    @task(1) tests the variantvalidator endpoints with a randonly selected variant from a list
    @task(2) tests the gene2transcript endpoints with a randonly selected gene symbol from a list

    Note: These are the two most heavily used tools, but more tests will be added
    """
    @task(2)
    def index(self):
        random_task = test_set.gene_list()
        url = "VariantValidator/tools/gene2transcripts/%s?content-type=application/json" % random_task
        self.client.get(url)

    @task(1)
    def profile(self):
        odd_job = test_set.variant_list()
        # Make a request to the current VariantValidator rest-API
        url = '/'.join(['VariantValidator/variantvalidator',
                        'GRCh37',
                        odd_job,
                        'all?content-type=application/json'
                        ])
        self.client.get(url)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(0, 10) # seconds
