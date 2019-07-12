import abc
import logging
from time import time

from combcov.exact_cover import ExactCover

logger = logging.getLogger("CombCov")
logging.basicConfig(
    format='[%(levelname)-4s] (%(name)s) %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class CombCov():

    def __init__(self, root_object, max_elmnt_size):
        self.root_object = root_object
        self.max_elmnt_size = max_elmnt_size
        self._enumerate_all_elmnts_up_to_max_size()
        self._create_binary_strings_from_rules()
        self._solve()

    def _enumerate_all_elmnts_up_to_max_size(self):
        logger.info("Enumerating all elements of size up to {}...".format(
            self.max_elmnt_size))
        time_start = time()

        elmnts = []
        self.enumeration = [None] * (self.max_elmnt_size + 1)
        for n in range(self.max_elmnt_size + 1):
            elmnts_of_length_n = self.root_object.get_elmnts(of_size=n)
            self.enumeration[n] = len(elmnts_of_length_n)
            elmnts.extend(elmnts_of_length_n)

        self.elmnts_dict = {
            string: nr for nr, string in enumerate(elmnts, start=0)
        }

        time_end = time()
        elapsed_time = time_end - time_start

        logger.info("...DONE enumerating elements! "
                    "(Running time: {:.2f} sec)".format(elapsed_time))
        logger.info("Total of {} elements.".format(len(elmnts)))
        logger.info("Enumeration: {}".format(self.enumeration))

    def _create_binary_strings_from_rules(self):
        logger.info("Creating binary strings and rules...")
        time_start = time()

        string_to_cover = 2 ** len(self.elmnts_dict) - 1
        logger.info("Bitstring to cover: {} ".format(string_to_cover))

        self.rules = []
        self.bitstrings = []
        self.bitstring_to_rules_dict = {}
        self.rules_to_bitstring_dict = {}

        for rule in self.root_object.get_subrules():
            if rule in self.rules:
                rule_is_good = False
            else:
                rule_is_good = True
                binary_string = 0

            for elmnt_size in range(self.max_elmnt_size + 1):
                if not rule_is_good:
                    break

                seen_elmnts = set()
                for elmnt in rule.get_elmnts(of_size=elmnt_size):
                    if elmnt not in self.elmnts_dict or elmnt in seen_elmnts:
                        rule_is_good = False
                        break
                    else:
                        seen_elmnts.add(elmnt)
                        binary_string += 2 ** (self.elmnts_dict[elmnt])

                # Throwing out single-rule covers
                if binary_string == string_to_cover:
                    rule_is_good = False

            if rule_is_good:
                self.rules.append(rule)
                self.rules_to_bitstring_dict[rule] = binary_string

                # ToDo: Use defaultdict for more readable syntax
                if binary_string not in self.bitstring_to_rules_dict:
                    self.bitstrings.append(binary_string)
                    self.bitstring_to_rules_dict[binary_string] = [rule]
                else:
                    self.bitstring_to_rules_dict[binary_string].append(rule)

        time_end = time()
        elapsed_time = time_end - time_start

        logger.info("...DONE creating binary strings and rules! "
                    "(Running time: {:.2f} sec)".format(elapsed_time))
        logger.info("Total of {} rules valid rules.".format(len(self.rules)))
        logger.info("There of {} rules creating distinct binary "
                    "strings".format(len(self.bitstring_to_rules_dict)))

    def _solve(self):
        logger.info("Searching for a cover for {}...".format(self.root_object))
        time_start = time()

        self.solution = []
        self.ec = ExactCover(self.bitstrings, len(self.elmnts_dict))
        self.solution = [
            self.bitstring_to_rules_dict[self.bitstrings[bitstring_index]][0]
            for bitstring_index in self.ec.exact_cover()]

        time_end = time()
        elapsed_time = time_end - time_start

        logger.info("...DONE searching for a cover! "
                    "(Running time: {:.2f} sec)".format(elapsed_time))

    def print_outcome(self):
        if self.solution:
            print("Solution found!")
            for i, rule in enumerate(self.solution, start=1):
                print(" - Rule #{}: {} with bitstring {}".format(
                    i, rule, self.rules_to_bitstring_dict[rule]))
        else:
            print("No solution found.")

    def __iter__(self):
        yield from self.solution


class Rule(abc.ABC):
    @abc.abstractmethod
    def get_elmnts(self, of_size):
        raise NotImplementedError

    @abc.abstractmethod
    def get_subrules(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _key(self):
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        return isinstance(self, type(other)) and self._key() == other._key()
