import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib as mpl
from IPython.core.display import HTML
import matplotlib.pyplot as plt
pd.options.display.float_format = '{:,.0f}'.format

bgcolor ='#205373'; text_color = '#F2E6C2'
innerbackcolor = "#C4E1F2"; outerbackcolor = "#205373"; fontcolor = "#F2E6C2"

# Styling notebook

def css_styling():
    from IPython.core.display import HTML
    styles = open("notebook_styles.css", "r").read()
    return HTML(styles)

# .......................DISPLAYING........................................ #
def display_me(df, num, title, bgcolor= bgcolor, text_color=text_color):
    from IPython.core.display import HTML
    if type(df) != pd.core.frame.DataFrame:
        df = df.to_frame()
        
    head_data = "<center>" + df.head(num).to_html()
    tail_data = "<center>" + df.tail(num).to_html()
    
    print("")
    div_print(f'{title.upper()} (first {num} rows of data)', fontsize = 4,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(head_data))
    print("")
    div_print(f'{title.upper()} (last {num} rows of data)', fontsize = 4,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(tail_data))
    print("")
    
    

def sample_df(data, num, title, width="auto",
              bgcolor= bgcolor, text_color=text_color):
    
    if bgcolor != None:
        bgcolor = bgcolor
    else:
        bgcolor = def_bgcolor
    if text_color != None:
        text_color = text_color
    else:
        text_color = def_text_color
        
    df = data.sample(num)
    df = "<center>" + df.to_html()
    div_print(f'{title.upper()} ({num} random samples)', fontsize = 3, width=width,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(df))

    
def center_df(df, title=None, width="auto",
             bgcolor=bgcolor, text_color=text_color):
    pd.options.display.float_format = '{:,.0f}'.format    
    if title != None:
        div_print(f"{title.upper()}", fontsize = 4, width=width,
                 bgcolor=bgcolor, text_color=text_color)
    display(HTML("<center>" + df.to_html()))
    
    
def center_series(series, title=None, width="auto",
                 bgcolor=bgcolor, text_color=text_color):
    pd.options.display.float_format = '{:,.0f}'.format
    if title != None:
        div_print(f"{title.upper()}", fontsize = 4, width=width,
                 bgcolor=bgcolor, text_color=text_color)
    display(HTML("<center>" + series.to_frame().to_html()))
    
    
def list_to_table(display_list, num_cols, title, width = "auto",
                  bgcolor=bgcolor, text_color=text_color):
        
    div_print(f"{title.upper()}", fontsize = 4, width=width,
             bgcolor=bgcolor, text_color=text_color)
    
    count = 0
    current = '<center><table><tr>'
    length = len(display_list)
    num_rows = round(length / num_cols) + 1

    for h in range(num_rows):
        for i in range(num_cols):
            try:
                current += ('<td>' + display_list[count] + '</td>')
            except IndexError:
                current += '<td>' + ' ' + '</td>'
            count += 1
        current += '</tr><tr>'
    current += '</tr></table></center>'
    display(HTML(current))
# ........................................................................ #

def div_print(text, width='auto',  bgcolor=bgcolor, text_color=text_color,
              fontsize=2):
    from IPython.display import HTML as html_print
        
    return display(html_print("<span style = 'display: block; width: {}; \
                                line-height: 2; background: {};\
                                margin-left: auto; margin-right: auto;\
                                border: 1px solid text_color;\
                                border-radius: 3px; text-align: center;\
                                padding: 3px 8px 3px 8px;'>\
                                <b><font size={}><text style=color:{}>{}\
                                </text></font></b></style>".format(width, bgcolor, 
                                                                   fontsize,
                                                                   text_color, text)))


def overview(df, title=None,  bgcolor=bgcolor, text_color=text_color):
    from IPython.display import HTML
        
    num_rows = df.shape[0]
    num_cols = df.shape[1]
    columns = list(df.columns)
    total_na = df.isna().sum().sum()
    columns = str(', '.join(list(df.columns)))
    
    overview_table = '<center><table>\
            <tr><td><font size=3><b>Columns Labels</b></font></td><td>{}</td></tr>\
            <tr><td><font size=3><b>Missing Values </b></font></td><td>{:,}</td></tr>\
            <tr><td><font size=3><b>Total Rows </b></font></td><td>{:,}</td></tr>\
            <tr><td><font size=3><b>Total Columns </b></font></td><td>{}</td></tr>\
            </table></center>'
    
    categorical_table = "<center>" + df.describe(include="O").to_html()
    numerical_table = "<center>" + df.describe().to_html()
    
    div_print(f'{title.upper()}: Dataframe Overview', fontsize=4, 
              bgcolor=bgcolor, text_color=text_color)
    display(HTML(overview_table.format(columns, total_na, num_rows, num_cols)))
    div_print(f'{title.upper()}: Categorical Data', fontsize = 4,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(categorical_table))
    div_print(f'{title.upper()}: Numerical Data', fontsize = 4,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(numerical_table))

    
    
    
    
def missing_values(df,  bgcolor=bgcolor, text_color=text_color):
    from IPython.display import HTML
    pd.options.display.float_format = '{:,.0f}'.format   
    missing_log = []
    for column in df.columns:
        missing_values = df[column].isna().sum()
        missing_log.append([column, missing_values])
    missing = pd.DataFrame(missing_log, columns = ['column name', 'missing'])
    div_print(f'Columns and Missing Values', fontsize=3, width="38%",
             bgcolor=bgcolor, text_color=text_color)
    missing = "<center>" + missing.to_html()
    display(HTML(missing))
    
    
 # ..................................................... #

def fancy_plot(data, kind = "line", title = None, legend_loc = 'upper right', 
               xlabel=None, ylabel=None, logy=False, outerbackcolor=outerbackcolor, 
               innerbackcolor=innerbackcolor, fontcolor=fontcolor, cmap = 'viridis', 
               label_rot = None):
    
    import random 
    import matplotlib as mpl
    import matplotlib.pyplot as plt
        
    mpl.rcParams['xtick.color'] = outerbackcolor
    mpl.rcParams['ytick.color'] = outerbackcolor
    mpl.rcParams['font.family'] = 'monospace'
    fig = plt.subplots(facecolor = outerbackcolor, figsize = (13, 7))
    ax = plt.axes();
    if kind == 'line':
        data.plot(kind='line', ax = ax, rot = label_rot, cmap = cmap, logy=logy)
    else:
        data.plot(kind = kind, ax = ax, rot = label_rot, cmap = cmap, logy=logy);
    plt.style.use("ggplot");
    ax.set_facecolor(innerbackcolor)
    ax.grid(color=fontcolor, linestyle=':', linewidth=0.75, alpha = 0.75)
    plt.tick_params(labelrotation = label_rot);
    plt.title(title, fontsize = 23, pad = 20, color=fontcolor);
    plt.ylabel(ylabel, fontsize = 18, color=fontcolor);
    plt.xlabel(xlabel, fontsize = 18, color=fontcolor);
    plt.xticks(fontsize=10, color=fontcolor)
    plt.yticks(fontsize=10, color=fontcolor)
    if legend_loc is None:
        ax.get_legend().remove()
    else:
        plt.legend(labels = data.columns, fontsize = 15, loc = legend_loc,
                   facecolor = outerbackcolor, labelcolor = fontcolor)
     


def correlation_heatmap(df, cmap, method = "pearson",
                        annot = True, fmt = '.2g',
                        vmin = 0.2, vmax = 0.8, label_rot = None,
                       title = None, figsize=(10,10)):
    import seaborn as sns
    import matplotlib as mpl
    mpl.rcParams['text.color'] = outerbackcolor
    mpl.rcParams['axes.labelcolor'] = outerbackcolor
    mpl.rcParams['xtick.color'] = outerbackcolor
    mpl.rcParams['ytick.color'] = outerbackcolor
    correlation_map = df.corr(method = method)
    plt.figure(figsize = figsize, facecolor = outerbackcolor)

    sns.heatmap(correlation_map, cmap = cmap, annot = annot, vmin = vmin,
               vmax = vmax, linewidth=0.25, linecolor = "white", fmt = fmt)                
    plt.title(title, fontsize = 20, pad = 20, color=fontcolor);
    plt.xticks(fontsize=11, color=fontcolor)
    plt.yticks(fontsize=11, color=fontcolor)
    plt.tick_params(labelrotation = label_rot);
    
    
def top_competitors(df):
	sport_input = input("Which sport? ")
	number = input("How many of the top countries? ")
	try:
		df = pd.crosstab(df.country, 
						df.discipline)\
						[sport_input].sort_values(ascending=False).head(int(number))
	
		return center_df(df.to_frame(), 
						   title = f"Top competing countries in {sport_input}",
						   width="50%")
	except KeyError:
		div_print("An error has occured. Please try again.", width = "60%")
		div_print("Input sport exactly as displayed above.", width = "60%")  
     
    
def top_sports_for_country(df):
	country_input = input("Which country? ")
	number = input("How many top sports? ")
	try:
		df = pd.crosstab(df.country, 
df.discipline).loc[country_input].sort_values(ascending=False).head(int(number))
	
		return center_df(df.to_frame(), 
						   title = f"Top sports {country_input} competes in",
						   width="50%")
	except KeyError:
		div_print("An error has occured. Please try again.", width = "60%")
		div_print("Input country exactly as displayed above.", width = "60%")   
    
