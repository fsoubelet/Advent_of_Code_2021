"""
--- Part Two ---

Now that you have the structure of your transmission decoded, you can calculate the value of the expression it represents.

Literal values (type ID 4) represent a single number as described above. The remaining type IDs are more interesting:

    Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
    Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
    Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.

Using these rules, you can now work out the value of the outermost packet in your BITS transmission.

For example:

    C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
    04005AC33890 finds the product of 6 and 9, resulting in the value 54.
    880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
    CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
    D8005AC2A8F0 produces 1, because 5 is less than 15.
    F600BC2D8F produces 0, because 5 is not greater than 15.
    9C005AC2F8F0 produces 0, because 5 is not equal to 15.
    9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.

What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?
"""
# Committing this code after unifying the approach for part 1 and 2
from math import prod
from pathlib import Path
from typing import Tuple

ID_TO_OPERATION = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda x: int(x[0] > x[1]),
    6: lambda x: int(x[0] < x[1]),
    7: lambda x: int(x[0] == x[1]),
}


def hexadecimal_to_binary(string: str) -> str:
    """
    Convert a hexadecimal string to its binary equivalent, still as a string.
    Inspired from https://stackoverflow.com/questions/1425493/convert-hex-to-binary
    """
    return "".join(f"{int(x, 16):04b}" for x in string)  # each character is a 4-lengthed binary


def parse_numbers(binary_string: str) -> Tuple[int, int]:
    """Given the binary version of the transmission, parses the numbers."""
    pointer, numbers = 0, []
    while True:
        numbers.append(binary_string[pointer + 1 : pointer + 5])
        if binary_string[pointer] == "0":
            break
        pointer += 5  # jump to the next number
    return 5 * len(numbers), int("".join(numbers), base=2)


def parse_message(binary_string: str) -> Tuple[int, int, int]:
    """Given the binary version of the transmission string, parse subpackets and return the solutions."""
    version = int(binary_string[:3], base=2)  # version is encoded in the first 3 characters
    type_id = int(binary_string[3:6], base=2)  # type ID is the next 3 characters
    pointer = 6  # to remember our position in the string

    if type_id == 4:  # If we've got a literal value, parse and return
        p, n = parse_numbers(binary_string[pointer:])
        return version, n, pointer + p

    version_sum = version
    numbers = []

    # Ok, now we need to parse the sub-packets
    if (
        binary_string[pointer] == "0"
    ):  # length type ID is 0, "the next 15 bits represent the total length in bits of the sub-packets contained in this packet"
        len_subpackets = int(binary_string[pointer + 1 : pointer + 16], base=2)
        pointer += 16  # this will put us at the start of the first sub-packet (after these 15 bits)
        parse_until = pointer + len_subpackets  # this will be the end of the sub-packets

        while pointer < parse_until:  # parse the sub-packets, recursively
            v, n, p = parse_message(binary_string[pointer:])
            pointer += p
            version_sum += v
            numbers.append(n)

    else:  # Otherwise, "the next 11 bits are represent the number of sub-packets immediately contained by this packet"
        n_subpackets = int(binary_string[pointer + 1 : pointer + 12], base=2)
        pointer += 12
        for _ in range(n_subpackets):  # we parse them recursively too
            v, n, p = parse_message(binary_string[pointer:])
            pointer += p
            version_sum += v
            numbers.append(n)

    # We're done :)
    return version_sum, ID_TO_OPERATION[type_id](numbers), pointer


if __name__ == "__main__":
    transmission: str = Path("inputs.txt").read_text()
    part1, part2, _ = parse_message(binary_string=hexadecimal_to_binary(transmission))
    print(part2)
