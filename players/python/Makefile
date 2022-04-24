#program name
PROGRAM := player

PYSOURCES := $(wildcard *.py)

# colors
Color_Off='\033[0m'
Black='\033[1;30m'
Red='\033[1;31m'
Green='\033[1;32m'
Yellow='\033[1;33m'
Blue='\033[1;34m'
Purple='\033[1;35m'
Cyan='\033[1;36m'
White='\033[1;37m'

all: $(PROGRAM) $(PROGRAM).tar.gz

$(PROGRAM).tar.gz: $(PYSOURCES) Makefile
	@echo -e $(Green)"Making tar for submit..."$(Color_Off)
	@tar -czf $@ $(PYSOURCES) Makefile
	@echo -e $(Green)"Tar successfully created!"$(Color_Off)

$(PROGRAM): main.py
	cp $< $@
	chmod +x $@

.PHONY: clean all run

run: $(PROGRAM)
	-@./$<

clean:
	@rm -f $(PROGRAM).tar.gz $(PROGRAM)
	@echo -e $(Cyan)"Cleaning Complete!"$(Color_Off)

