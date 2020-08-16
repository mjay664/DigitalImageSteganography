import KeyManager as KM


class EncryptionAndDecryption:
    def __init__(self, key):
        self.__key = key

    def __text_to_int_converter(self, text):
        list_of_ints = []
        for i in text:
            list_of_ints.append(ord(i))

        return list_of_ints

    def __int_to_text_converter(self, int_list):
        str_data = ''
        for i in int_list:
            str_data += chr(i)

        return str_data

    def encrypt_text(self, message):
        key_obj = KM.KeyGen()

        key_set = key_obj.get_key_set(self.__key)

        text_in_int_form = self.__text_to_int_converter('&'+message)

        for i in key_set:
            encrypted_text = []
            for j in text_in_int_form:
                encrypted_text.append(~(i ^ j))
            text_in_int_form = encrypted_text

        return encrypted_text

    def decrypt_text(self, encrypted_data):
        key_obj = KM.KeyGen()

        key_set = key_obj.get_key_set(self.__key)
        key_set.reverse()

        for i in key_set:
            decrypted_text = []
            for j in encrypted_data:
                decrypted_text.append(~(i ^ j))
            encrypted_data = decrypted_text
        s = self.__int_to_text_converter(encrypted_data)

        return s[1:]
