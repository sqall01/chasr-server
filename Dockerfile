FROM php:7-apache

RUN apt update
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli
COPY . /app

RUN sed -i "s|\$config_mysql_server = \"localhost\";|\$config_mysql_server = getenv(\"MYSQL_SERVER\");|g" /app/config/config.php.template
RUN sed -i "s|\$config_mysql_username = \"chasr_db_user\";|\$config_mysql_username = getenv(\"MYSQL_USERNAME\");|g" /app/config/config.php.template
RUN sed -i "s|\$config_mysql_password = \"<SECRET>\";|\$config_mysql_password = getenv(\"MYSQL_PASSWORD\");|g" /app/config/config.php.template
RUN sed -i "s|\$config_mysql_database = \"chasr\";|\$config_mysql_database = getenv(\"MYSQL_DATABASE\");|g" /app/config/config.php.template
RUN sed -i "s|\$config_mysql_port = 3306;|\$config_mysql_port = getenv(\"MYSQL_PORT\");|g" /app/config/config.php.template
RUN sed -i "s|\$config_session_expire = 86400;|\$config_session_expire = getenv(\"SESSION_EXPIRE\");|g" /app/config/config.php.template
RUN sed -i "s|\$config_chasr_num_min_devices = 2;|\$config_chasr_num_min_devices = getenv(\"NUM_MIN_DEVICES\");|g" /app/config/config.php.template
RUN sed -i "s|\$config_chasr_num_mid_devices = 5;|\$config_chasr_num_mid_devices = getenv(\"NUM_MID_DEVICES\");|g" /app/config/config.php.template
RUN sed -i "s|\$config_chasr_num_max_devices = 20;|\$config_chasr_num_max_devices = getenv(\"NUM_MAX_DEVICES\");|g" /app/config/config.php.template

RUN mv /app/config/config.php.template /app/config/config.php

RUN mv /app/* /var/www/html/