## Introduction

This project is the backend for the weather app. It is a simple API that returns the weather for a given city. It uses the OpenWeatherMap API to get the weather data.


## Installation

`pip install -r requirements.txt`

## Usage

`python app.py`

## API

### Get weather (GET Method)
http://localhost:5000/weather?location=city
http://localhost:5000/forecast?location=city

### User authentication (PUT Method)
http://localhost:5000/register
http://localhost:5000/login
http://localhost:5000/logout

## Testing
`python tests/test_api.py`

