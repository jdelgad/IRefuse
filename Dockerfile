FROM python:3-onbuild
MAINTAINER Jacob Delgado
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install apt-utils
RUN apt-get -y install python3-dev
RUN apt-get -y install python3-venv
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-pip
RUN apt-get -y install libffi-dev
RUN apt-get -y install libssl-dev
RUN apt-get -y autoclean
RUN apt-get -y autoremove
RUN useradd -M -s /bin/nologin irefuse
RUN mkdir -p /opt/irefuse/irefuse
RUN pyenv-3.5 /opt/irefuse/venv
COPY requirements.txt /opt/irefuse/
RUN source /opt/irefuse/venv/bin/activate
RUN pip install pip --upgrade
RUN pip install wheel
RUN pip install -r /opt/irefuse/requirements.txt
COPY irefuse /home/irefuse/irefuse
RUN chown -R irefuse:irefuse /opt/irefuse/

USER irefuse
WORKDIR /home/web
ENV PYTHONPATH /opt/irefuse/venv
#COPY webapp /home/web/webapp
ENTRYPOINT ["/home/web/.venv/default/bin/cherryd", "-i", "server"]
