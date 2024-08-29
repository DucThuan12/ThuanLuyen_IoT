ThuanLuyen-IoT
Cài ThingsBoard: 
Đầu tiên tạo thư mục và mở terminal chạy lệnh: 
docker volume create mytb-data
docker volume create mytb-logs

Sau khi chạy 2 lệnh trên thành công thì tạo file Docker-compose.yml
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


Chạy lệnh sau để tạo CounterFit - Fake IoT Hardware
docker pull hungldvntts/counterfit-iot:latest
docker run -it -p 5000:5000 hungldvntts/counterfit-iot

Sau đó chạy lệnh 
docker compose pull
docker compose up
để chạy các image và container của ThingsBoard

Sau đó chạy "localhost:8080" để chạy ThingsBoard và "localhost:5000" để chạy CounterFit - Fake IoT Hardware
Tài khoản đăng nhập ThingsBorad:
Tài Khoản: tenant@thingsboard.org
Mật khẩu: tenant
