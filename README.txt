First time openning the project you need to change the influxDB Token key.

Start with $docker compose up -d --build

Open http://influxdb:8086 on browser:
Load your data -> Client Libraries -> Python -> Initialize the Client //here you will find the token.

On: docker-compose.yaml -> save-processor replace the new authentication key.


Other considerations:
Kafka consumer groups not working.
