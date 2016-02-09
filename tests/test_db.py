import unittest

import signac.db

try:
    signac.db.get_database('testing', hostname='testing')
except signac.common.errors.ConfigError:
    SKIP_REASON = "No 'testing' host configured."
except ImportError:
    SKIP_REASON = "pymongo not available"
else:
    SKIP_REASON = None
    import signac.common.host


@unittest.skipIf(SKIP_REASON is not None, SKIP_REASON)
class DBTest(unittest.TestCase):

    def get_test_db(self):
        signac.db.get_database('testing', hostname='testing')

    def test_get_connector(self):
        signac.common.host.get_connector(hostname='testing')

    def test_get_connector_no_client(self):
        c = signac.common.host.get_connector(hostname='testing')
        with self.assertRaises(RuntimeError):
            c.client

    def test_get_client(self):
        signac.common.host.get_client(hostname='testing')

    def test_connector_get_host(self):
        host_config = signac.common.host.get_host_config(hostname='testing')
        c = signac.common.host.get_connector(hostname='testing')
        self.assertEqual(host_config['url'], c.host)
        self.assertEqual(host_config, c.config)

    def test_logout(self):
        c = signac.common.host.get_connector(hostname='testing')
        with self.assertRaises(RuntimeError):
            c.client
        c.connect()
        c.client
        c.authenticate()
        c.logout()

if __name__ == '__main__':
    unittest.main()
