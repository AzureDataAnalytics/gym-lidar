#!/bin/bash

# Menjalankan layanan pigpio
echo "Starting pigpio daemon..."
sudo systemctl start pigpiod

# Mengecek status layanan
sudo systemctl status pigpiod --no-pager
