from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    # def test_example_unit_test(self):
    #     dummy_keyword_dict = {
    #         'cat': ['title1', 'title2', 'title3'],
    #         'dog': ['title3', 'title4']
    #     }
    #     expected_search_results = ['title3', 'title4']
    #     self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)

    def test_keyword_to_titles_unit_test(self):
        metadata = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian']], ['Games', 'Jack Johnson', 1181623340, 21023, ['canadian']], ['Awesome', 'Jack Johnson', 1181623340, 21023, ['yes']]]

        expected_multiple_articles = {
            'canadian': ['List of Canadian musicians', 'Games'],
            'yes': ['Awesome']
        }
        self.assertEqual(keyword_to_titles(metadata), expected_multiple_articles)

        metadata = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian', 'music']], ['Games', 'Jack Johnson', 1181623340, 21023, ['canadian', 'games', 'fun']], ['Awesome', 'Jack Johnson', 1181623340, 21023, ['yes', 'fun']]]

        expected_multiple_keyowrds = {
            'canadian': ['List of Canadian musicians', 'Games'],
            'music': ['List of Canadian musicians'],
            'games': ['Games'],
            'fun': ['Games', 'Awesome'],
            'yes': ['Awesome']
        }
        self.assertEqual(keyword_to_titles(metadata), expected_multiple_keyowrds)

        metadata = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian', 'music']], ['Games', 'Jack Johnson', 1181623340, 21023, ['canadian', 'games', 'fun']], ['Awesome', 'Jack Johnson', 1181623340, 21023, ['yes', 'fun', 'Yes', 'yes!']]]

        expected_capital_and_lower = {
        'canadian': ['List of Canadian musicians', 'Games'],
        'music': ['List of Canadian musicians'],
        'games': ['Games'],
        'fun': ['Games', 'Awesome'],
        'yes': ['Awesome'],
        'Yes': ['Awesome'],
        'yes!': ['Awesome']
        }

        self.assertEqual(keyword_to_titles(metadata), expected_capital_and_lower)

        self.assertEqual(keyword_to_titles([]), {})

    def test_title_to_info(self):
        metadata = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian']], ['Games', 'Madi J', 51, 800, ['canadian']], ['Awesome', 'Wonder Land', 30, 0, ['yes']]]

        expected_regular = {
        'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023},
        'Games': {'author': 'Madi J', 'timestamp': 51, 'length': 800},
        'Awesome': {'author': 'Wonder Land', 'timestamp': 30, 'length': 0}, 
        }

        self.assertEqual(title_to_info(metadata), expected_regular)

        metadata = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian']], ['GAMES! 123!', 'Mad1 J@nes', 51, 800, ['canadian']], ['Awesom3', 'W0nder Land', 30, 0, ['yes']]]

        expected_special_characters = {
        'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023},
        'GAMES! 123!': {'author': 'Mad1 J@nes', 'timestamp': 51, 'length': 800},
        'Awesom3': {'author': 'W0nder Land', 'timestamp': 30, 'length': 0}, 
        }

        self.assertEqual(title_to_info(metadata), expected_special_characters)

        metadata = [['List of Canadian musicians', 'Jack Johnson', 1181623340, 21023, ['canadian']], ['GAMES! 123!', 'Mad1 J@nes', 51, 800, ['canadian']], ['GAMES! 123!', 'Mad1 J@nes', 51, 800, ['canadian']], ['Awesom3', 'W0nder Land', 30, 0, ['yes']]]

        expected_duplicate = {
        'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023},
        'GAMES! 123!': {'author': 'Mad1 J@nes', 'timestamp': 51, 'length': 800},
        'Awesom3': {'author': 'W0nder Land', 'timestamp': 30, 'length': 0}, 
        }

        self.assertEqual(title_to_info(metadata), expected_duplicate)

        self.assertEqual(title_to_info([]), {})

    def test_search(self):
        keyword_to_titles = {
            'canadian': ['List of Canadian musicians', 'Games'],
            'yes': ['Awesome']
        }

        expected_regular = ['List of Canadian musicians', 'Games']

        self.assertEqual(search('canadian', keyword_to_titles), expected_regular)

        keyword_to_titles = {
            'canadian': ['List of Canadian musicians', 'Games'],
            'yes': ['Awesome'],
            'Yes': ['Ok! Lets go!', 'Today'],
            'Yes!': ['Summer Time'],
        }

        self.assertEqual(search('Yes', keyword_to_titles), ['Ok! Lets go!', 'Today'])

        self.assertEqual(search('Yes', []), [])

        self.assertEqual(search('', keyword_to_titles), [])

    def test_article_length(self):
        title_to_info = {
        'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023},
        'Games': {'author': 'Madi J', 'timestamp': 51, 'length': 800},
        'Awesome': {'author': 'Wonder Land', 'timestamp': 30, 'length': 0}, 
        }

        self.assertEqual(article_length(5, [], title_to_info), [])

        self.assertEqual(article_length(5, ['List of Canadian musicians', 'Games'], {}), [])

        self.assertEqual(article_length(1181623340, ['List of Canadian musicians', 'Games'], title_to_info), ['List of Canadian musicians', 'Games'])

        self.assertEqual(article_length(800, ['List of Canadian musicians', 'Games'], title_to_info), ['Games'])

        self.assertEqual(article_length(1181623340, ['List of Canadian musicians', 'Games', ' '], title_to_info), ['List of Canadian musicians', 'Games'])

        self.assertEqual(article_length(0, ['List of Canadian musicians', 'Awesome', 'Games'], title_to_info), ['Awesome'])

        self.assertEqual(article_length(0, ['List of Canadian musicians', 'Games'], title_to_info), [])
    
    def test_key_by_author(self):
        title_to_info = {
        'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023},
        'Games': {'author': 'Madi J', 'timestamp': 51, 'length': 800},
        'Awesome': {'author': 'Wonder Land', 'timestamp': 30, 'length': 0}, 
        }

        expected_individual = {
            'Jack Johnson': ['List of Canadian musicians'],
            'Madi J': ['Games'],
            'Wonder Land': ['Awesome']
        }

        self.assertEqual(key_by_author(['List of Canadian musicians', 'Awesome', 'Games'], title_to_info), expected_individual)

        title_to_info = {
        'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023},
        'Games': {'author': 'Madi J', 'timestamp': 51, 'length': 800},
        'Awesome': {'author': 'Jack Johnson', 'timestamp': 30, 'length': 0},
        'Great': {'author': 'Madi J', 'timestamp': 30, 'length': 0},
        'Triple': {'author': 'Madi J', 'timestamp': 30, 'length': 0}
        }

        expected_multiple_articles = {
            'Jack Johnson': ['List of Canadian musicians', 'Awesome'],
            'Madi J': ['Games', 'Triple'],
        }

        self.assertEqual(key_by_author(['List of Canadian musicians', 'Awesome', 'Games', "Triple"], title_to_info), expected_multiple_articles)

        self.assertEqual(key_by_author([], title_to_info), {})

        self.assertEqual(key_by_author(['List of Canadian musicians', 'Awesome', 'Games', "Triple"], {}), {})
    
    def test_filter_to_author(self):
        title_to_info = {
        'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023},
        'Games': {'author': 'Madi J', 'timestamp': 51, 'length': 800},
        'Awesome': {'author': 'Jack Johnson', 'timestamp': 30, 'length': 0},
        'Great': {'author': 'Madi J', 'timestamp': 30, 'length': 0},
        'Triple': {'author': 'Madi J', 'timestamp': 30, 'length': 0}
        }

        self.assertEqual(filter_to_author('Madi J', ['Games', 'Awesome', 'Triple'], title_to_info), ['Games', 'Triple'])

        self.assertEqual(filter_to_author('Jake', ['Games', 'Awesome', 'Triple'], title_to_info), [])

        self.assertEqual(filter_to_author('Madi J', [], title_to_info), [])

        self.assertEqual(filter_to_author('', ['Games', 'Awesome', 'Triple'], title_to_info), [])

        self.assertEqual(filter_to_author('Madi J', ['Games', 'Awesome', 'Triple'], {}), [])

    def test_filter_out(self):
        keyword_to_titles = {
            'canadian': ['List of Canadian musicians', 'Games'],
            'music': ['List of Canadian musicians'],
            'games': ['Games'],
            'fun': ['Games', 'Awesome'],
            'yes': ['Awesome']
        }

        self.assertEqual(filter_out('canadian', ['List of Canadian musicians', 'Games', 'Awesome'], keyword_to_titles), ['Awesome'])
        
        self.assertEqual(filter_out('time', ['List of Canadian musicians', 'Games', 'Awesome'], keyword_to_titles), ['List of Canadian musicians', 'Games', 'Awesome'])

        self.assertEqual(filter_out('fun', ['List of Canadian musicians', 'Games', 'Awesome'], keyword_to_titles), ['List of Canadian musicians'])

        self.assertEqual(filter_out('', ['List of Canadian musicians', 'Games', 'Awesome'], keyword_to_titles), ['List of Canadian musicians', 'Games', 'Awesome'])

        self.assertEqual(filter_out('fun', ['Try', 'Together'], keyword_to_titles), ['Try', 'Together'])
    
    def test_articles_from_year(self):
        title_to_info = {
        'List of Canadian musicians': {'author': 'Jack Johnson', 'timestamp': 1181623340, 'length': 21023},
        'Games': {'author': 'Madi J', 'timestamp': 1191623340, 'length': 800},
        'Awesome': {'author': 'Wonder Land', 'timestamp': 1201623340, 'length': 0}, 
        }

        self.assertEqual(articles_from_year(2007, ['List of Canadian musicians', 'Games', 'Awesome'], title_to_info), ['List of Canadian musicians', 'Games'])

        self.assertEqual(articles_from_year(2009, ['List of Canadian musicians', 'Games', 'Awesome'], title_to_info), [])

        self.assertEqual(articles_from_year(2007, ['Awesome'], title_to_info), [])

        self.assertEqual(articles_from_year(2008, ['Awesome'], {}), [])

        self.assertEqual(articles_from_year(2007, [], title_to_info), [])

        




    #####################
    # INTEGRATION TESTS #
    #####################

    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_1_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 1
        advanced_response = 2000

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team']\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_2_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 2
        

        output = get_print(input_mock, [keyword, advanced_option])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + "\nHere are your articles: {'jack johnson': ['Spain national beach soccer team'], 'Burna Boy': ['Will Johnson (soccer)'], 'Mack Johnson': ['Steven Cohen (soccer)']}\n"

        self.assertEqual(output, expected)

    @patch('builtins.input')
    def test_3_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 3
        advanced_response = 'jack johnson'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team']\n"

        self.assertEqual(output, expected)
    
    @patch('builtins.input')
    def test_4_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 4
        advanced_response = 'for'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team']\n"

        self.assertEqual(output, expected)

    

    

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()
