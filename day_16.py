import itertools as it
from math import prod

class Packet:
    def __init__(self, raw, start=0):
        self.version = int("".join(raw[start:start+3]),2)
        self.type = int("".join(raw[start+3:start+6]),2)

        cursor = start+6

        if self.type == 4:
            # Literal value
            bits = []
            while True:
                done, *nextbits = raw[cursor:cursor+5]
                bits.extend(nextbits)
                cursor += 5
                
                if done == "0":
                    break
            
            self._value = int("".join(bits), 2)
        else:
            # operator packet with subpackets
            self.subpackets = []
            length_type = raw[cursor]
            cursor += 1

            if length_type == "0":
                bit_length = int("".join(raw[cursor:cursor+15]), 2)
                cursor += 15
                consumed = 0
                while consumed < bit_length:
                    nextpacket = Packet(raw, cursor)
                    self.subpackets.append(nextpacket)
                    cursor += nextpacket.length
                    consumed += nextpacket.length

            else:
                subpacket_length = int("".join(raw[cursor:cursor+11]), 2)
                cursor += 11
                for _ in range(subpacket_length):
                    nextpacket = Packet(raw, cursor)
                    self.subpackets.append(nextpacket)
                    cursor += nextpacket.length

        self.length = cursor - start


    @property
    def value(self):
        match self.type:
            case 0:
                return sum(p.value for p in self.subpackets)
            case 1:
                return prod(p.value for p in self.subpackets)
            case 2:
                return min(p.value for p in self.subpackets)
            case 3:
                return max(p.value for p in self.subpackets)
            case 4:
                return self._value
            case 5:
                return int(self.subpackets[0].value > self.subpackets[1].value)
            case 6:
                return int(self.subpackets[0].value < self.subpackets[1].value)
            case 7:
                return int(self.subpackets[0].value == self.subpackets[1].value)

    def walk(self):
        yield self
        if hasattr(self, "subpackets"):
            for packet in self.subpackets:
                yield from packet.walk()

def _parse(rawdata):
    trans = {
        "0" : "0000",
        "1" : "0001",
        "2" : "0010",
        "3" : "0011",
        "4" : "0100",
        "5" : "0101",
        "6" : "0110",
        "7" : "0111",
        "8" : "1000",
        "9" : "1001",
        "A" : "1010",
        "B" : "1011",
        "C" : "1100",
        "D" : "1101",
        "E" : "1110",
        "F" : "1111",
    }
    bindata = list(it.chain.from_iterable(trans[h] for h in rawdata.strip()))
    return [Packet(bindata)]

def part_1(packet):
    r"""
    >>> part_1(*_parse('''\
    ... 8A004A801A8002F478
    ... '''))
    16
    >>> part_1(*_parse('''\
    ... 620080001611562C8802118E34
    ... '''))
    12
    >>> part_1(*_parse('''\
    ... C0015000016115A2E0802F182340
    ... '''))
    23
    >>> part_1(*_parse('''\
    ... A0016C880162017C3686B18A3D4780
    ... '''))
    31

    """
    return sum(p.version for p in packet.walk()) 


def part_2(packet):
    r"""
    >>> part_2(*_parse("C200B40A82"))
    3
    >>> part_2(*_parse("04005AC33890"))
    54
    >>> part_2(*_parse("880086C3E88112"))
    7
    >>> part_2(*_parse("CE00C43D881120"))
    9
    >>> part_2(*_parse("D8005AC2A8F0"))
    1
    >>> part_2(*_parse("F600BC2D8F"))
    0
    >>> part_2(*_parse("9C005AC2F8F0"))
    0
    >>> part_2(*_parse("9C0141080250320F1802104A08"))
    1

    """
    return packet.value
