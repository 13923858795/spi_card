# spi_card


flask run -h 0.0.0.0 -p 80

nohup gunicorn app.app:create_app\(\) -b 0.0.0.0:80 -w 3 &
