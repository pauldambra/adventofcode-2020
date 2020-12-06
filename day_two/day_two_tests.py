from files.reader import get_puzzle_input_path
import unittest
import re
import os


def ruleFrom(s):
    x = s.split(":")[0].split(" ")
    letter = x[1]
    counts = x[0].split('-')
    pattern = (
        f"^(?:[^{letter}]*[{letter}]){{{counts[0]},{counts[1]}}}"
        f"[^{letter}]*$"
    )
    try:
        rule = re.compile(pattern)
    except Exception:
        print(f"could not compile: {pattern} generated from rule: {x}")
        raise
    else:
        # print(f"compiled {pattern} from {x}")
        return rule


def partTwoRulesFrom(s):
    x = s.split(":")[0].split(" ")
    letter = x[1]
    counts = [int(z) for z in x[0].split('-')]
    patterns = [f"^.{{{counts[0]-1}}}{letter}",
                f"^.{{{counts[1]-1}}}{letter}"]
    try:
        rules = [re.compile(p) for p in patterns]
    except Exception:
        print(f"could not compile: {patterns} generated from rule: {x}")
        raise
    else:
        # print(f"compiled {pattern} from {x}")
        return rules


def passwordFrom(s):
    p = s.split(":")
    return p[1].strip()


def passwordIsValid(password, rule):
    result = rule.search(password)
    return result


def passwordIsValidPartTwo(password, rules):
    results = [r.search(password) for r in rules]
    return len(results) == 2 and sum(x is not None for x in results) == 1


def checkPasswordValidity(examples):
    return [x for x
            in examples
            if passwordIsValid(passwordFrom(x), ruleFrom(x))]


def checkPasswordValidityPartTwo(examples):
    return [x for x
            in examples
            if passwordIsValidPartTwo(passwordFrom(x), partTwoRulesFrom(x))]


def read_from_file(f):
    with open(f) as content:
        return [line.rstrip() for line in content]


class DayTwoTests(unittest.TestCase):

    def test_valid_passwords_example(self):
        policyExamples = ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"]
        validPasswords = checkPasswordValidity(policyExamples)
        self.assertEqual(len(validPasswords), 2)

    def test_valid_passwords_one_failing(self):
        policyExamples = ["2-2 a: abcde"]
        validPasswords = checkPasswordValidity(policyExamples)
        self.assertEqual(len(validPasswords), 0)

    def test_non_continuous_letters_do_count(self):
        x = "11-14 z: zzzzzzvzzxbzzzh"
        password = passwordFrom(x)
        rule = ruleFrom(x)
        self.assertTrue(passwordIsValid(password, rule))

    def test_valid_passwords_puzzle_input(self):
        policyExamples = read_from_file(
            get_puzzle_input_path(os.path.dirname(__file__)))
        validPasswords = checkPasswordValidity(policyExamples)
        self.assertEqual(len(validPasswords), 536)

    def test_part_two_rule_example_one(self):
        example = "1-3 a: abcde"
        rule = partTwoRulesFrom(example)
        self.assertEqual(rule[0], re.compile("^.{0}a"))
        self.assertEqual(rule[1], re.compile("^.{2}a"))

        result = passwordIsValidPartTwo(
            passwordFrom(example),
            partTwoRulesFrom(example))
        self.assertTrue(result)

    def test_part_two_rule_example_two(self):
        example = "1-3 b: cdefg"
        rule = partTwoRulesFrom(example)
        self.assertEqual(rule[0], re.compile("^.{0}b"))
        self.assertEqual(rule[1], re.compile("^.{2}b"))

        result = passwordIsValidPartTwo(
            passwordFrom(example),
            partTwoRulesFrom(example))
        self.assertFalse(result)

    def test_part_two_rule_example_three(self):
        example = "2-9 c: ccccccccc"
        rule = partTwoRulesFrom(example)
        self.assertEqual(rule[0], re.compile("^.{1}c"))
        self.assertEqual(rule[1], re.compile("^.{8}c"))

        result = passwordIsValidPartTwo(
            passwordFrom(example),
            partTwoRulesFrom(example))
        self.assertFalse(result)

    def test_valid_passwords_puzzle_input_part_two(self):
        policyExamples = read_from_file(
            get_puzzle_input_path(os.path.dirname(__file__)))
        validPasswords = checkPasswordValidityPartTwo(policyExamples)
        self.assertLess(len(validPasswords), 786)
        self.assertEqual(len(validPasswords), 558)


if __name__ == '__main__':
    unittest.main()
