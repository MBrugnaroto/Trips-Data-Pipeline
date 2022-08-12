FROM postgres:11

ENV POSTGRES_PASSWORD postgres 
ENV POSTGRES_DB mobi7_code_interview 

COPY postgresql.conf /postgresql.conf
COPY ./set-config.sh \
     ./initdb.sql /docker-entrypoint-initdb.d/
