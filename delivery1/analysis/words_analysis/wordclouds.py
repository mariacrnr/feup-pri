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
    wordcloud = WordCloud(background_color="white", width=800, height=700,collocations=False).generate(df_without_stopwords)
    svg_file=wordcloud.to_svg()
    f = open(path + "/wordcloud_" + group + ".svg",'w')
    f.write(svg_file)
    f.close()
    plt.figure( figsize=(20.0*8.0/7.0,20.0) )
    plt.imshow(wordcloud)
    plt.axis('off')
    # plt.savefig(path + "/wordcloud_" + group + ".pdf")

def run():
    political_parties = ['ps_merged', 'psd', 'ch', 'il']

    for group in political_parties:
        df = import_refined_data(group)
        df_without_stopwords = wordcloud_setup(df)
        plot_wordcloud(df_without_stopwords, group)

run()