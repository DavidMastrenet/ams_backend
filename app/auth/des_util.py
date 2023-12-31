# 初始置换 IP
IP_TABLE = [58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7]
# 逆置换
IPR_Table = [40, 8, 48, 16, 56, 24, 64, 32, 39,
             7, 47, 15, 55, 23, 63, 31, 38, 6,
             46, 14, 54, 22, 62, 30, 37, 5, 45,
             13, 53, 21, 61, 29, 36, 4, 44, 12,
             52, 20, 60, 28, 35, 3, 43, 11, 51,
             19, 59, 27, 34, 2, 42, 10, 50, 18,
             58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

# 扩展置换 E
E_TABLE = [32, 1, 2, 3, 4, 5, 4, 5,
           6, 7, 8, 9, 8, 9, 10, 11,
           12, 13, 12, 13, 14, 15, 16, 17,
           16, 17, 18, 19, 20, 21, 20, 21,
           22, 23, 24, 25, 24, 25, 26, 27,
           28, 29, 28, 29, 30, 31, 32, 1]

# P盒
P_BOX_TABLE = [16, 7, 20, 21, 29, 12, 28, 17,
               1, 15, 23, 26, 5, 18, 31, 10,
               2, 8, 24, 14, 32, 27, 3, 9,
               19, 13, 30, 6, 22, 11, 4, 25]

# S盒
S_BOX_TABLE = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],

]

# 子密钥置换PC2
KEY_TABLE = [14, 17, 11, 24, 1, 5, 3, 28,
             15, 6, 21, 10, 23, 19, 12, 4,
             26, 8, 16, 7, 27, 20, 13, 2,
             41, 52, 31, 37, 47, 55, 30, 40,
             51, 45, 33, 48, 44, 49, 39, 56,
             34, 53, 46, 42, 50, 36, 29, 32]

# 子密钥循环左移
MOVE_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def process_bt(temp_bt, first_key_bt, second_key_bt, third_key_bt):
    for i in range(len(first_key_bt)):
        temp_bt = enc(temp_bt, first_key_bt[i])
    for i in range(len(second_key_bt)):
        temp_bt = enc(temp_bt, second_key_bt[i])
    for i in range(len(third_key_bt)):
        temp_bt = enc(temp_bt, third_key_bt[i])
    return temp_bt


def raw_str_enc(data, first_key="1", second_key="2", third_key="3"):
    length = len(data)
    enc_data = ""
    first_key_bt = get_key_bytes(first_key)
    second_key_bt = get_key_bytes(second_key)
    third_key_bt = get_key_bytes(third_key)

    if length > 0:
        if length < 4:
            enc_data = bt64_to_hex(process_bt(str_to_bt(data), first_key_bt, second_key_bt, third_key_bt))
        else:
            iterator = int(length / 4)
            remainder = length % 4
            for i in range(iterator):
                enc_data = enc_data + bt64_to_hex(
                    process_bt(str_to_bt(data[i * 4:i * 4 + 4]), first_key_bt, second_key_bt, third_key_bt))
            if remainder > 0:
                enc_data += bt64_to_hex(
                    process_bt(str_to_bt(data[iterator * 4 + 0:length]), first_key_bt, second_key_bt, third_key_bt))
    return enc_data


def get_key_bytes(key):
    key_bytes = []
    length = len(key)
    iterator = int(length / 4)
    remainder = length % 4
    for i in range(iterator):
        key_bytes.append(str_to_bt(key[i * 4:i * 4 + 4]))
    if remainder > 0:
        key_bytes.append(str_to_bt(key[(iterator - 1) * 4:length]))
    return key_bytes


def str_to_bt(input_str):
    length = len(input_str)
    bt = [0 for _ in range(64)]
    if length < 4:
        for i in range(length):
            k = ord(str(input_str[i]))
            for j in range(16):
                bt[16 * i + j] = int(k / (2 ** (15 - j))) % 2
        for p in range(length, 4):
            k = 0
            for q in range(16):
                bt[16 * p + q] = int(k / (2 ** (15 - q))) % 2
    else:
        for i in range(4):
            k = ord(str(input_str[i]))
            for j in range(16):
                bt[16 * i + j] = int(k / (2 ** (15 - j))) % 2
    return bt


def bt64_to_hex(byte_data):
    hex_result = ""
    for i in range(16):
        bt = ""
        for j in range(4):
            bt = bt + byte_data[i * 4 + j]
        hex_result = hex_result + bt4_to_hex(bt)
    return hex_result


def bt4_to_hex(bt):
    return str(hex(int(bt, 2)))[2:].upper()


def process_change(bin_str, table):
    res = ""
    for i in table:
        res += str(bin_str[i - 1])
    return res


def str_xor(my_str1, my_str2):
    res = ""
    for i in range(0, len(my_str1)):
        xor_res = int(my_str1[i], 10) ^ int(my_str2[i], 10)
        if xor_res == 1:
            res += '1'
        if xor_res == 0:
            res += '0'

    return res


def s_box(my_str):
    res = ""
    c = 0
    for i in range(0, len(my_str), 6):
        now_str = my_str[i:i + 6]
        row = int(now_str[0] + now_str[5], 2)
        col = int(now_str[1:5], 2)
        num = bin(S_BOX_TABLE[c][row * 16 + col])[2:]
        for gz in range(0, 4 - len(num)):
            num = '0' + num
        res += num
        c += 1
    return res


def gen_key(key_byte):
    key = [0 for _ in range(56)]
    keys = [[] for _ in range(16)]
    for i in range(7):
        j = 0
        k = 7
        while True:
            if j >= 8:
                break
            key[i * 8 + j] = key_byte[8 * k + i]
            j = j + 1
            k = k - 1
    for i in range(16):
        for j in range(MOVE_TABLE[i]):
            temp_left = key[0]
            temp_right = key[28]
            for k in range(27):
                key[k] = key[k + 1]
                key[28 + k] = key[29 + k]
            key[27] = temp_left
            key[55] = temp_right
        temp_key = process_change(key, KEY_TABLE)
        keys[i] = temp_key
    return keys


def enc(bin_message, bin_key):
    ip = process_change(bin_message, IP_TABLE)
    keys = gen_key(bin_key)
    ip_left = ip[0:32]
    ip_right = ip[32:]

    for i in range(16):
        temp_left = ip_left
        ip_left = ip_right
        key = keys[i]

        temp_e = process_change(ip_right, E_TABLE)
        temp_xor1 = str_xor(temp_e, key)
        temp_s_box = s_box(temp_xor1)
        temp_p_box = process_change(temp_s_box, P_BOX_TABLE)
        temp_xor2 = str_xor(temp_p_box, temp_left)
        ip_right = temp_xor2

    return process_change(ip_right + ip_left, IPR_Table)
