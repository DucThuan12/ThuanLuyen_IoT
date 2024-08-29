# ThuanLuyen-IoT
```
## Mô tả
Dự án "ThuanLuyen-IoT" triển khai ThingsBoard và CounterFit - Fake IoT Hardware sử dụng Docker. Dự án này giúp giám sát và quản lý các thiết bị IoT thông qua ThingsBoard và mô phỏng phần cứng IoT với CounterFit.

## Yêu cầu Hệ thống
- Docker 20.10 trở lên
- Docker Compose 1.29 trở lên

## Cài đặt

### 1. Tạo Docker Volumes
Mở terminal và chạy các lệnh sau để tạo các volumes cho ThingsBoard:

- docker volume create mytb-data
- docker volume create mytb-logs

## 2. Tạo file Docker-compose.yml
Tạo một file Docker-compose.yml trong thư mục dự án của bạn với nội dung sau:

version: '3.0'
services:
  mytb:
    restart: always
    image: "thingsboard/tb-postgres"
    ports:
      - "8080:9090"
      - "1883:1883"
      - "7070:7070"
      - "5683-5688:5683-5688/udp"
    environment:
      TB_QUEUE_TYPE: in-memory
    volumes:
      - mytb-data:/data
      - mytb-logs:/var/log/thingsboard
volumes:
  mytb-data:
    external: true
  mytb-logs:
    external: true

## 3. Khởi động ThingsBoard
Chạy lệnh sau trong thư mục chứa file Docker-compose.yml để khởi động ThingsBoard:
- docker compose pull
- docker compose up
## 4. Cài đặt CounterFit - Fake IoT Hardware
Tải và chạy container CounterFit - Fake IoT Hardware bằng cách sử dụng các lệnh sau:
- docker pull hungldvntts/counterfit-iot:latest
- docker run -it -p 5000:5000 hungldvntts/counterfit-iot
## 5. File kết nối counterFit với ThingsBoard
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


