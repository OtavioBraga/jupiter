FROM postgres:9.5.4
MAINTAINER Douglas Miranda <douglasmirandasilva@gmail.com>

# add backup scripts
ADD backup.sh /usr/local/bin/backup
ADD restore.sh /usr/local/bin/restore
ADD list-backups.sh /usr/local/bin/list-backups

# Install extensions
COPY install-extensions.sh /docker-entrypoint-initdb.d/install-extensions.sh

# make them executable
RUN chmod +x /usr/local/bin/restore
RUN chmod +x /usr/local/bin/list-backups
RUN chmod +x /usr/local/bin/backup
