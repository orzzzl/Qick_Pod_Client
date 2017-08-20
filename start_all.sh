#!/usr/bin/env bash

#starting manager server
python3 camera_manager/main.py &

#starting camera 0
python3 camera_service/main.py --camera_idx=0 &

#starting camera 1
python3 camera_service/main.py --camera_idx=1 &

#starting coordinator
python3 coordinator/main.py &

#starting video uploading
python3 network/main.py &

#starting gpio hardware service
python3 gpio_service/main.py &

#starting cleaning service
python3 data_cleaner/main.py &

#esc
python3 end_session_checker/main.py &

read cmd

pkill -P $$
