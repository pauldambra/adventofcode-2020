from __future__ import annotations
import re


class ThirtySixBitNumber:

    def __init__(self, *args) -> None:
        if isinstance(args[0], int):
            self.value = args[0]
            self.bits = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

            remaining = args[0]
            for index in range(0, 36):
                power = 35 - index
                position_value = pow(2, power)
                if remaining > 0 and remaining >= position_value:
                    self.bits[index] = 1
                    remaining -= position_value

        else:
            self.bits = args[0]
            self.set_value_from_bits()

    def set_value_from_bits(self):
        self.value = 0
        for power in range(0, 36):
            i = 35 - power
            position_value = pow(2, power)
            if self.bits[i] == 1:
                self.value += position_value

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ThirtySixBitNumber):
            return False

        return self.bits == o.bits

    def __hash__(self):
        return self.value.__hash__()

    def __repr__(self) -> str:
        return f"value: {self.value} for bits {self.bits}"

    def copy(self):
        return ThirtySixBitNumber(self.value)

    def set_bit(self, index: int, value: int) -> ThirtySixBitNumber:
        bits = self.bits.copy()
        bits[index] = value
        return ThirtySixBitNumber(bits)

    def set_bit_in_place(self, index: int, value: int) -> ThirtySixBitNumber:
        self.bits[index] = value
        self.set_value_from_bits()
        return self


class BitMask:

    def __init__(self, mask: str) -> None:
        self.mask = mask

    def apply_to(self, num: ThirtySixBitNumber) -> ThirtySixBitNumber:
        copy = num.copy()
        for i, m in enumerate(self.mask):
            if m != "X":
                copy = copy.set_bit(i, int(m))

        return copy

    def __eq__(self, o: object) -> bool:
        if isinstance(o, BitMask):
            return self.mask == o.mask
        else:
            return False

    def __repr__(self) -> str:
        return f"BitMask: {self.mask}"


class VersionOneDecoderProgram:
    def __init__(self) -> None:
        self.bitmask: BitMask = None
        self.memory = {}

    def process_line(self, line: str):
        if line.startswith('mask'):
            self.bitmask = BitMask(line.split(" = ")[1].strip())
        elif line.startswith("mem"):
            match = re.match(r"mem\[(\d+)] = (\d+)", line)
            address = int(match.group(1))
            num = ThirtySixBitNumber(int(match.group(2)))
            self.memory[address] = self.bitmask.apply_to(num).value

    def sum_memory(self):
        return sum(self.memory.values())
