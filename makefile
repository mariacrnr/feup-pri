all: clean collect process analyze

clean:
	rm -rf data
clean_collection:
	rm -rf raw
clean_process:
	rm -rf data/clean
	rm -rf data/refined
clean_analysis:
	rm -rf analysis/output

.PHONY: collect processed analysis adhoc

collect: collect_data merge_data
collect_data:
	mkdir -p data/raw
	python3 collection/data_collection.py	
merge_data:
	python3 collection/data_merging.py


process: process_cleaning process_refinement
process_cleaning:
	mkdir -p data/clean
	python3 processing/data_cleaning.py
process_refinement:
	mkdir -p data/refined
	python3 processing/data_refinement.py


analyze: analyze_nulls
analyze_nulls:
	mkdir -p analysis/output/null_analysis
	python3 analysis/null_analysis.py
analyze_text:
	mkdir -p analysis/output/text_analysis
	python3 analysis/text_analysis.py
analyze_words:
	mkdir -p analysis/output/words_analysis
	python3 analysis/words_analysis.py


adhoc:
	# This target is not part of the overall automation, but it can be useful to have something similar
	# to automate some less frequent operation that you might want to run only when strictly necessary
	# (e.g., organize all produced data/analysis and run a notebook for an easier visual verification of obtained results)
	Rscript code/some_adhoc_script.R

