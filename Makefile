.PHONY: fmt

fmt:
	@black --exclude venv/ --line-length 120 --target-version py37 .

.PHONY: check-fmt
check-fmt:
	@black --check --exclude venv/ --line-length 120 --target-version py37 .

.PHONY: tests
tests:
	@pytest configatron/