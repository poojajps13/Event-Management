from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator1(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.username) + six.text_type(timestamp) + six.text_type(user.is_active) + six.text_type(
            user.first_name)


account_activation_token = TokenGenerator1()


class TokenGenerator2(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.username) + six.text_type(timestamp) + six.text_type(user.last_login)


password_reset_token = TokenGenerator2()
