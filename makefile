# ----- Project Targets ----- #
.PHONY: list clean

# -- list all possible target in this makefile
list:
	@echo "list of make targets:"
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null \
	| awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' \
	| sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs

# -- clean all temp files
clean:
	@echo "cleaning up workbench"
	rm  -fv   *.tmp
	rm  -fv   tmp_*
