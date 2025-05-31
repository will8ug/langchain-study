import unittest
from unittest.mock import patch, MagicMock
import os
from raw_function_play import get_weather

class TestWeatherFunction(unittest.TestCase):
    def setUp(self):
        # Set up test environment variables
        os.environ['OPENWEATHER_API_KEY'] = 'test_api_key'
        
        # Sample successful API response
        self.successful_response = {
            'weather': [{'description': 'clear sky'}],
            'main': {'temp': 20.5}
        }
        
        # Sample error API response
        self.error_response = {
            'cod': '404',
            'message': 'city not found'
        }

    def test_successful_weather_request(self):
        """Test successful weather API call"""
        with patch('requests.get') as mock_get:
            # Configure the mock
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = self.successful_response
            mock_get.return_value = mock_response

            # Call the function
            result = get_weather('London')

            # Assertions
            self.assertIn('clear sky', result)
            self.assertIn('20.5', result)
            self.assertIn('London', result)
            
            # Verify the API was called correctly
            mock_get.assert_called_once()
            args, kwargs = mock_get.call_args
            self.assertEqual(kwargs['params']['q'], 'London')
            self.assertEqual(kwargs['params']['appid'], 'test_api_key')
            self.assertEqual(kwargs['params']['units'], 'metric')

    def test_missing_api_key(self):
        """Test behavior when API key is missing"""
        # Temporarily remove the API key
        os.environ.pop('OPENWEATHER_API_KEY', None)
        
        result = get_weather('London')
        self.assertIn('Error: OpenWeather API key not found', result)

    def test_city_not_found(self):
        """Test behavior when city is not found"""
        with patch('requests.get') as mock_get:
            # Configure the mock
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.json.return_value = self.error_response
            mock_get.return_value = mock_response

            result = get_weather('NonexistentCity')
            self.assertIn('Error: Could not get weather', result)

    def test_api_request_failure(self):
        """Test behavior when API request fails"""
        with patch('requests.get') as mock_get:
            # Configure the mock to raise an exception
            mock_get.side_effect = Exception('Network error')

            result = get_weather('London')
            self.assertIn('Error: Network error', result)

    def test_empty_city_name(self):
        """Test behavior with empty city name"""
        result = get_weather('')
        self.assertIn('Error: Could not get weather', result)

if __name__ == '__main__':
    unittest.main() 