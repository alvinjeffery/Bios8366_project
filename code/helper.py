# helper functions 

import matplotlib.pyplot as plt

def pie_chart(labels, df, var, title, font=14, figsize=(2, 2)):
    """
    Create pie chart of categorical variables.
    Inpute: labels (as a list), var - column from dataframe, title for figure
    """
    sizes = []
    for lab in labels: 
        sizes.append(len(df[df[var] == lab]))
    fig1, ax1 = plt.subplots()
    font = {'family' : 'monospace',
          'size'   : font}
    plt.rcParams["figure.figsize"] = figsize
    plt.rc('font', **font) 
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', pctdistance=0.8, startangle=90)
    ax1.axis('equal'); ax1.set_title(title, y=1.08); plt.show()
    
