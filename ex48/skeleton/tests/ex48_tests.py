from nose.tools import *
from ex48.lexicon import Lexicon


def text_directions():
    assert_equal(Lexicon.scan("north"), [('direction', 'north')])
    result = Lexicon.scan("north South EAST west dOwn up left right back")
    assert_equal(result, [('direction', 'north'),
                          ('direction', 'South'),
                          ('direction', 'EAST'),
                          ('direction', 'west'),
                          ('direction', 'dOwn'),
                          ('direction', 'up'),
                          ('direction', 'left'),
                          ('direction', 'right'),
                          ('direction', 'back')
                          ])


def test_verbs():
    assert_equal(Lexicon.scan('go'), [('verb', 'go')])
    result = Lexicon.scan("go KILL eat stop")
    assert_equal(result, [('verb', 'go'),
                          ('verb', 'KILL'),
                          ('verb', 'eat'),
                          ('verb', 'stop')
                          ])


def test_stops():
    assert_equal(Lexicon.scan("the"), [('stop', 'the')])
    result = Lexicon.scan("the in of FROM at it")
    assert_equal(result, [('stop', 'the'),
                          ('stop', 'in'),
                          ('stop', 'of'),
                          ('stop', 'FROM'),
                          ('stop', 'at'),
                          ('stop', 'it'),
                          ])


def test_numbers():
    assert_equal(Lexicon.scan("1234"), [('number', '1234')])
    result = Lexicon.scan("3 91234 23098 8128 0")
    assert_equal(result, [('number', '3'),
                          ('number', '91234'),
                          ('number', '23098'),
                          ('number', '8128'),
                          ('number', '0'),
                          ])


def test_errors():
    assert_equal(Lexicon.scan("ASDFADFASDF"), [('error', 'ASDFADFASDF')])
    result = Lexicon.scan("Bear IAS princess")
    assert_equal(result, [('noun', 'Bear'),
                          ('error', 'IAS'),
                          ('noun', 'princess')
                          ])
