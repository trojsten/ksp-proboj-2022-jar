CLEAN = player.tar.gz player

.PHONY: clean player.tar.gz

player.tar.gz:
	tar -cvzf $@ $(wildcard *.py) Makefile

player: main.py
	cp $< $@
	chmod +x $@

clean:
	rm -f $(CLEAN)
