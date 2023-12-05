import binascii


class BitUtils:
    @staticmethod
    def set_bit(value, bit):
        """Set the specified bit in the value."""
        return value | (1 << bit)

    @staticmethod
    def clear_bit(value, bit):
        """Clear the specified bit in the value."""
        return value & ~(1 << bit)

    @staticmethod
    def toggle_bit(value, bit):
        """Toggle the specified bit in the value."""
        return value ^ (1 << bit)

    @staticmethod
    def get_bit(value, bit):
        """Get the value of the specified bit in the value."""
        return (value >> bit) & 1

    @staticmethod
    def convert_to_hex(value):
        """Convert an integer to a hexadecimal string."""
        return hex(value)[2:]

    @staticmethod
    def pad_hex(value, length=2):
        """Pad a hexadecimal string with zeros to the specified length."""
        return f"{value:0>{length}}"

    @staticmethod
    def hex_to_binary(hex_string):
        """Convert a hexadecimal string to binary."""
        binary_string = bin(int(hex_string, 16))[2:]
        return binary_string.zfill(8 * ((len(binary_string) + 7) // 8))

    @staticmethod
    def binary_to_hex(binary_string):
        """Convert a binary string to hexadecimal."""
        hex_string = hex(int(binary_string, 2))[2:]
        return hex_string.zfill((len(hex_string) + 1) // 2 * 2)

    @staticmethod
    def int_to_hex(int_value):
        """Convert a int value to hexadecimal 4 chars."""
        return hex(int_value)[2:].upper().zfill(4)

    @staticmethod
    def hex_to_int(hex_value):
        """Convert a hax value to integer"""
        return int(hex_value, 16)

    @staticmethod
    def calculate_crc32_hex(data):
        crc32 = binascii.crc32(data.encode())
        crc32_hex = format(crc32 & 0xFFFFFFFF, '08X')
        return crc32_hex
