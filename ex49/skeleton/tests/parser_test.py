from nose.tools import *
from ex49.parser import *
from lexicon import Lexicon
from copy import deepcopy


# construct a test set that consists of several test lists
global_test_lists = [ Lexicon.scan('south'), Lexicon.scan('door'), Lexicon.scan('go'), Lexicon.scan('to'),
                      Lexicon.scan('234'), Lexicon.scan('error123'), Lexicon.scan('the east door'), Lexicon.scan('go to east'),
                      Lexicon.scan('bear go to the door'), Lexicon.scan('the princess kill 10 bear') 
                    ]

# the type of the the first tuple for each test list
test_types = ['direction', 'noun', 'verb', 'stop', 'number', 'error',
               'stop', 'verb', 'noun', 'stop', None]

list_len = len(global_test_lists)


def test_peek():
    ''' test peek function '''
    test_lists = deepcopy(global_test_lists)
    for i in range(list_len):
        test_list = test_lists[i]
        expected_word = test_types[i]
        assert_equal(peek(test_list), expected_word)


def test_match():
    ''' test match function '''
    test_lists = deepcopy(global_test_lists)
    for i in range(list_len):
        test_list = test_lists[i]
        test_type = test_types[i]
        if len(test_list) > 0:
            expected_tuple = test_list[0]
        else:
            expected_tuple = None
        assert_equal(match(test_list, test_type), expected_tuple)


def test_skip():
    ''' test skip function '''
    test_lists = deepcopy(global_test_lists)
    expected_lists1 = [Lexicon.scan('south'), Lexicon.scan('door'), Lexicon.scan('go'), [], Lexicon.scan('234'), Lexicon.scan('error123'),
                       Lexicon.scan('east door'), Lexicon.scan('go to east'), Lexicon.scan('bear go to the door'),
                       Lexicon.scan('princess kill 10 bear'), []]

    for i in range(list_len):
        test_list = test_lists[i]
        expected_list = expected_lists1[i]
        skip(test_list, 'stop')
        assert_equal(test_list, expected_list)

    test_list2 = [('error', 'error123')]
    expected_list2 = []
    skip(test_list2, 'error')
    assert_equal(test_list2, expected_list2)


def test_parse_verb():
    ''' test parse_verb function '''
    parser = Parser()
    # test good situations
    test_lists_good =  [Lexicon.scan('go'), Lexicon.scan('go to east'), Lexicon.scan('to error123 eat')] 
    expected_lists = [Lexicon.scan('go'), Lexicon.scan('go'), Lexicon.scan('eat')]

    for i in range(len(test_lists_good)):
        test_list = test_lists_good[i]
        expected_list = expected_lists[i]
        assert_equal(parser.parse_verb(test_list), *expected_list)

    # test bad situations
    test_lists_bad = [Lexicon.scan('south'), Lexicon.scan('door'), Lexicon.scan('234'), Lexicon.scan('east door'),
                       Lexicon.scan('error123'), Lexicon.scan('to'),
                      Lexicon.scan('bear go to the door'), Lexicon.scan('the princess kill 10 bear'), []]
    for i in range(len(test_lists_bad)):
        test_list = test_lists_bad[i]
        assert_raises(ParserError, parser.parse_verb, test_list)


def test_parse_object():
    ''' test parse_object function '''
    parser = Parser()
    # test good situations
    test_lists_good =  [Lexicon.scan('south'), Lexicon.scan('door'), Lexicon.scan('the bear'), Lexicon.scan('east door'),
                        Lexicon.scan('bear go to the door'), Lexicon.scan('the princess kill 10 bear')]

    expected_lists = [Lexicon.scan('south'), Lexicon.scan('door'), Lexicon.scan('bear'),
                      Lexicon.scan('east'), Lexicon.scan('bear'), Lexicon.scan('princess')]

    for i in range(len(test_lists_good)):
        test_list = test_lists_good[i]
        expected_list = expected_lists[i]
        assert_equal(parser.parse_object(test_list), *expected_list)

    # test bad situations
    test_lists_bad = [Lexicon.scan('go'), Lexicon.scan('to'), Lexicon.scan('234'), Lexicon.scan('error123'), Lexicon.scan('go to east'), []]
    for i in range(len(test_lists_bad)):
        test_list = test_lists_bad[i]
        assert_raises(ParserError, parser.parse_object, test_list)


def test_class_sentence():
    # test good situations
    test_lists_good =  [Lexicon.scan('bear go east'), Lexicon.scan('princess kill bear'), Lexicon.scan(
                        'bear kill bear')]
    expected_nums = [1, 1, 10]
    expected_objects = ['east', 'bear', 'bear']

    for i in range(len(test_lists_good)):
        test_list = test_lists_good[i]
        test_num = expected_nums[i]
        test_object = expected_objects[i]

        sentence = Sentence(*test_list)
        assert_equal(sentence.subject, test_list[0][1])
        assert_equal(sentence.verb, test_list[1][1])
        assert_equal(sentence.object, test_object)

    # test bad situations, for more restrict checking
    test_lists_bad =  [Lexicon.scan('south'), Lexicon.scan('bear'), Lexicon.scan('go'), Lexicon.scan('to'),
                       Lexicon.scan('the'), Lexicon.scan('door'), Lexicon.scan('bear go to the door'),
                       Lexicon.scan('the princess kill 10 bear'), []] 

    for i in range(len(test_lists_good)):
        test_list = test_lists_bad[i]
        assert_raises(TypeError, Sentence, *test_list)


def test_parse_subject():
    ''' test parse_subject function '''
    parser = Parser()

    test_lists =  [Lexicon.scan('error123 eat princess'), Lexicon.scan('go to east'),
                   Lexicon.scan('go error123 to the cabinet door'), Lexicon.scan('kill bear')]

    test_subjects = [Lexicon.scan('bear'), Lexicon.scan('princess'), Lexicon.scan('cabinet'), Lexicon.scan('princess')]
    expected_verbs = ['eat', 'go', 'go', 'kill']
    expected_objects = ['princess', 'east', 'cabinet', 'bear']
    expected_nums = [1, 1, 1, 10]

    for i in range(len(test_lists)):
        test_list = test_lists[i]
        test_subject = test_subjects[i]
        expected_verb = expected_verbs[i]
        expected_object = expected_objects[i]
        sentence = parser.parse_subject(test_list, test_subject[0])
        assert_equal(sentence.subject, test_subject[0][1])
        assert_equal(sentence.verb, expected_verb)
        assert_equal(sentence.object, expected_object)


def test_parse_sentence():
    ''' test parse_sentence function '''
    parser = Parser()
    # test good situations
    test_lists1 =  [Lexicon.scan('bear go to the door'),
                    Lexicon.scan('the princess kill bear'),
                    Lexicon.scan('kill the bear')]

    expected_subjects = ['bear', 'princess', 'player']
    expected_verbs = ['go', 'kill', 'kill']
    expected_objects = ['door', 'bear', 'bear']
    expected_nums = [1, 10, 1]
        
    for i in range(len(test_lists1)):
        test_list = test_lists1[i]
        sentence = parser.parse_sentence(test_list)
        expected_subject = expected_subjects[i]
        expected_verb = expected_verbs[i]
        expected_object = expected_objects[i]
        assert_equal(sentence.subject, expected_subject)
        assert_equal(sentence.verb, expected_verb)
        assert_equal(sentence.object, expected_object)

    # test bad situations
    test_lists2 =  [Lexicon.scan('234')]
    for i in range(len(test_lists2)):
        test_list = test_lists2[i]
        assert_raises(ParserError, parser.parse_object, test_list)
