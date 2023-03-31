import unittest
import requests


class TestWeatherAPI(unittest.TestCase):
    """Tests for the weather API. More test cases can be added for complete test coverage."""
    def setUp(self):
        self.base_url = "https://weather-app-backend-rjrobben.vercel.app"
    
    def test_a_get_weather_valid_location(self):
        location = "London"
        response = requests.get(f"{self.base_url}/weather?location={location}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("location" in data)
        self.assertTrue("weather" in data)
        self.assertTrue("icon_code" in data["weather"])

    def test_b_get_weather_invalid_location(self):
        location = "InvalidCity"
        response = requests.get(f"{self.base_url}/weather?location={location}")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["error"], "city not found")
    
    def test_c_get_weather_missing_location(self):
        response = requests.get(f"{self.base_url}/weather")
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"], "location parameter is missing")

    def test_d_get_forecast_valid_location(self):
        location = "London"
        response = requests.get(f"{self.base_url}/forecast?location={location}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("forecast" in data)

    def test_e_get_forecast_missing_location(self):
        response = requests.get(f"{self.base_url}/forecast")
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["error"], "location parameter is missing")
    
    def test_f_register_new_user(self):
        user_data = {
            "email": "test@test.com",
            "password": "password"
        }
        response = requests.post(f"{self.base_url}/register", json=user_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["message"], "Registered successfully")
    
    def test_g_register_existing_user(self):
        user_data = {
            "email": "test@test.com",
            "password": "password"
        }
        response = requests.post(f"{self.base_url}/register", json=user_data)
        self.assertEqual(response.status_code, 409)
        data = response.json()
        self.assertEqual(data["message"], "User already exists")
    
    def test_h_login_valid_credentials(self):
        user_data = {
            "email": "test@test.com",
            "password": "password"
        }
        response = requests.post(f"{self.base_url}/login", json=user_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["message"], "Logged in successfully")
    
    def test_i_login_invalid_credentials(self):
        user_data = {
            "email": "test@test.com",
            "password": "invalidpassword"
        }
        response = requests.post(f"{self.base_url}/login", json=user_data)
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertEqual(data["message"], "Invalid credentials")
    
    def test_j_login_user_does_not_exist(self):
        user_data = {
            "email": "nonexistent@test.com",
            "password": "password"
        }
        response = requests.post(f"{self.base_url}/login", json=user_data)
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["message"], "User does not exist")
    
if __name__ == '__main__':
    unittest.main()
