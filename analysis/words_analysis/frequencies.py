import pandas as pd
from queue import Empty
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


path = "analysis/output/words_analysis/frequencies/"

def import_refined_data(group):
    df = pd.read_json("data/refined/" + group + '_refined.json')
    return df

def get_colors(data):
    colors = []

    for group in data:
        if(group == "PS"):
            colors.append("darkred")
        elif(group == "PSD"):
            colors.append("darkorange")
        elif(group == "CHEGA"):
            colors.append("darkblue")
        elif(group == "IL"):
            colors.append("lightblue")

    return colors


def political_groups_frequency(df, groups):
    
    df["text"] = df['text'].str.lower().str.replace(r'[^\w\s]','',regex=True)
 
    word_frequency = df.text.str.split().explode().value_counts().reset_index()
    
    word_frequency.columns = ['Word', 'Frequency'] 
    
    frequency0 = word_frequency.loc[word_frequency['Word'].str.contains("^" + groups[0] + "$", case=False)]
    frequency1 = word_frequency.loc[word_frequency['Word'].str.contains("^" + groups[1] + "$", case=True)]
    frequency2 = word_frequency.loc[word_frequency['Word'].str.contains("^" + groups[2] + "$", case=True)]  


    if(frequency0.empty):  
        final_frequence0 = 0
        final_frequence1 = frequency1.iloc[0]["Frequency"]
        final_frequence2 = frequency2.iloc[0]["Frequency"]
    elif(frequency1.empty):
        final_frequence0 = frequency0.iloc[0]["Frequency"]
        final_frequence1 = 0
        final_frequence2 = frequency2.iloc[0]["Frequency"]
    elif(frequency2.empty):
        final_frequence0 = frequency0.iloc[0]["Frequency"]
        final_frequence1 = frequency1.iloc[0]["Frequency"]
        final_frequence2 = 0
    else:
        final_frequence0 = frequency0.iloc[0]["Frequency"]
        final_frequence1 = frequency1.iloc[0]["Frequency"]
        final_frequence2 = frequency2.iloc[0]["Frequency"]


    return [final_frequence0, final_frequence1, final_frequence2]

def plot_pie_chart(groups, data, partie):    
    # Creating plot
    # Creating explode data
    explode = (0.1, 0.0, 0.2)

    colors = get_colors(groups)
    
    # Wedge properties
    wp = { 'linewidth' : 1, 'edgecolor' : "green" }
    
    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%\n({:d} g)".format(pct, absolute)
    
    # Creating plot
    fig, ax = plt.subplots(figsize =(10, 7))
    wedges, texts, autotexts = ax.pie(data,
                                    autopct = lambda pct: func(pct, data),
                                    explode = explode,
                                    labels = groups,
                                    shadow = True,
                                    colors = colors,
                                    startangle = 90,
                                    wedgeprops = wp,
                                    textprops = dict(color ="black"))
    
    # Adding legend
    ax.legend(wedges, groups,
            title ="Political Groups",
            loc ="center left",
            bbox_to_anchor =(1, 0, 0.5, 1))
    
    plt.setp(autotexts, size = 6, weight ="bold")
    
    plt.savefig(path + "/mentions_of_other_parties_" + partie + ".png", dpi=1000)
    

def run():
    political_parties = ['ps_merged', 'psd', 'ch', 'il']

    for group in political_parties:
        df = import_refined_data(group)
        if(group == 'ps_merged'):
            ps_frequency = political_groups_frequency(df, ['psd','ch','il'])
            plot_pie_chart(['PSD','CHEGA','IL'], ps_frequency, 'ps')
        elif(group == 'psd'):
            psd_frequency = political_groups_frequency(df, ['ps','ch','il'])
            plot_pie_chart(['PS','CHEGA','IL'], psd_frequency, group)
        elif(group == 'ch'):
            ch_frequency = political_groups_frequency(df, ['ps','psd','il'])
            plot_pie_chart(['PS','PSD','IL'], ch_frequency, group)
        elif(group == 'il'):
            il_frequency = political_groups_frequency(df, ['ps','psd','ch'])
            plot_pie_chart(['PS','PSD','CHEGA'], il_frequency, group)

run()