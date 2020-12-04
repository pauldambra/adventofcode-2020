import re


class PartTwoValidator(object):
    @classmethod
    def validate(s):
        return byr(s) and iyr(s) and ecl(s) and pid(s) and hcl(s) and hgt(s) and eyr(s)


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


class pid(object):
    def __init__(self, s):
        self.value = s

    @classmethod
    def parse(class_, s):
        pattern = "^[0-9]{9}$"
        regex = re.compile(pattern)
        match = regex.search(s)
        print([s, match])
        if match:
            return pid(s)
        else:
            return None

    def __str__(self):
        return f"pid: {self.value}"


class hcl(object):
    def __init__(self, s):
        self.value = s

    @classmethod
    def parse(class_, s):
        pattern = "^#[0-9a-f]{6}$"
        regex = re.compile(pattern)
        match = regex.search(s)
        print([s, match])
        if match:
            return hcl(s)
        else:
            return None

    def __str__(self):
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
