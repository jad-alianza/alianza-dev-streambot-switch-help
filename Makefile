-include .core.env
-include data-shared-project-utils/streaming/.env
-include .env
-include data-shared-project-utils/streaming/Makefile

.PHONY: update-base
update-base:  ## (initialize shared-utilities submodule and pull the latest files)
	git submodule update --init --recursive --remote --merge

.PHONY: print-env
print-env: ## (Print core variables)
	@echo "APP_NAME_FULL     : $$APP_NAME_FULL"
	@echo "APP_NAME_SHORT    : $$APP_NAME_SHORT"
	@echo "APP_NAME_FULL_SQL : $$APP_NAME_FULL_SQL"
	@echo "APP_NAME_SHORT_SQL: $$APP_NAME_SHORT_SQL"
