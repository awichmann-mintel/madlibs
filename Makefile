-include $(shell curl -sSL -o .build-harness "https://raw.githubusercontent.com/mintel/build-harness/master/templates/Makefile.build-harness"; echo .build-harness)

init: init-build-harness
	@make pipenv
.PHONY: init

export SERVICE_NAME = mad_libz

.env:
	@read -p "Enter a port for your dev site: " DJANGO_DEV_PORT; \
	echo "# Port for dev site. Must end in a colon (:)." >> .env; \
	echo "DJANGO_DEV_PORT=$$DJANGO_DEV_PORT:" >> .env; \
	echo "Wrote DJANGO_DEV_PORT=$$DJANGO_DEV_PORT: to .env" 1>&2;
	@read -p "Enter a port for your dev site proxy: " PROXY_DEV_PORT; \
	echo "# Port for dev site. Must end in a colon (:)." >> .env; \
	echo "PROXY_DEV_PORT=$$PROXY_DEV_PORT:" >> .env; \
	echo "Wrote PROXY_DEV_PORT=$$PROXY_DEV_PORT: to .env" 1>&2;
	echo "DJANGO_SECRET_KEY=foobar" >> .env
	echo "DJANGO_DEBUG=1" >> .env
	echo "USE_EVEREST_NETWORK=true" >> .env

build: Pipfile.lock  ## build a Docker image of this Django project
	docker build . -f docker/Dockerfile -t "$${TAG:-mad_libz:latest}"
.PHONY: build

up: .env compose/up
.PHONY: up

down: .env compose/down
.PHONY: down

restart: compose/rebuild
.PHONY: restart

exec: docker/exec
.PHONY: exec

ps: compose/ps
.PHONY: ps

logs: compose/logs
.PHONY: logs

tail: logs
.PHONY: tail

lint: python/lint
.PHONY: lint

fmt: python/fmt
.PHONY: fmt

test: django/test
.PHONY: test

test-lf: pytest/test-lf
.PHONY: test-lf

test-post-build: pytest/test-post-build
.PHONY: test-post-build

release_patch: bumpversion/release_patch
.PHONY: release_patch

release_minor: bumpversion/release_minor
.PHONY: release_minor

release_major: bumpversion/release_major
.PHONY: release_major

clean: pipenv/clean python/clean clean-build-harness
	@exit 0
.PHONY: clean
