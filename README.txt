First time openning the project you need to change the influxDB token key.

Look at docker-compose.yaml -> save-processor service for the authentication keys.

Once on http://influxdb:8086 :
Load your data -> Client Libraries -> Python -> Initialize the Client //here you will find the token.
