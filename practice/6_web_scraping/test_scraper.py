import unittest
from unittest.mock import patch, MagicMock
from stock_info import clean_numeric, get_tickers, get_stock_data, scraper_session

class TestScraper(unittest.TestCase):

    def test_clean_numeric(self):
        self.assertEqual(clean_numeric("1.5B"), 1500000000.0)
        self.assertEqual(clean_numeric("500M"), 500000000.0)
        self.assertEqual(clean_numeric("+15.4%"), 15.4)
        self.assertEqual(clean_numeric("N/A"), 0.0)
        self.assertEqual(clean_numeric("-"), 0.0)

    @patch('stock_info.scraper_session.get')
    def test_get_tickers(self, mock_get):

        fake_html = """
        <table>
            <tr class="row yf-1og7bvd">
                <td>
                    <span class="symbol yf-1pdfbgz">AAPL</span>
                    <div class="leftAlignHeader companyName yf-362rys enableMaxWidth">Apple Inc.</div>
                </td>
            </tr>
            <tr class="row yf-1og7bvd">
                <td>
                    <span class="symbol yf-1pdfbgz">TSLA</span>
                    <div class="leftAlignHeader companyName yf-362rys enableMaxWidth">Tesla, Inc.</div>
                </td>
            </tr>
        </table>
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = fake_html.encode('utf-8')
        mock_get.return_value = mock_response

        result = get_tickers()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['symbol'], "AAPL")
        self.assertEqual(result[0]['name'], "Apple Inc.")
        self.assertEqual(result[1]['symbol'], "TSLA")

       
       
if __name__ == '__main__':
    unittest.main()