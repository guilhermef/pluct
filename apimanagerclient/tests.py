#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import unittest
from mock import patch, MagicMock
from apimanagerclient import Service
from apimanagerclient.service import Resource


class ServiceSchemaMock(MagicMock):
    content = json.dumps({
        "extensions": {
            "list_endpoint": "/v1/extensions/",
            "schema": "/v1/extensions/schema/"
        },
        "portals": {
            "list_endpoint": "/v1/portals/",
            "schema": "/v1/portals/schema/"
        }
    })



class ServiceTestCase(unittest.TestCase):


    def setUp(self):
        super(ServiceTestCase, self).setUp()
        self.request_mock = patch('requests.get').start()
        self.request_mock.return_value = ServiceSchemaMock()

        patch('apimanagerclient.service.Resource._get_schema').start()


        self.my_service = Service('http://my-api.com', 'v1')

    def test_should_have_url(self):
        self.assertEqual(self.my_service.url, 'http://my-api.com')

    def test_should_have_version(self):
        self.assertEqual(self.my_service.version, 'v1')


    def test_should_call_the_get_method(self):
        self.request_mock.assert_called_with(
            url='http://my-api.com/v1', params={'format': 'json'}
        )

    def test_should_obtain_resources(self):
        self.assertEqual(self.my_service.resources.keys(), [u'portals', u'extensions'])

    def test_should_create_resources(self):
        self.assertIsInstance(self.my_service.extensions, Resource)
        self.assertIsInstance(self.my_service.portals, Resource)


class ResourceSchemaMock(MagicMock):
    content = json.dumps({
        'allowed_list_http_methods': [
            "get"
        ],
        }
    )


class ResourceTestCase(unittest.TestCase):
    def setUp(self):
        super(ResourceTestCase, self).setUp()
        self.request_mock = patch('requests.get').start()
        self.request_mock.return_value = ResourceSchemaMock()

        self.my_resource = Resource(name='foo', service_url='http://my-api.com/v1')

    def test_should_obtain_service_url(self):
        my_resource = Resource(name='foo', service_url='http://my-api.com/v1')
        self.assertEqual(my_resource.url, 'http://my-api.com/v1/foo')

    def test_should_store_allowed_methods(self):
        my_resource = Resource(name='foo', service_url='http://my-api.com/v1')
        self.assertEqual(my_resource.methods, ['get',])


if __name__ == '__main__':
    unittest.main()
