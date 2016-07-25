import preamble

from metaparse import LALR


def fappend(l, x):
    l.append(x)
    return l

class Gcourses(metaclass=LALR.meta):

    """
    Grammar to assign multiple numbers to precedend course name.
    Examples:

"CS 2110"                        => ("CS", 2110) # 0

"CS 2110 and INFO 3300"          => [("CS", 2110), ("INFO", 3300)] # 1
"CS 2110, INFO 3300"             => [("CS", 2110), ("INFO", 3300)] # 1
"CS 2110, 3300, 3140"            => [("CS", 2110), ("CS", 3300), ("CS", 3140)] # 1

"CS 2110 or INFO 3300"           => [[("CS", 2110)], [("INFO", 3300)]] # 2

"MATH 2210, 2230, 2310, or 2940" => [[("MATH", 2210), ("MATH", 2230), ("MATH", 2310)], [("MATH", 2940)]] # 3

    """

    IGNORED = r'[ \t]+|(,)|(and)'
    NAME    = r'[A-Z]+'
    NUMBER  = r'\d{4}'
    OR      = r'or'


    # info -> headed
    def info(headed):                return headed

    # info -> conj
    def info(conj):                  return conj

    # info -> disj
    def info(disj):                  return disj

    # headed -> NAME nums
    def headed(NAME, nums):          return [(NAME, x) for x in nums]

    # nums -> nums NUMBER
    def nums(nums, NUMBER):          return fappend(nums , NUMBER)
    # def nums(nums, NUMBER):          return nums + [NUMBER]

    # nums -> NUMBER
    def nums(NUMBER):                return [NUMBER]

    # conj -> headed headed
    def conj(headed_1, headed_2):      return headed_1 + headed_2

    # disj -> headed OR headed
    def disj(headed_1, OR, headed_2):  return [headed_1, headed_2]

    # disj -> headed OR nums
    def disj(headed, OR, nums):     return [headed, [(headed[0][0], n) for n in nums]]

import pprint as pp

gcrs = Gcourses

assert gcrs.interpret('CS 2110') == \
    [('CS', '2110')]
assert gcrs.interpret('CS 2110 and INFO 3300') == \
    [('CS', '2110'), ('INFO', '3300')]
assert gcrs.interpret('CS 2110, INFO 3300') == \
    [('CS', '2110'), ('INFO', '3300')]
assert gcrs.interpret('CS 2110, 3300, 3140') == \
    [('CS', '2110'), ('CS', '3300'), ('CS', '3140')]
assert gcrs.interpret('CS 2110 or INFO 3300') == \
    [[('CS', '2110')], [('INFO', '3300')]]

# Compare forms with same semantics...
inp = "MATH 2210, 2230, 2310 or 2940"
s1 =  Gcourses.parse(inp)
v1 =  Gcourses.interpret(inp)

inp = "MATH 2210, 2230, 2310, or 2940"
s2 = Gcourses.parse(inp)
v2 =  Gcourses.interpret(inp)

assert s1 == s2
assert v1 == v2

