AUTHOR=$(shell git config --local user.name)
MDS:=intro.md ref.md link.md

MDS_MD:=$(addprefix md/,$(MDS))

MDS_MD_O:=$(addprefix md/o/,$(MDS))
MDS_MD_D:=$(MDS_MD_O:.md=.d)
MDS_MD_O:=$(MDS_MD_O) md/o/sample_code.md

MDS_O:=o/index.md $(addprefix o/,$(MDS)) o/sample_code.md

.PHONY: all html
all : o/example.md
html : o/example.html

-include $(MDS_MD_D)

MD_GEN:=../export/py

md/o/%.md : md/%.md
	$(MD_GEN)/md_compile.py -o $@ $< --mds $(MDS_MD)

md/o/sample_code.md : md/sample_code.md
	$(MD_GEN)/md_compile.py -o $@ $< --mds $(MDS_MD) md/sample_code.md

md/o/%.d : md/%.md
	$(MD_GEN)/md_compile.py -D $(@:.d=.md) -o $@ $< --mds $(MDS_MD)

o/index.md : md/o/example.json
	$(MD_GEN)/md_make_index.py --sec_num -o $@ $< \
		--exclude sample_code.md:2 --excerpt link.md:2

md/sample_code.md : $(MDS_MD)
	$(MD_GEN)/md_sample_section.py -o $@ $^

md/o/example.json :$(MDS_MD_O) 
	$(MD_GEN)/md_make_db.py $@ --mds $^

o/%.md : md/o/%.md md/o/example.json
	$(MD_GEN)/md_link.py --sec_num -o $@ --db md/o/example.json $<

%.png: %.pu
	$(MD_GEN)/plant_uml_encode.py $< -o $@
	$(MD_GEN)/png_checker.py $@ || (rm $@; exit 1)

o/example.md: $(MDS_O)
	$(MD_GEN)/md_join.py -o $@ $^

o/example.html: o/example.md
	[ -n "$(AUTHOR)" ]
	$(MD_GEN)/md_to_html.py --author "$(AUTHOR)" --title "md_gen example" -o $@ $<

.PHONY: clean help
clean:
	-rm -f $(MDS_MD_D)
	-rm -f $(MDS_MD_O)
	-rm -f $(MDS_O)
	-rm -f o/example.md o/example.html
	-rm -f md/sample_code.md md/o/example.json

help:
	@echo "make                     :generate o/example.md"
	@echo "make html                :generate o/example.html"
	@echo "make clean               :generated files are deleted"
	@echo "make help                :show this message"
	
