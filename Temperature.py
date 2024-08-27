import requests
from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT
import time

# Khởi tạo kết nối Counterfit
CounterFitConnection.init('127.0.0.1', 5000)

# Cấu hình cảm biến DHT
sensor = DHT("11", 5)

# URL của ThingsBoard với token thiết bị
ACCESS_TOKEN = 'E395HGkVyC9LLz4TsAbL'
THINGSBOARD_URL = f'http://localhost:8080/api/v1/{ACCESS_TOKEN}/telemetry'

while True:
    try:
        humidity, temperature = sensor.read()  # Đọc cả độ ẩm và nhiệt độ
        if humidity is not None and temperature is not None:
            # Tạo dữ liệu để gửi lên ThingsBoard
            payload = {
                'temperature': temperature,
                'humidity': humidity
            }
            # Gửi dữ liệu lên ThingsBoard
            response = requests.post(THINGSBOARD_URL, json=payload)
            print(f'Temperature: {temperature}°C, Humidity: {humidity}%, Status Code: {response.status_code}')
        else:
            print('Failed to read from sensor')
    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')
    
    time.sleep(10)  # Đọc dữ liệu mỗi 10 giây