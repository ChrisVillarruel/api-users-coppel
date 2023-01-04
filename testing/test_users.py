import unittest

from config.backends import set_password, get_password, DecodeJWTToken, CreateJWTToken


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


class TestCaseCreateJWTToken(unittest.TestCase):
    def setUp(self) -> None:
        self.token = CreateJWTToken

    def test_create_jwt_token(self):
        token = self.token(user_id="56122589966210001")
        self.assertIsInstance(token.payload, dict)
        self.assertIsInstance(token.payload.get("iss"), str)
        self.assertIsInstance(token.create_jwt(), str)


class TestCaseDecodeJWTToken(unittest.TestCase):
    def setUp(self) -> None:
        self.token = DecodeJWTToken

    def test_create_jwt_token(self):
        token = self.token(
            jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2M2I1MTgzNzYyNDkwOWZjMjJiNjFjNTciLCJleHAiOjE2NzM2NzY2MDQuNTgxMTE5LCJpYXQiOjE2NzI4MTI2MDQuNTgxMTY2fQ._jPxazT5iiY3Yjwg5zWyWMSoQojbIYGoC5G_QvTl-c0")
        self.assertIsInstance(token.decode_jwt(), dict)


unittest.main()
