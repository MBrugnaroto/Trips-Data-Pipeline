FROM apache/airflow:2.3.2

ADD webserver_config.py /opt/airflow
ADD airflow.cfg /opt/airflow

USER root

RUN apt-get update && \
    apt-get -y install apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common
RUN curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg > /tmp/dkey
RUN apt-key add /tmp/dkey && \
    add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
    $(lsb_release -cs) \
    stable"
RUN apt-get update && \
    apt-get -y install docker-ce

RUN /usr/local/bin/python -m pip install --upgrade pip

USER airflow
RUN pip install apache-airflow-providers-docker