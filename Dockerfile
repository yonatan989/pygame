FROM python:3.8
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN apt-get update && apt install -y \
python-dev \
libsdl-image1.2-dev \
libsdl-mixer1.2-dev \
libsdl-ttf2.0-dev \
libsdl1.2-dev \ 
libsmpeg-dev \ 
python-numpy \
subversion \
libportmidi-dev \
ffmpeg \
libswscale-dev \
libavformat-dev \
libavcodec-dev \
libfreetype6-dev \ 
vim 
RUN pip install --upgrade pip && \
    pip install --no-cache -r requirements.txt
CMD [ "python", "./OOP_PYGAME/DodKIng.py"]
