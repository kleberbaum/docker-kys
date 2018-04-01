FROM python:3.5-alpine

ADD requirements/ /requirements/
RUN set -ex && \
	echo "## Installing base ##" && \
	echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing/" >> /etc/apk/repositories && \
	echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community/" >> /etc/apk/repositories && \
	apk upgrade --update-cache --available && \
	apk add --no-cache --virtual=build-dependencies \
		gcc \
		g++ \
		make \
		libc-dev \
		musl-dev \
		linux-headers \
		pcre-dev \
		postgresql-dev \
		libjpeg-turbo-dev \
		git && \
	\
	apk add --force \
        tini@community \
    \
	&& pyvenv /venv \
	&& /venv/bin/pip install -U pip \
	&& LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install -r /requirements/production.txt" \
	&& runDeps="$( \
		scanelf --needed --nobanner --recursive /venv \
			| awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
			| sort -u \
			| xargs -r apk info --installed \
			| sort -u \
	)" \
	&& apk add --virtual .python-rundeps $runDeps \
	&& apk del build-dependencies \
    && rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /var/cache/distfiles/*
RUN apk add --no-cache postgresql-client
RUN mkdir /code/
WORKDIR /code/
ADD . /code/
RUN mv /code/run.sh /
EXPOSE 8000

# Add custom environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=esite.settings.production DJANGO_DEBUG=off

# uWSGI configuration (customize as needed):
ENV UWSGI_VIRTUALENV=/venv UWSGI_WSGI_FILE=esite/wsgi_production.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000

# Call collectstatic with dummy environment variables:
RUN DATABASE_URL=postgres://none REDIS_URL=none /venv/bin/python manage.py collectstatic --noinput

# make sure static files are writable by uWSGI process
RUN chown -R 1000:2000 /code/esite/media

# start uWSGI, using a wrapper script to allow us to easily add more commands to container startup:
ENTRYPOINT ["/sbin/tini", "--", "/run.sh"]
CMD ["/venv/bin/uwsgi", "--http-auto-chunked", "--http-keepalive", "--static-map", "/media/=/code/esite/media/"]
