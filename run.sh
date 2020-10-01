sudo docker container run -it --rm --env="DISPLAY" --net=host --device /dev/snd -v /tmp/.X11-unix:/tmp/.X11-unix -v /run/dbus/:/run/dbus/:rw -v /dev/shm:/dev/shm -v /tmp/record:/usr/src/app/records the_meteor_age_pygame

