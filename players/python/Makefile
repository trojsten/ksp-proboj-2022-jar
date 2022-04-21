#program name
PROGRAM = player

$(PYSOURCES) = $(wildcard *.py)

.PHONY: clean run $(program).tar.gz

$(program).tar.gz: $(PYSOURCES) Makefile
	@echo -e $(Green)"Making tar for submit..."$(Color_Off)
	@tar -czf $@ $(PYSOURCES) Makefile
	@echo -e $(Green)"Tar successfully created!"$(Color_Off)

$(program): main.py
	cp $< $@
	chmod +x $@

run: $(program)
	@./$<

clean:
	@rm -f $(program).tar.gz $(program)
	@echo -e $(Cyan)"Cleaning Complete!"$(Color_Off)

