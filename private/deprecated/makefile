# ----- Project Targets ----- #
.PHONY: test startdb uml list clean

LOGSERER=${HOME}/data/db

# -- test
test:
	python tomo_6bm.py -d devices.yml scan.yml

# -- start mongodb logger server
startdb:
	@mongod  --dbpath $(LOGSERER)

# -- make uml diagram
uml:
	@echo "Making UML for devices module"
	@pyreverse -Amy -o pdf -p apsdevices devices.py
	@echo

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
