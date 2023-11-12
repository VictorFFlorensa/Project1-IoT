#!/bin/bash

echo "Este script va a borrar el contenedor influxdb y todos los volumenes, luego iniciarà un nuevo contenedor con influxdb."
echo "¿Quieres continuar? (y/n)"
read -r response

case "$response" in
    [yY])
        echo "Iniciando..."
        # Aquí puedes poner el código para la acción que deseas realizar
        # El contenedor existe, detener y eliminar
        docker stop influxdb_docker-influxdb-1 > /dev/null 2>&1
        docker rm influxdb_docker-influxdb-1 > /dev/null 2>&1
        docker volume prune -f > /dev/null 2>&1
        ;;
    [nN])
        echo "Saliendo del script. No se realizará ninguna acción."
        ;;
    *)
        echo "Respuesta no válida. Saliendo del script."
        ;;
esac
