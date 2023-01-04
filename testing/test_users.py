import unittest
from config.backends import set_password, get_password


class TestCaseHashPasswordUser(unittest.TestCase):
    def test_set_password(self):
        user_password = "givc980909@se8453"
        hash_password = set_password(user_password)

        self.assertIsInstance(hash_password, str)
        self.assertNotEqual(user_password, hash_password)
        self.assertNotIsInstance(hash_password, bytes)

    def test_get_password(self):
        hash_password = "gAAAAABjtKZuLGrfgP7de4BTVyPuPR_6whWqx7xft0PVkR7jfzRL-fxBqpOzA-En6jwD-JLtATKIdcbfSS5KsWPuzFkcRsqWxlUBtU-X4Uf3sLwGs_mqDlc="
        user_password = "givc980909@se8453"

        password = get_password(hash_password, user_password)

        self.assertIsInstance(password, bool)
        self.assertIs(password, True)
