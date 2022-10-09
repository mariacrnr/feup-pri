import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

path = "analysis/output/words_analysis/wordclouds/"

def import_refined_data(group):
    df = pd.read_json("data/refined/" + group + '_refined.json')
    return df


def wordcloud_setup(df):
    stop = stopwords.words('portuguese') + ["ser","quer","se","sobre","toda","assim","sendo"]

    wordcloud_text=df["text"].str.replace("[$&+-:;“”=?@#|'<>.^*()%!,\"\/]"," ",regex=True)
    wordcloud_text=wordcloud_text.str.replace("\d","",regex=True)
    wordcloud_text=wordcloud_text.str.replace(" +"," ",regex=True)


    df_without_stopwords=" ".join(wordcloud_text)
    df_without_stopwords=' '.join([word.lower() for word in df_without_stopwords.split(" ") if word.lower() not in (stop)])

    return df_without_stopwords


def plot_wordcloud(df_without_stopwords, group):
    wordcloud = WordCloud(width=800, height=400,collocations=False).generate(df_without_stopwords)

    plt.figure( figsize=(20,10) )
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.savefig(path + "/wordcloud_" + group + ".png", dpi=1000)

def run():
    political_parties = ['ps_merged', 'psd', 'ch', 'il']

    for group in political_parties:
        df = import_refined_data(group)
        df_without_stopwords = wordcloud_setup(df)
        plot_wordcloud(df_without_stopwords, group)

run()