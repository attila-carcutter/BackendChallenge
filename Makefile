.PHONY: format
format:
	black .

.PHONY: unit-test
unit-test:
	pytest tests/unit/

.PHONY: coverage
coverage: unit-test
	coverage report
