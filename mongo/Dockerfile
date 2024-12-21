FROM mongo:latest

ARG MONGO_SSH_USERNAME
ARG MONGO_SSH_PASSWORD

RUN apt-get update && apt-get install -y openssh-server supervisor

## Tworzenie użytkownika, aby umożliwić logowanie przez SSH
RUN useradd -m -s /bin/bash "${MONGO_SSH_USERNAME}" && echo "${MONGO_SSH_USERNAME}:${MONGO_SSH_PASSWORD}" | chpasswd

RUN mkdir /var/run/sshd \
    && echo 'PasswordAuthentication yes' >> /etc/ssh/sshd_config

#COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
#
#CMD ["/usr/bin/supervisord"]