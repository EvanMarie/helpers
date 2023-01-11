import pandas as pd
import numpy as np
import matplotlib as mpl
from IPython.core.display import HTML
import matplotlib.pyplot as plt
pd.options.display.float_format = '{:,.2f}'.format

bgcolor ='#333333'; text_color = 'white'
innerbackcolor = "#222222"; outerbackcolor = "#33333"; fontcolor = "white"

# FUNCTIONS: d, p, sp, table_of_contents, display_me, sample_df, center_df, center_series
#	     list_to_table, div_print, overview, missing_values, fancy_plot



# ......................TINY_GUYS....................................... #

def sp(): print('');
def p(x): print(x); sp()
def d(x): display(x); sp()

def pretty(input, fontsize=3, bgcolor = '#444444', 
			 textcolor="white", width=None, label=None): 
	from IPython.display import HTML
	input = str(input)
	
	def get_color(color):
		label_font = [x - 3 for x in [int(num) for num in color[1:]]]
		label_font = "#" + "".join(str(x) for x in label_font)
		return label_font
	
	if label != None:
		label_font = get_color(bgcolor)
		pretty(label, fontsize=fontsize, bgcolor = 'white', 
					textcolor=label_font, 	width=width, label=None)
	display(HTML("<span style = 'line-height: 1.5; \
                                background: {}; width: {}; \
                                border: 1px solid text_color;\
                                border-radius: 0px; text-align: center;\
                                padding: 3px;'>\
                                <b><font size={}><text style=color:{}>{}\
                                </text></font></b></style>".format(bgcolor, width,
                                                                   fontsize,
                                                                   textcolor, input)))


def div_print(text, width ='auto',  bgcolor=bgcolor, text_color=text_color,
              fontsize=2):
    from IPython.display import HTML as html_print

    if width != 'auto':
        if width[-1] != '%':
            width = str(width) + "px"
        
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

# ......................TABLE_OF_CONTENTS....................................... #


def parse_links(basic_list):

	link_names = []
	link_links = []
	link_tags = []

	for item in basic_list:
		item_parts = item.split()
		name = "[" + item.title() + "]"
		link_names.append(name)
		
		try:
			item_tag = "<a name = '" + item_parts[0] + "_" + item_parts[1] + "'></a>"
			item_link = "(#" + item_parts[0] + "_" + item_parts[1] + ")"
		except:
			item_tag = "<a name = '" + item_parts[0] + "'></a>"
			item_link = "(#" + item_parts[0] + ")"
			

		link_links.append(item_link.lower())
		link_tags.append(item_tag.lower())

	return link_names, link_links, link_tags



def table_of_contents(title='', head1 = None, head2=None, col1=[], col2=[]):
	from IPython.display import HTML
	table_data = "<center><font size=6> " + title + "</font></center>  \n  \n|<font size=4> " + head1 +  "|   |<font size=4> " + head2 + "</font>|   |  \n|---|---|---|---|  \n"

	divider = "| | "
	
	col1_names, col1_links, col1_htmls = parse_links(col1)
	col2_names, col2_links, col2_htmls = parse_links(col2)
	
	html_list = col1_htmls + col2_htmls
	
	count = 0
	while count < max(len(col1), len(col2)):
		table_data =  table_data + divider
		try:
			data1 = col1_names[count] + col1_links[count]
			table_data = table_data + data1
		except:
			table_data = table_data
		try:
			data2 = col2_names[count] + col2_links[count]
			table_data = table_data + divider + data2 + "|  \n"
		except:
			table_data = table_data + divider + "|  \n"
	
		count +=1
	table_data = "---  \n" + table_data + "  \n---"
	print(""); print(table_data)
	print("")
	
	link_string = str(html_list)
	link_string = link_string.replace("[", "")
	link_string = link_string.replace("]", "")
	link_string = link_string.replace(',', " | ")
	link_string = link_string.replace('"', "")
	
	return(link_string)



# .......................LINK_MENU........................................ #


def link_menu(links_list, title=None, links_per_row=5):
	count = len(links_list)
	current = 0

	link_names, link_links, link_tags = parse_links(links_list)
	link_string = "---  \n<font size=5> " + title + "</font>  \n"
	tags_data = ""
	
	for link_item in range(count):
		if current > count:
			break
		if (current + 1) % links_per_row == 0:
			link_string = link_string + " | " + link_names[current] + link_links[current] + " | "
			link_string = link_string + "   \n" 
		else:
			link_string = link_string + " | " + link_names[current] + link_links[current]

		tags_data = tags_data + " | " + link_tags[current]
		current += 1

	link_string = link_string + "  \n---"
	print(link_string)
	print("")
	return tags_data


# .......................DISPLAY_ME........................................ #

def display_me(df, num, title, bgcolor= bgcolor, text_color=text_color):
    from IPython.core.display import HTML
    if type(df) != pd.core.frame.DataFrame:
        df = df.to_frame()
        
    head_data = "<center>" + df.head(num).to_html()
    tail_data = "<center>" + df.tail(num).to_html()
    
    print("")
    div_print(f'{title} (first {num} rows of data)', fontsize = 4,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(head_data))
    print("")
    div_print(f'{title} (last {num} rows of data)', fontsize = 4,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(tail_data))
    print("")

# .......................SAMPLE_DF....................................... #

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
    div_print(f'{title} ({num} random samples)', fontsize = 3, width=width,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(df))

# .......................CENTER....................................... #
    
def center(data, title = None, width = "auto",
             bgcolor=bgcolor, text_color=text_color):
    pd.options.display.float_format = '{:,.2f}'.format    

    if title != None:    
        div_print(f"{title}", fontsize = 4, width=width,
                 bgcolor=bgcolor, text_color=text_color)
                 
    if isinstance(data, pd.core.frame.DataFrame):
        display(HTML("<center>" + data.to_html()))
    elif isinstance(data, pd.core.series.Series):
        display(HTML("<center>" + data.to_frame().to_html()))
    else:
        div_print("Data is not the correct type.", fontsize = 4, width="30%")

# .......................LIST_TO_TABLE....................................... #
    
def list_to_table(display_list, num_cols, title, width = "auto",
                  bgcolor=bgcolor, text_color=text_color):
        
    div_print(f"{title}", fontsize = 4, width=width,
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

# .............................DIV_PRINT.......................................... #

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


# .......................OVERVIEW....................................... #

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
    
    div_print(f'{title}: Dataframe Overview', fontsize=4, 
              bgcolor=bgcolor, text_color=text_color)
    display(HTML(overview_table.format(columns, total_na, num_rows, num_cols)))
    div_print(f'{title}: Categorical Data', fontsize = 4,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(categorical_table))
    div_print(f'{title}: Numerical Data', fontsize = 4,
             bgcolor=bgcolor, text_color=text_color)
    display(HTML(numerical_table))



# .......................MISSING_VALUES....................................... #
    
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
    
    
 # ............................FANCY_PLOT....................................... #

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
    plt.tick_params(labelrotation = 40);
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


