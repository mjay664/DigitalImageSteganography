

class KeyGen:
    def __init__(self):
        pass

    def get_key_set(self, key):
        key_1 = self.__get_key(key)
        if key_1 == 0:
            key_1 += 1
        key_2 = self.__get_key(key ^ key_1)
        if key_2 == 0:
            key_2 += 1

        return [key_1, key_2]

    def __int_to_binary(self, i):
        if i == 0: return "0"
        s = ''
        while i:
            if i & 1 == 1:
                s = "1" + s
            else:
                s = "0" + s
            i /= 2
        return s

    def __rotate_binary_num(self, number, rotate):
        str_data = number[rotate:] + number[0:rotate]
        return str_data

    def __mod256(self, number):
        tmp = number
        while tmp >= 256:
            tmp -= 256
        return tmp

    def __binary_str_to_int(self, binary_str):
        list_data = list(binary_str)
        list_data.reverse()
        tmp_num = 0

        for i in range(len(list_data)):
            tmp_num += int(list_data[i]) * (2 ** i)

        return tmp_num

    def __digit_adder(self, number):
        tmp = 0
        while number > 0:
            tmp += number % 10
            number = number / 10

        return tmp

    def __xor_numbers(self, number_1, number_2):
        binary_str_1 = self.__int_to_binary(number_1)
        binary_str_2 = self.__int_to_binary(number_2)
        len_1 = len(binary_str_1)
        len_2 = len(binary_str_2)
        xored_binary_str = ''

        if len_1 > len_2:
            s = ''
            for i in range(len_1 - len_2):
                s += '0'
            s += binary_str_2
            binary_str_2 = s

        else:
            s = ''
            for i in range(len_2 - len_1):
                s += '0'
            s += binary_str_1
            binary_str_1 = s

        for i in range(len(binary_str_1)):
            if binary_str_1[i] == binary_str_2[i]:
                xored_binary_str += '0'
            else:
                xored_binary_str += '1'

        return self.__binary_str_to_int(xored_binary_str)

    def __slice_binary_num(self, binary_num, num_slice):
        slice_list = []
        tmp = ''
        for i in range(len(binary_num)):
            tmp += binary_num[i]
            if (i + 1) % num_slice == 0:
                slice_list.append(tmp)
                tmp = ''

        return slice_list


    def __get_key(self, number):

        str_num = self.__int_to_binary(number)

        if len(str_num) % 8 != 0:
            tmp = ''
            for i in range(8 - (len(str_num) % 8)):
                tmp += '0'
            tmp += str_num
            str_num = tmp

        sum_of_digits = self.__digit_adder(number)

        number_after_rotation = self.__rotate_binary_num(str_num, sum_of_digits)

        slice_list = self.__slice_binary_num(number_after_rotation, 8)
        x = slice_list[0]
        for i in range(1, len(slice_list)):
            x = self.__xor_numbers(self.__binary_str_to_int(x), self.__binary_str_to_int(slice_list[i]))
            tmp_ = self.__digit_adder(x)
            x = self.__rotate_binary_num(self.__int_to_binary(x), tmp_)

        return self.__mod256(self.__binary_str_to_int(x))

