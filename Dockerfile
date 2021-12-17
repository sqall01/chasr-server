FROM php:7-apache

RUN apt update
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

COPY . /app
RUN mv /app/config/config.php.template /app/config/config.php

RUN mv /app/* /var/www/html/