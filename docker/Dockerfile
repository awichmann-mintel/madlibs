FROM python:3.6-slim

# Config
ENV APP_DIR=/app \
    DJANGO_SETTINGS_MODULE=config.settings \
    DJANGO_STATIC_ROOT=/static

# Set up volumes.
VOLUME ["/etc/nginx/conf.d", "${DJANGO_STATIC_ROOT}"]

# Add scripts to do good Docker package management.
COPY install_packages.sh /usr/bin/install_packages
COPY upgrade_packages.sh /usr/bin/upgrade_packages
COPY remove_packages.sh /usr/bin/remove_packages

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED=1

# Don't cache pip packages (pip uses falsey values like 0 to indicate a flag is set for some reason).
ENV PIP_NO_CACHE_DIR=0

# Expose the gunicorn port.
EXPOSE 80

# Set up health check.
RUN install_packages curl
HEALTHCHECK CMD curl -f http://127.0.0.1/health-check/ || exit 1

# Setup Docker entrypoint.
COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# Install Python dependencies.
COPY Pipfile Pipfile.lock ./
ARG JFROG_USERNAME=
ARG JFROG_ACCESS_TOKEN=
ENV PIPENV_ARGS="" \
    JFROG_USERNAME=${JFROG_USERNAME} \
    JFROG_ACCESS_TOKEN=${JFROG_ACCESS_TOKEN}
RUN set -ex; \
    buildDeps=" \
        gcc \
    "; \
    install_packages $buildDeps; \
    pip install pipenv; \
    pipenv install --deploy --system $PIPENV_ARGS; \
    pip uninstall --yes pipenv; \
    remove_packages $buildDeps;

# Copy app.
COPY . ${APP_DIR}
WORKDIR ${APP_DIR}

# Set log level and Everest environment.
ENV APP_ENVIRONMENT=dev
ARG LOG_LEVEL=INFO
ENV EVEREST_LOG_LEVEL=${LOG_LEVEL}

# Environment variables that will change on every build.
ARG GIT_HASH=
ARG JENKINS_BUILD=
ENV EVEREST_GIT_HASH=${GIT_HASH} \
    EVEREST_JENKINS_BUILD=${JENKINS_BUILD}

# Upgrade system packages to get latest security updates.
RUN upgrade_packages
