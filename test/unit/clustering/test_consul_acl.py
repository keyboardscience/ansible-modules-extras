import unittest
import mock
import yaml
import inspect
import collections

from ansible.compat.tests import unittest
from ansible.modules.extras.clustering import consul_acl

'''
Test suite to test argument processing
'''
class ArgumentsConsulACLTestCase(unittest.TestCase):
    @mock.patch("ansible.modules.extras.clustering.consul_acl.AnsibleModule")
    def test_arguments_processing(self, mock_module):
        consul_acl.main()
        mock_module.assert_called_with(
                    dict(
                        mgmt_token=dict(required=True, no_log=True),
                        host=dict(default='localhost'),
                        name=dict(required=False),
                        port=dict(default=8500, type='int'),
                        rules=dict(default=None, required=False, type='list'),
                        ssl=dict(default=False, required=False, type='bool'),
                        ssl_verify=dict(default=False, required=False, type='bool'),
                        state=dict(default='present', choices=['present', 'absent']),
                        token=dict(required=False, no_log=True),
                        token_type=dict(required=False, choices=['client', 'management'], default='client', aliases=['type'])

                    ), supports_check_mode=False
                )


'''
Test suite to test #get_consul_api
'''
class TLSConsulACLTestCase(unittest.TestCase):
    @mock.patch("ansible.modules.extras.clustering.consul_acl.AnsibleModule", params=dict(host="localhost", port=8500, ssl=False, ssl_verify=False))
    def test_get_consul_api_http(self, mock_module):
        '''
        get_consul_api - test with SSL disabled
        '''

        ret_val = consul_acl.get_consul_api(mock_module)
        self.assertEqual(ret_val.scheme, 'http')

    @mock.patch("ansible.modules.extras.clustering.consul_acl.AnsibleModule", params=dict(host="localhost", port=8500, ssl=True, ssl_verify=False))
    def test_get_consul_api_https(self, mock_module):
        '''
        get_consul_api - test with SSL enabled
        '''

        ret_val = consul_acl.get_consul_api(mock_module)
        self.assertEqual(ret_val.scheme, 'https')

    @mock.patch("ansible.modules.extras.clustering.consul_acl.AnsibleModule", params=dict(host="localhost", port=8500, ssl=True, ssl_verify=False))
    def test_get_consul_api_https_verify_off(self, mock_module):
        '''
        get_consul_api - test with SSL Verification disabled
        '''

        ret_val = consul_acl.get_consul_api(mock_module)
        self.assertEqual(ret_val.scheme, 'https')
        self.assertEqual(ret_val.http.verify, False)

    @mock.patch("ansible.modules.extras.clustering.consul_acl.AnsibleModule", params=dict(host="localhost", port=8500, ssl=True, ssl_verify=True))
    def test_get_consul_api_https_verify_on(self, mock_module):
        '''
        get_consul_api - test with SSL Verification enabled
        '''

        ret_val = consul_acl.get_consul_api(mock_module)
        self.assertEqual(ret_val.scheme, 'https')
        self.assertEqual(ret_val.http.verify, True)

