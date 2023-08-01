def _list_to_bits_list(char_list: list):
    result = ""
    for byte in char_list:
        ascii_val = ord(byte)
        result += _to_32_bit(ascii_val)

    return result


def _to_32_bit(num: int) -> str:
    return str(bin(num))[2:].zfill(32)


def _to_8_bit(num: int) -> str:
    if len(str(num)) < 1:
        num = "0" * 8

    return str(bin(num))[2:].zfill(8)


def _calculate_byte_size(hash_length_in_bytes) -> int:
    bytes_number = 0

    while bytes_number * 256 < hash_length_in_bytes:
        bytes_number += 1

    return bytes_number


def _rotate_right(x: str, rotations: int) -> str:
    """
    Performs right rotation on the bits of a binary value.
    :param x: The binary value in string to rotate
    :param rotations: The number of rotations to perform.
    :return: The rotated binary string.
    """
    binary = x.zfill(rotations)  # Pad the binary value with leading zeros if necessary
    rotated_binary = binary[-rotations:] + binary[:-rotations]  # Perform right rotation
    rotated_binary = rotated_binary.zfill(32)
    return rotated_binary


def _shift(x: str, num_bits: int) -> str:
    """
    Shifts the first 'num_bits' bits of a binary value to 0.
    :param x: The binary value to perform the shift on.
    :param num_bits: The number of bits to shift to 0.
    :return: The result of shifting the bits as a binary string.
    """
    if len(x) < num_bits:
        raise "Length is shorter than should be!"

    for i in range(num_bits):
        start = x[0:i]
        end = x[i + 1:]
        x = start + '0' + end

    return x


def _add_modulus_two_three(x, y, z):
    result = 0

    for i in range(32):
        bit_sum = (int(x[i]) + int(y[i]) + int(z[i])) % 2
        result = (result << 1) | bit_sum

    result = _to_32_bit(result)
    return result


def _add_modulus_two(x, y):
    """
    Adds the bits of two hexadecimal variables modulo 2.
    :param x: The first hexadecimal variable.
    :param y: The second hexadecimal variable.
    :return: The result of the addition modulo 2 as a hexadecimal value.
    """
    result = 0

    for i in range(32):
        bit_sum = (int(x[i]) + int(y[i])) % 2
        result = (result << 1) | bit_sum

    result = _to_32_bit(result)

    return result


def _add_modulus_two_five(a, b, c, d, e):
    """
    Adds the bits of five hexadecimal variables a, b, c, d, and e modulo 2.
    :param a: The first hexadecimal variable.
    :param b: The second hexadecimal variable.
    :param c: The third hexadecimal variable.
    :param d: The fourth hexadecimal variable.
    :param e: The fifth hexadecimal variable.
    :return: The result of the addition modulo 2 as a hexadecimal value.
    """
    result = 0

    for i in range(32):
        bit_sum = (int(a[i]) + int(b[i]) + int(c[i]) + int(d[i]) + int(e[i])) % 2
        result = (result << 1) | bit_sum

    result = _to_32_bit(result)

    return result


def _add_modulus_two_four(a, b, c, d):
    """
    Adds the bits of four hexadecimal variables a, b, c, and d modulo 2.
    :param a: The first hexadecimal variable.
    :param b: The second hexadecimal variable.
    :param c: The third hexadecimal variable.
    :param d: The fourth hexadecimal variable.
    :return: The result of the addition modulo 2 as a hexadecimal value.
    """
    result = 0

    for i in range(32):
        bit_sum = (int(a) + int(b[i]) + int(c[i]) + int(d[i])) % 2
        result = (result << 1) | bit_sum

    result = _to_32_bit(result)

    return result


def _sigma0(num: str):
    x = _rotate_right(num, 7)
    y = _rotate_right(x, 18)
    z = _shift(y, 3)
    return _add_modulus_two_three(x, y, z)


def _sigma1(num):
    x = _rotate_right(num, 17)
    y = _rotate_right(x, 19)
    z = _shift(num, 10)
    return _add_modulus_two_three(x, y, z)


def _capital_sigma0(num):
    x = _rotate_right(num, 2)
    y = _rotate_right(x, 13)
    z = _rotate_right(y, 22)

    return _add_modulus_two_three(x, y, z)


def _capital_sigma1(num):
    x = _rotate_right(num, 6)
    y = _rotate_right(x, 11)
    z = _rotate_right(y, 25)

    return _add_modulus_two_three(x, y, z)


def _Ch(e, f, g):
    """
    Performs the bitwise operation on the bits of e, selecting bits from f or g based on the bit value of e.
    :param e: Binary value as a string.
    :param f: Binary value as a string.
    :param g: Binary value as a string.
    :return: Integer value representing the result after performing the operation.
    """
    result = 0
    for i in range(32):
        bit = int(e[i])  # Get the i-th bit of e
        selected_bit = f[i] if bit == 1 else g[i]  # Select the corresponding bit from f or g
        result = (result << 1) | int(selected_bit)  # Append the selected bit to the result

    result = _to_32_bit(result)
    return result


def _get_list_range_as_string(my_list, start, end):
    """
    Returns a string containing a specified range of bytes from the given list of integers.
    Each integer in the list is treated as a 4-byte little-endian representation.
    :param my_list: The list of integers from which to extract the range of bytes.
    :param start: The index of the first byte in the range.
    :param end: The index of the last byte in the range (exclusive).
    :return: A string containing the bytes in the specified range, represented as bits.
    :raises ValueError: If the start or end indices are out of range.
    """
    try:
        # To bytes
        start = int(start / 4)
        end = int(end / 4)
        byte_range = my_list[start:end]

        bit_string = ""
        ascii_val = 0
        for byte in byte_range:
            ascii_val = ord(byte)
            bit_string += _to_8_bit(ascii_val)

        return _to_32_bit(ascii_val)
    except (IndexError, TypeError):
        raise ValueError("Start or end indices are out of range.")


def _Maj(a, b, c):
    """
    Calculates the majority value of each bit among the three binary variables a, b, and c.
    :param a: The first binary variable.
    :param b: The second binary variable.
    :param c: The third binary variable.
    :return: The result of the majority calculation as a binary string.
    """
    result = ""
    for i in range(len(a)):
        try:
            bit_sum = int(a[i]) + int(b[i]) + int(c[i])
            bit_value = "1" if bit_sum >= 2 else "0"
            result += bit_value
        except ValueError:
            raise ValueError
    return result


def to_hex(binary_string: str) -> str:
    """
    Converts a 32-bit binary string to a hexadecimal string without the "0x" prefix.
    :param binary_string: The 32-bit binary string to convert.
    :return: The hexadecimal string representation of the binary value.
    """
    decimal_value = int(binary_string, 2)
    hex_string = hex(decimal_value)[2:].zfill(8)  # Convert to hexadecimal and pad with leading zeros if necessary
    return hex_string


def _create_hex_string(hex_values):
    """
    Creates a string from a list of hexadecimal values.
    :param hex_values: A list of hexadecimal values.
    :return: A string representing the concatenated hex values without the '0x' prefix.
    """
    hex_string = ''.join(hex_values).replace('0x', '')
    return hex_string


def _cut_string_to_length(string):
    if len(string) <= 32:
        return string
    else:
        return string[-32:]


class Hash:
    BIT = 1 / 8
    BYTE = int(8 * BIT)
    BLOCK_SIZE = 64

    def __init__(self, stream: str):
        self.hash_value = stream
        self.hash_length = len(stream)
        self.hash_bytes_list = list(stream)
        self.bits_string = _list_to_bits_list(self.hash_bytes_list)

    def _get_blocks_size(self, length: int) -> int:
        """
        Calculates the closest multiple of 64 bytes that is greater than or equal to the given length.
        :param length: in bytes of the hash
        :return: the closest multiple of 64 bytes that is greater or equal to the given length
        :raise:  SystemExit: If the length is less than 0
        """

        if length < 0:
            raise "Length can't be less than 0!"

        num_of_blocks = 0

        while num_of_blocks < length:
            num_of_blocks += self.BLOCK_SIZE

        return int(num_of_blocks / self.BYTE)

    def _add_one(self):
        self.bits_string += "1"

    def _add_zero(self):
        self.bits_string += "0"

    def _add_padding(self, block_size_bit: int):
        # Add the first 1
        self._add_one()

        # Padding of 0's until block size - 8
        while len(self.bits_string) < (block_size_bit - 64):
            self._add_zero()

    def _add_original_length(self):
        """
        The function calculates how many bytes are needed to represent the original length. Then it appends empty
        bytes and then the original length in bytes to the end of the hash bytes
        :return: None
        """
        length = _calculate_byte_size(
            self.hash_length)  # How many bytes needed to represent the length?
        length_in_bits = str(bin(len(self.hash_value)))[2:]
        for i in range(8):
            if 8 - i == length:
                self.bits_string += length_in_bits
                break

            self._add_zero()

    def calculate_hash(self):
        # Convert to the closest multiple of 64 (from above)
        block_size = self._get_blocks_size(self.hash_length)
        block_size_bit = block_size * 8
        # Add padding
        self._add_padding(block_size_bit)

        # Last 64 represent the original input length
        self._add_original_length()

        print("Passed original length")

        N = int(block_size / 64)
        row_size = int(block_size / 16)

        # Setting hash values
        m_values = []
        for i in range(16):
            m = _get_list_range_as_string(self.hash_bytes_list, i * row_size, (i + 1) * row_size)
            m_values.append(m)

        m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15 = m_values

        # Calculated using first 8 prime numbers: 2, 3, 5, 7, 11, 13, 17, 19
        H0 = 0x6a09e667
        H1 = 0xbb67ae85
        H2 = 0x3c6ef372
        H3 = 0xa54ff53a
        H4 = 0x510e527f
        H5 = 0x9b05688c
        H6 = 0x1f83d9ab
        H7 = 0x5be0cd19

        k = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        ]

        w = [
            m0, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15
        ]

        # Set the W values
        for _ in range(N):
            for i in range(64 - 16):
                t = i + 16

                a = _sigma1(w[t - 2])
                b = w[t - 7]
                c = _sigma0(w[t - 15])
                d = w[t - 16]

                w.append(None)
                w[t] = _add_modulus_two_four(a, b, c, d)

            a = _to_32_bit(H0)
            b = _to_32_bit(H1)
            c = _to_32_bit(H2)
            d = _to_32_bit(H3)
            e = _to_32_bit(H4)
            f = _to_32_bit(H5)
            g = _to_32_bit(H6)
            h = _to_32_bit(H7)

            for t in range(64):
                T1 = _add_modulus_two_five(h, _capital_sigma1(e), _Ch(e, f, g), _to_32_bit(k[0]), w[0])
                T2 = _add_modulus_two(_capital_sigma0(a), _Maj(a, b, c))
                h = g
                g = f
                f = e
                e = _add_modulus_two(d, T1)
                d = c
                c = b
                b = a
                a = _add_modulus_two(T1, T2)

            H0 = _add_modulus_two(a, _to_32_bit(H0))
            H1 = _add_modulus_two(b, _to_32_bit(H1))
            H2 = _add_modulus_two(c, _to_32_bit(H2))
            H3 = _add_modulus_two(d, _to_32_bit(H3))
            H4 = _add_modulus_two(e, _to_32_bit(H4))
            H5 = _add_modulus_two(f, _to_32_bit(H5))
            H6 = _add_modulus_two(g, _to_32_bit(H6))
            H7 = _add_modulus_two(h, _to_32_bit(H7))

        return _create_hex_string([to_hex(H0), to_hex(H1), to_hex(H2), to_hex(H3), to_hex(H4), to_hex(H5), to_hex(H6),
                                   to_hex(H7)])
