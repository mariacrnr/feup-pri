output:= analysis/output
words:= analysis/words_analysis
text:=analysis/text_analysis

all: clean collect process analyze

clean:
	rm -rf data
clean_collection:
	rm -rf raw
clean_process:
	rm -rf data/clean
	rm -rf data/refined
clean_analysis:
	rm -rf $(output)
clean_null_analysis:
	rm -rf $(output)/null_analysis
clean_text_analysis:
	rm -rf $(output)/text_analysis
clean_words_analysis:
	rm -rf $(output)/words_analysis


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


analyze: analyze_nulls analyze_text analyze_words
analyze_nulls:
	mkdir -p $(output)/null_analysis
	python3 analysis/null_analysis.py

analyze_text: webpages_stats length_stats
webpages_stats:
	mkdir -p $(output)/text_analysis/webpages
	python3 $(text)/webpages.py
length_stats: 
	mkdir -p $(output)/text_analysis/length
	python3 $(text)/length.py

analyze_words: analyze_frequencies analyze_wordclouds
analyze_frequencies:
	mkdir -p $(output)/words_analysis/frequencies
	python3 $(words)/frequencies.py
analyze_wordclouds:
	mkdir -p $(output)/words_analysis/wordclouds
	python3  $(words)/wordclouds.py



adhoc: data_preparation_notebook data_exploration_notebook
data_preparation_notebook: processing/data_preparation.ipynb
	jupyter-nbconvert --to pdf $<;
data_exploration_notebook: analysis/data_exploration.ipynb
	jupyter-nbconvert --to pdf $<;

