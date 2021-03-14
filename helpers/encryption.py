from Crypto.Cipher import AES

"""
How encyption works:
https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
"""
# original_message = "hello world"
# cipher = AES.new(key.encode("utf8"), AES.MODE_EAX)
# nonce = cipher.nonce
# ciphertext, tag = cipher.encrypt_and_digest(original_message.encode("utf8"))
# print("Cipher", ciphertext, tag)

# cipher = AES.new(key.encode("utf8"), AES.MODE_EAX, nonce=nonce)
# plaintext = cipher.decrypt(ciphertext)
# print("Decrypyed message", plaintext)


class AESEncrpytion:
    def __init__(self):
        self.key = "donotsteal$$$$$$"
        self.cipher = AES.new(self.key.encode("utf8"), AES.MODE_EAX)
        self.nonce = self.cipher.nonce

    def encrypt(self, Model, message):
        from app import db

        """
        We'll prob need to vertically shard the encyption DB so this method
        takes in a Model and a message to encrypt
        """
        ciphertext, tag = self.cipher.encrypt_and_digest(message.encode("utf8"))
        new_encryption = Model(tag=tag, ciphertext=ciphertext, nonce=self.nonce)
        db.session.add(new_encryption)
        db.session.commit()
        return new_encryption

    def decrypt(self, Model, id):
        encryptedvalue = Model.query.get(id)
        if not encryptedvalue:
            raise Exception("Invalid id to decrypt")

        cipher = AES.new(
            self.key.encode("utf8"), AES.MODE_EAX, nonce=encryptedvalue.nonce
        )
        return cipher.decrypt(encryptedvalue.ciphertext).decode("utf-8")
