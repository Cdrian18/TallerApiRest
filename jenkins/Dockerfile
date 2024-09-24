FROM jenkins/jenkins:lts

# Instalar los plugins necesarios para git y pipelines
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# Cambiar a usuario root para instalar Node.js
USER root

# Usar Node.js 18, que es compatible con npm 10
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm

# Regresar al usuario Jenkins
USER jenkins
