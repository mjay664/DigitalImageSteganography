from PIL import Image
import EncryptionAndDecryptionManager as EDM
import KeyManager as KM
import os
import tkMessageBox


class StagManager:
    def __init__(self, image_name):
        self.__im = Image.open(image_name)
        size = self.__im.size
        self.__im_height = size[0]
        self.__im_width = size[1]
        if size[0] > 1080:
            ratio = 1080.0 / size[0];
            self.__im = self.__im.resize((int(size[0] * ratio), int(size[1] * ratio)))
            size = self.__im.size
            self.__im_height = size[0]
            self.__im_width = size[1]
        self.__im_mode = self.__im.mode

    def __int_to_binary(self, i):
        if i == 0: return "0"
        s = ''
        while i:
            if i & 1 == 1:
                s = "1" + s
            else:
                s = "0" + s
            i /= 2

        k = ''
        for j in range(0, 8 - len(s)):
            k += '0'

        k += s
        s = k

        return s

    def __get_pixels(self):
        image_size = self.__im.size
        tmp_pix = self.__im.load()
        pixels = []

        for i in range(image_size[0]):
            tmp = []
            for j in range(image_size[1]):
                tmp.append(list(tmp_pix[i, j]))
            pixels.append(tmp)
        return pixels

    def __binary_str_to_int(self, binary_str):
        list_data = list(binary_str)
        list_data.reverse()
        tmp_num = 0

        for i in range(len(list_data)):
            tmp_num += int(list_data[i]) * (2 ** i)

        return tmp_num

    def __put_message_in_pixels(self, message, key):
        png = self.__im
        png.load()

        background = Image.new("RGB", png.size, (255, 255, 255))
        try:
            background.paste(png, mask=png.split()[3])
        except:
            background.paste(png)

        background.save('temp.png', 'PNG')
        self.__im = Image.open('temp.png')
        pixels = self.__get_pixels()
        os.remove('temp.png')
        list_l = []

        key_obj_1 = KM.KeyGen()

        enc_obj = EDM.EncryptionAndDecryption(key)

        encrypted_text = enc_obj.encrypt_text(message)
        encrypted_text_str = ''

        for i in encrypted_text:
            encrypted_text_str += self.__int_to_binary(i)
        key_set = key_obj_1.get_key_set(key)
        height_pre = key_set[0]
        key_pre = key_set[1]
        rgb_flag = 0

        for i in range(self.__im_height):
            for j in range(self.__im_width):
                pixels[i][j].append(255)

        for i in encrypted_text_str:
            if rgb_flag == 0:
                width_index = self.__im_width - key_pre
                height_index = self.__im_height - height_pre
            else:
                width_index = key_pre
                height_index = height_pre

            if i == '1':
                x_val = 254
            else:
                x_val = 253

            rgb_flag += 1
            if rgb_flag > 1:
                rgb_flag = 0

            pixels[height_index - 1][width_index - 1][3] = x_val

            t = (height_pre, key_pre, rgb_flag)
            i = 1
            while t in list_l:
                key_set = key_obj_1.get_key_set(height_pre+key_pre + i)
                key_pre = key_set[1]
                height_pre = key_set[0]
                t = (height_pre, key_pre, rgb_flag)
                i += 1
            list_l.append(t)

        return pixels

    def __get_message_from_image(self, key):
        pixels = self.__get_pixels()
        key_obj_1 = KM.KeyGen()
        key_set = key_obj_1.get_key_set(key)
        height_pre = key_set[0]
        key_pre = key_set[1]
        rgb_flag = 0
        list_l = []

        encrypted_text = []
        tmp_str = ''
        z_pix = 0

        while z_pix < 255:
            if rgb_flag == 0:
                width_index = self.__im_width - key_pre
                height_index = self.__im_height - height_pre
            else:
                width_index = key_pre
                height_index = height_pre

            z_pix = pixels[height_index-1][width_index-1][3]

            rgb_flag += 1

            if rgb_flag > 1:
                rgb_flag = 0

            if z_pix == 254:
                tmp_str += '1'
            elif z_pix == 253:
                tmp_str += '0'

            if len(tmp_str) == 8:
                encrypted_text.append(self.__binary_str_to_int(tmp_str))
                tmp_str = ''

            t = (height_pre, key_pre, rgb_flag)
            i = 1
            while t in list_l:
                key_set = key_obj_1.get_key_set(height_pre + key_pre + i)
                key_pre = key_set[1]
                height_pre = key_set[0]
                t = (height_pre, key_pre, rgb_flag)
                i += 1

            list_l.append(t)

        enc_obj = EDM.EncryptionAndDecryption(key)
        s = enc_obj.decrypt_text(encrypted_text)
        return s

    def hide_message(self, key, message):
        pixels = self.__put_message_in_pixels(message, key)

        im = Image.new("RGBA", (self.__im_height, self.__im_width))

        for i in range(self.__im_height):
            for j in range(self.__im_width):

                im.putpixel((i, j), tuple(pixels[i][j]))

        return im

    def show_message(self, key):
        try:
            message = self.__get_message_from_image(key)
            return message
        except:
            tkMessageBox.showinfo('Alert', 'No Message Found')
        return 'No hidden info'
