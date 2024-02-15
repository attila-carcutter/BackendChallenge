SHELL=/bin/bash -e -u -o pipefail


.PHONY: format
format:
	black .

.PHONY: unit-test
unit-test:
	pytest tests/unit/

.PHONY: acceptance-test
acceptance-test:
	pytest --no-cov tests/acceptance/

.PHONY: coverage
coverage: unit-test
	coverage report

dirs := api/ tests/
.PHONY: lint
lint:
	black --check $(dirs)
	mypy $(dirs)

.PHONY: run
run:
	cli api-server vehicle-features
