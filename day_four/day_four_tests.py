import unittest
import re


class PartTwoValidator(object):
    @classmethod
    def validate(class_, s):
        try:
            validations = [
                byr.parse(s['byr']),
                iyr.parse(s['iyr']),
                ecl.parse(s['ecl']),
                pid.parse(s['pid']),
                hcl.parse(s['hcl']),
                hgt.parse(s['hgt']),
                eyr.parse(s['eyr'])
            ]
        except KeyError:
            return False
        else:
            return all(validations)


class ecl(object):
    def __init__(self, s):
        self.value = s

    @classmethod
    def parse(class_, s):

        if s in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
            return ecl(s)
        else:
            return None

    def __str__(self):
        return f"ecl: {self.value}"

    def __repr__(self):
        return f"ecl: {self.value}"


class pid(object):
    def __init__(self, s):
        self.value = s

    @classmethod
    def parse(class_, s):
        pattern = "^[0-9]{9}$"
        regex = re.compile(pattern)
        match = regex.search(s)
        if match:
            return pid(s)
        else:
            return None

    def __str__(self):
        return f"pid: {self.value}"

    def __repr__(self):
        return f"pid: {self.value}"


class hcl(object):
    def __init__(self, s):
        self.value = s

    @classmethod
    def parse(class_, s):
        pattern = "^#[0-9a-f]{6}$"
        regex = re.compile(pattern)
        match = regex.search(s)
        if match:
            return hcl(s)
        else:
            return None

    def __str__(self):
        return f"hcl: {self.value}"

    def __repr__(self):
        return f"hcl: {self.value}"


class hgt(object):
    def __init__(self, s):
        self.value = s

    @classmethod
    def parse_in_range(class_, s, lower, upper):
        n = int(s[:-2])
        if lower <= n and n <= upper:
            return hgt(n)
        else:
            return None

    @classmethod
    def parse(class_, s):
        if s.endswith("cm"):
            return class_.parse_in_range(s, 150, 193)
        elif s.endswith("in"):
            return class_.parse_in_range(s, 59, 76)
        else:
            return None

    def __str__(self):
        return f"hgt: {self.value}"

    def __repr__(self):
        return f"hgt: {self.value}"


class eyr(object):
    def __init__(self, s):
        self.value = s

    @classmethod
    def parse(class_, s):
        if len(s) == 4:
            n = int(s)
            if 2020 <= n and n <= 2030:
                return eyr(n)
            else:
                return None
        else:
            return None

    def __str__(self):
        return f"eyr: {self.value}"

    def __repr__(self):
        return f"eyr: {self.value}"


class iyr(object):
    def __init__(self, s):
        self.value = s

    @classmethod
    def parse(class_, s):
        if len(s) == 4:
            n = int(s)
            if 2010 <= n and n <= 2020:
                return iyr(n)
            else:
                return None
        else:
            return None

    def __str__(self):
        return f"iyr: {self.value}"

    def __repr__(self):
        return f"iyr: {self.value}"


class byr(object):
    def __init__(self, s):
        self.value = s

    @classmethod
    def parse(class_, s):
        if len(s) == 4:
            n = int(s)
            if 1920 <= n and n <= 2002:
                return byr(n)
            else:
                return None
        else:
            return None

    def __str__(self):
        return f"byr: {self.value}"

    def __repr__(self):
        return f"byr: {self.value}"


def split_input(input):
    unparse_passports = []
    current = []
    for line in input.splitlines():
        if len(line) > 0:
            current.append(line.strip())
        else:
            if len(current) == 0:
                pass
            else:
                unparse_passports.append(current)
                current = []

    if len(current) > 0:
        unparse_passports.append(current)

    return [" ".join(x).strip() for x in unparse_passports]


def parse_passport_string(s):
    return dict(x.split(":") for x in s.split(" "))


def parse(input):
    unparsed_passports = split_input(input)
    parsed_passports = [parse_passport_string(s) for s in unparsed_passports]
    return parsed_passports


def is_valid_passport(p):
    return all([
        "byr" in p,
        "iyr" in p,
        "eyr" in p,
        "hgt" in p,
        "hcl" in p,
        "ecl" in p,
        "pid" in p
    ])


class DayThreeTests(unittest.TestCase):

    example_input = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
    """

    def test_read_passwords_from_example(self):
        passports = parse(self.example_input)
        valid_passports = [p for p in passports if is_valid_passport(p)]
        # print(valid_passports)
        self.assertEqual(len(valid_passports), 2)

    def test_read_passwords_from_puzzle_input(self):
        with open('puzzle_input.txt') as content:
            ss = content.read()
        passports = parse(ss)
        valid_passports = [p for p in passports if is_valid_passport(p)]
        # print(valid_passports)
        self.assertEqual(len(valid_passports), 228)

    def test_byr_validation(self):
        self.assertIsNone(byr.parse('1919'))
        [self.assertIsNotNone(byr.parse(str(n))) for n in range(1920, 2003)]
        self.assertIsNone(byr.parse('2003'))

    def test_iyr_validation(self):
        self.assertIsNone(iyr.parse('2009'))
        [self.assertIsNotNone(iyr.parse(str(n))) for n in range(2010, 2021)]
        self.assertIsNone(iyr.parse('2021'))

    def test_eyr_validation(self):
        self.assertIsNone(eyr.parse('2019'))
        [self.assertIsNotNone(eyr.parse(str(n))) for n in range(2020, 2031)]
        self.assertIsNone(eyr.parse('2031'))

    def test_hgt_validation_in_centimetres(self):
        self.assertIsNone(hgt.parse('149cm'))
        [self.assertIsNotNone(hgt.parse(str(n)+"cm")) for n in range(150, 194)]
        self.assertIsNone(hgt.parse('194cm'))

    def test_hgt_validation_in_inches(self):
        self.assertIsNone(hgt.parse('58in'))
        [self.assertIsNotNone(hgt.parse(str(n)+"in")) for n in range(59, 77)]
        self.assertIsNone(hgt.parse('77in'))

    def test_hcl_validation(self):
        self.assertIsNone(hcl.parse('not starting with hash'))
        self.assertIsNone(hcl.parse('#short'))
        self.assertIsNone(hcl.parse('#gggggg'))
        self.assertIsNotNone(hcl.parse('#012fff'))

    def test_ecl_validation(self):
        self.assertIsNone(ecl.parse('aaa'))
        self.assertIsNone(ecl.parse('zzz'))
        [self.assertIsNotNone(ecl.parse(s)
                              for s
                              in ["amb",
                                  "blu",
                                  "brn",
                                  "gry",
                                  "grn",
                                  "hzl",
                                  "oth"])]

    def test_pid_validation(self):
        self.assertIsNone(pid.parse('1234567890'))
        self.assertIsNone(pid.parse('12345678'))
        self.assertIsNone(pid.parse('12345678a'))
        self.assertIsNotNone(pid.parse('123456789'))

    def test_part_two_invalid(self):
        ss = """
        eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""
        passports = parse(ss)
        valid_passports = [
            p for p in passports if PartTwoValidator.validate(p)]
        self.assertEqual(len(valid_passports), 0)

    def test_read_passwords_from_puzzle_input_part_two(self):
        with open('puzzle_input.txt') as content:
            ss = content.read()
        passports = parse(ss)
        valid_passports = [
            p for p in passports if PartTwoValidator.validate(p)]
        # print(valid_passports)
        self.assertEqual(len(valid_passports), 175)


if __name__ == '__main__':
    unittest.main()
