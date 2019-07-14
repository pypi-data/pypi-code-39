import unittest
from chatParser import WhatsAppChatParser


class TestWhatsAppChatParser(unittest.TestCase):
    def test_ignore_deleted_messages(self):
        test_data_file = "deletedLinesTestData.txt"
        expected_output_text = "Quote 3\n"

        chatparser = WhatsAppChatParser(test_data_file)
        chatparser.SetMessageAuthor("Aashish")
        chatparser.ExtractQuoteList(test_data_file)
        first_quote = chatparser.getNextQuote()
        second_quote = chatparser.getNextQuote()
        Third_quote = chatparser.getNextQuote()
        actual_output = Third_quote

        self.assertEqual(actual_output, expected_output_text)

    def test_multiline_is_supported(self):
        test_data_file = "multilineTestData.txt"
        expected_output_text = "Ignorance is bliss\n\n"
        expected_output_text += "Its so painful to be aware of negative effects of my own actions\n\n"
        expected_output_text += "Still falling victim of this uncontrolled mind\n"
        chatparser = WhatsAppChatParser(test_data_file)
        chatparser.SetMessageAuthor("Aashish")
        chatparser.ExtractQuoteList(test_data_file)
        actual_output = chatparser.getNextQuote()

        self.assertEqual(actual_output, expected_output_text)

    def test_messages_on_or_after_a_date(self):
    	test_data_file = "dateFilterTestData.txt"
    	message1 = "Quote4\n"
    	message2 = "Quote5\n"
    	chatparser = WhatsAppChatParser(test_data_file)
    	chatparser.SetMessageAuthor("All")
    	chatparser.SetStartDate("16/11/19")
    	chatparser.ExtractQuoteList(test_data_file)
    	self.assertEqual(chatparser.getNextQuote(), message1)
    	self.assertEqual(chatparser.getNextQuote(), message2)

    def test_messages_on_or_before_a_date(self):
    	test_data_file = "dateFilterTestData.txt"
    	message1 = "Quote1\n"
    	message2 = "Quote2\n"
    	message3 = "Quote3\n"
    	chatparser = WhatsAppChatParser(test_data_file)
    	chatparser.SetMessageAuthor("All")
    	chatparser.SetEndDate("15/11/19")
    	chatparser.ExtractQuoteList(test_data_file)
    	#print(chatparser.getNextQuote())
    	#print(chatparser.getNextQuote())
    	#print(chatparser.getNextQuote())
    	#self.assertEqual(chatparser.getNextQuote(), message1)
    	#self.assertEqual(chatparser.getNextQuote(), message2)
    	#self.assertEqual(chatparser.getNextQuote(), message3)
    	#self.assertRaises(Exception,chatparser.getNextQuote())
