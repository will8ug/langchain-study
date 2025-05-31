import unittest
import os
from dotenv import load_dotenv
from raw_function_play import get_weather

class TestWeatherIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment before running any tests"""
        # Load environment variables
        load_dotenv()
        
        # Verify API key exists
        if not os.getenv('OPENWEATHER_API_KEY'):
            raise ValueError("OPENWEATHER_API_KEY not found in environment variables")

    def test_real_weather_request(self):
        """Test weather API with real cities"""
        # Test with major cities
        cities = ['London', 'Tokyo', 'Guangzhou']
        
        for city in cities:
            result = get_weather(city)
            
            # Verify the response contains expected elements
            self.assertIn(city, result)
            self.assertIn('°C', result)
            self.assertNotIn('Error', result)
            
            # Print the result for manual verification
            print(f"\nWeather for {city}: {result}")

    def test_invalid_city(self):
        """Test weather API with an invalid city name"""
        result = get_weather('ThisCityDoesNotExist123456')
        self.assertIn('Error', result)
        print(f"\nInvalid city test result: {result}")

    def test_special_characters_city(self):
        """Test weather API with city names containing special characters"""
        cities = ['São Paulo', 'München', 'Côte d\'Ivoire']
        
        for city in cities:
            result = get_weather(city)
            self.assertIn(city, result)
            self.assertNotIn('Error', result)
            print(f"\nWeather for {city}: {result}")

    def test_weather_data_consistency(self):
        """Test that weather data is consistent for the same city"""
        city = 'London'
        
        # Get weather twice
        result1 = get_weather(city)
        result2 = get_weather(city)
        
        # Both results should contain the city name and temperature
        self.assertIn(city, result1)
        self.assertIn(city, result2)
        self.assertIn('°C', result1)
        self.assertIn('°C', result2)
        
        print(f"\nFirst weather check for {city}: {result1}")
        print(f"Second weather check for {city}: {result2}")

if __name__ == '__main__':
    unittest.main(verbosity=2) 