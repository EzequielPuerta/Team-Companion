FROM python:3.8-buster AS base
LABEL maintainer="Tyke <proyecto-mesa@mercapsoftware.com>"

# hadolint ignore=DL3008
RUN set -eux; \
    apt-get update; \
    apt-get --assume-yes --no-install-recommends install \
        ca-certificates \
        gosu \
        ; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install \
    blinker~=1.4 \
    Flask~=2.0.1 \
    flask-login~=0.5.0 \
    flask-migrate~=2.5.3 \
    flask-sqlalchemy~=2.4.4 \
    Flask-WTF~=0.15.1 \
    psycopg2~=2.8.6 \
    python-dateutil~=2.8 \
    pytz~=2020.4 \
    requests~=2.27.1 \
    ;

ENV TEAM_COMPANION_PATH /opt/tyke/team_companion_kernel
ENV POSTGRES_SQL_PATH $TEAM_COMPANION_PATH/migrations

RUN mkdir -p \
        $TEAM_COMPANION_PATH/logs/ \
        $POSTGRES_SQL_PATH \
        ;

COPY team_companion/ $TEAM_COMPANION_PATH/team_companion/
COPY client.py $TEAM_COMPANION_PATH/client.py
COPY setup.sh $TEAM_COMPANION_PATH/setup.sh

RUN set -eux; \
    chmod ug=rwX \
        $TEAM_COMPANION_PATH/logs \
        $POSTGRES_SQL_PATH \
        ; \
    chmod ug+x \
        $TEAM_COMPANION_PATH/setup.sh \
        ;

# hadolint ignore=DL3002
USER root
WORKDIR $TEAM_COMPANION_PATH

# START NEW IMAGE: DEBUGGER
FROM base AS debug
VOLUME [ "$TEAM_COMPANION_PATH/logs/", "$POSTGRES_SQL_PATH/" ]
RUN pip install ptvsd~=4.3.2

COPY entrypoints/debugger.sh $TEAM_COMPANION_PATH/entrypoint.sh
RUN set -eux; \
    chmod ug+x $TEAM_COMPANION_PATH/entrypoint.sh;
CMD "$TEAM_COMPANION_PATH/entrypoint.sh"

# START NEW IMAGE: TESTING
FROM base AS testing
VOLUME [ "$TEAM_COMPANION_PATH/logs/", "$POSTGRES_SQL_PATH/" ]
RUN pip install ptvsd~=4.3.2

COPY entrypoints/testing.sh $TEAM_COMPANION_PATH/entrypoint.sh
RUN set -eux; \
    chmod ug+x $TEAM_COMPANION_PATH/entrypoint.sh;
CMD "$TEAM_COMPANION_PATH/entrypoint.sh"

# START NEW IMAGE: PRODUCTION
FROM base AS production
VOLUME [ "$TEAM_COMPANION_PATH/logs/", "$POSTGRES_SQL_PATH/" ]

COPY entrypoints/production.sh $TEAM_COMPANION_PATH/entrypoint.sh
RUN set -eux; \
    chmod ug+x $TEAM_COMPANION_PATH/entrypoint.sh;
CMD "$TEAM_COMPANION_PATH/entrypoint.sh"