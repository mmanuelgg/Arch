#!/bin/sh
case $1 in
    period-changed)
        exec notify-send "Redshift" "Periodo cambiado a $3"
esac
