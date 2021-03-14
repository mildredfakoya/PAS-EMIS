import pytest

from helpers.encryption import AESEncrpytion
from models.user_models import UserEncryption


def test_encrypt():
    encrypt = AESEncrpytion()
    encrpyt_model = encrypt.encrypt(UserEncryption, "abc123")
    check_db = UserEncryption.query.get(encrpyt_model.id)
    assert check_db is not None


def test_decrypt():
    original_message = "abc123"
    # Encrpyt
    encrypt = AESEncrpytion()
    encrpyt_model = encrypt.encrypt(UserEncryption, original_message)
    query_model_from_db = UserEncryption.query.get(encrpyt_model.id)
    assert query_model_from_db is not None

    # Decrypt
    decrypt = AESEncrpytion()
    decrypted_message = decrypt.decrypt(UserEncryption, encrpyt_model.id)
    assert decrypted_message == original_message


def test_encrypt_one_line():
    encrpyt_model = AESEncrpytion().encrypt(UserEncryption, "abc123")
    check_db = UserEncryption.query.get(encrpyt_model.id)
    assert check_db is not None