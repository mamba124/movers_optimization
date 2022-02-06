FROM continuumio/anaconda3:latest


#RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get update
RUN apt-get install -y wget \
        build-essential \
        libgl1-mesa-glx \
        libgtk-3-dev 
ARG FIREFOX_VERSION=63.0
RUN wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
   && rm -rf /opt/firefox \
   && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
   && rm /tmp/firefox.tar.bz2 \
   && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
   && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox
ARG GK_VERSION=v0.30.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz http://github.com/mozilla/geckodriver/releases/download/$GK_VERSION/geckodriver-$GK_VERSION-linux64.tar.gz \
   && rm -rf /opt/geckodriver \
   && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
   && rm /tmp/geckodriver.tar.gz \
   && mv /opt/geckodriver /opt/geckodriver-$GK_VERSION \
   && chmod 755 /opt/geckodriver-$GK_VERSION \
   && ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver

ENV TERM xterm

RUN mkdir app

ENV START=16

ENV FINISH=8

WORKDIR app/

#CMD ["python", " -m pip install --upgrade pip"]
RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY secret_files/ ./secret_files

COPY . .

CMD ["python", "api.py"]
