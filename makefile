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
clean_null_analysis:
	rm -rf analysis/output/null_analysis
clean_text_analysis:
	rm -rf analysis/output/text_analysis
clean_words_analysis:
	rm -rf analysis/output/words_analysis


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

analyze_text: webpages_stats length_stats
webpages_stats:
	mkdir -p analysis/output/text_analysis/webpages
	python3 analysis/text_analysis/webpages.py
length_stats: 
	mkdir -p analysis/output/text_analysis/length
	python3 analysis/text_analysis/length.py

analyze_words: analyze_frequencies analyze_wordclouds
analyze_frequencies:
	mkdir -p analysis/output/words_analysis/frequencies
	python3.py analysis/words_analysis/frequencies.py
analyze_wordclouds:
	mkdir -p analysis/output/words_analysis/wordclouds
	python3  analysis/words_analysis/wordclouds.py



adhoc:
	# This target is not part of the overall automation, but it can be useful to have something similar
	# to automate some less frequent operation that you might want to run only when strictly necessary
	# (e.g., organize all produced data/analysis and run a notebook for an easier visual verification of obtained results)
	Rscript code/some_adhoc_script.R

