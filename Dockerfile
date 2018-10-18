FROM python:3.6-alpine3.7

LABEL description="The erebos website more manageable w/ wagtail."

# this is maintained by kleberbaum
MAINTAINER Florian Kleber <kleberbaum@erebos.xyz>

# Add custom environment variables needed by Django or your settings file here:
ENV DJANGO_DEBUG=off \
	DJANGO_SETTINGS_MODULE=esite.settings.production

# uWSGI configuration (customize as needed):
ENV UWSGI_UID=1000 UWSGI_GID=2000 \
	UWSGI_HTTP=:8000 \
	UWSGI_VIRTUALENV=/venv \
	UWSGI_WSGI_FILE=esite/wsgi_production.py \
	UWSGI_MASTER=1 \
	UWSGI_WORKERS=3 \
	UWSGI_THREADS=8

WORKDIR /code/

# pre installation requirements XD
ADD requirements/ /requirements/

RUN set -e && \
	\
	echo "## Adjust APK ##" && \
	echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing/" \
		>> /etc/apk/repositories && \
	echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community/" \
		>> /etc/apk/repositories && \
	apk upgrade --update-cache --available && \
	\
	echo "## Installing base ##" && \
	apk add --virtual=build-dependencies \
		gcc \
		g++ \
		make \
		libc-dev \
		musl-dev \
		linux-headers \
		pcre-dev \
		postgresql-dev \
		git && \
	apk add --force \
		tiff-dev \
		zlib-dev \
		freetype-dev \
		libjpeg-turbo-dev \
		postgresql-client \
        tini@community \
  	\
	&& python -m venv /venv \
	&& /venv/bin/pip install -U pip \
	\
	&& LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install -r \
		/requirements/production.txt" \
	\
	&& runDeps="$( \
			scanelf --needed --nobanner --recursive /venv \
				| awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
				| sort -u \
				| xargs -r apk info --installed \
				| sort -u \
	   )" \
   \
   && apk add --virtual .python-rundeps $runDeps \
   && apk del build-dependencies \
   && rm -rf /tmp/* /var/tmp/* /var/cache/apk/* /var/cache/distfiles/*

EXPOSE 8000

ADD . /code/

# place init
RUN mv /code/run.sh /

# Call collectstatic with dummy environment variables:
RUN DATABASE_URL=postgres://none REDIS_URL=none && \
/venv/bin/python manage.py collectstatic --noinput

# make sure static files are writable by uWSGI process
RUN chown -R 1000:2000 /code/esite/media

# I personally like to start my containers with tini ^^
# which start uWSGI, using a wrapper script to allow us to easily add
# more commands to container startup:
ENTRYPOINT ["/sbin/tini", "--", "/run.sh"]

CMD ["/venv/bin/uwsgi", "--http-auto-chunked", \
			"--http-keepalive", \
			"--static-map", \
			"/media/=/code/esite/media/" \
]
