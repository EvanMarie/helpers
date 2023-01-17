import pandas as pd
import numpy as np
import matplotlib as mpl
from IPython.core.display import HTML
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:,.2f}'.format

bgcolor = '#333333';
text_color = 'white'
innerbackcolor = "#222222";
outerbackcolor = "#333333";
fontcolor = "white"

favorite_cmaps = ['cool', 'autumn', 'autumn_r', 'Set2_r', 'cool_r',
                  'gist_rainbow', 'prism', 'rainbow', 'spring']


# FUNCTIONS: d, p, sp, table_of_contents, display_me, sample_df, see,
#	     list_to_table, div_print, overview, missing_values, fancy_plot

# .......................IMPORTS....................................... #
def pd_np_mpl_import():
    global pd
    global np
    global plt
    global reload

    pd = __import__('pandas', globals(), locals())
    np = __import__('numpy', globals(), locals())
    matplotlib = __import__('matplotlib', globals(), locals())
    plt = matplotlib.pyplot
    importlib = __import__('importlib', globals(), locals())
    reload = importlib.reload


def url_import():
    global urlretrieve
    urllib = __import__('urllib', globals(), locals())
    urlretrieve = urllib.request.urlretrieve

def yf_import():
    global yf
    yf = __import__('yfinance', globals(), locals())


def import_all():
    pd_np_mpl_import()
    url_import()
    yf_import()


# ......................TINY_GUYS....................................... #

def sp(): print('');


def p(x): print(x); sp()


def d(x): display(x); sp()


def pretty(input, label=None, fontsize=3, bgcolor='#444444',
           textcolor="white", width=None
           ):
    from IPython.display import HTML
    input = str(input)

    def get_color(color):
        label_font = [x - 3 for x in [int(num) for num in color[1:]]]
        label_font = "#" + "".join(str(x) for x in label_font)
        return label_font

    if label != None:
        label_font = get_color(bgcolor)
        pretty(label, fontsize=fontsize, bgcolor='#ececec',
               textcolor=label_font, width=width, label=None)

    display(HTML("<span style = 'line-height: 1.5; \
                                background: {}; width: {}; \
                                border: 1px solid text_color;\
                                border-radius: 0px; text-align: center;\
                                padding: 5px;'>\
                                <b><font size={}><text style=color:{}>{}\
                                </text></font></b></style>".format(bgcolor, width,
                                                                   fontsize,
                                                                   textcolor, input)))


def div_print(text, width='auto', bgcolor=bgcolor, text_color=text_color,
              fontsize=2
              ):
    from IPython.display import HTML as html_print

    if width == 'auto':
        font_calc = {6: 2.75, 5: 2.5, 4: 2.5, 3: 3, 2: 4}
        width = str(len(text) * fontsize * font_calc[fontsize]) + "px"

    else:
        if type(width) != str:
            width = str(width)
        if width[-1] == "x":
            width = width
        elif width[-1] != '%':
            width = width + "px"

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

# .......................Time Stamp Converter....................................... #
# Write a function to convert any column in a df that is a timestamp
# to date, hour, and min only
# Find columns that dtype is timestamp
def time_stamp_converter(df):
    def find_timestamp(df):
        timestamp_cols = []
        for col in df.columns:
            if df[col].dtype.name.startswith('datetime64'):
                timestamp_cols.append(col)
        return timestamp_cols
    timestamp_cols = find_timestamp(df)
    for col in timestamp_cols:
        df[col] = df[col].dt.strftime('%Y-%m-%d')
    return df

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


def table_of_contents(title='', head1=None, head2=None, col1=[], col2=[]):
    from IPython.display import HTML
    table_data = "<center><font size=6> " + title + "</font></center>  \n  \n|<font size=4> " + head1 + "|   |<font size=4> " + head2 + "</font>|   |  \n|---|---|---|---|  \n"

    divider = "| | "

    col1_names, col1_links, col1_htmls = parse_links(col1)
    col2_names, col2_links, col2_htmls = parse_links(col2)

    html_list = col1_htmls + col2_htmls

    count = 0
    while count < max(len(col1), len(col2)):
        table_data = table_data + divider
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

        count += 1
    table_data = "---  \n" + table_data + "  \n---"
    print("");
    print(table_data)
    print("")

    link_string = str(html_list)
    link_string = link_string.replace("[", "")
    link_string = link_string.replace("]", "")
    link_string = link_string.replace(',', " | ")
    link_string = link_string.replace('"', "")

    return (link_string)


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
def head_tail_vert(df, num, title, bgcolor=bgcolor,
                    text_color=text_color, fontsize=4,
                    intraday=False):
    from IPython.core.display import HTML

    if type(df) != pd.core.frame.DataFrame:
        df = df.copy().to_frame()

    if not intraday:
        df = time_stamp_converter(df.copy())
        if df.index.dtype.name.startswith('datetime64'):
            df.index = df.index.strftime('%Y-%m-%d')
            # df.index = df.index.date

    head_data = "<center>" + df.head(num).to_html()
    tail_data = "<center>" + df.tail(num).to_html()

    print("")
    div_print(f'{title}: head({num})', fontsize=fontsize,
              bgcolor=bgcolor, text_color=text_color)
    display(HTML(head_data))
    print("")
    div_print(f'{title}: tail({num})', fontsize=fontsize,
              bgcolor=bgcolor, text_color=text_color)
    display(HTML(tail_data))
    print("")

def head_tail_horz(df, num, title, bgcolor=bgcolor,
                   text_color=text_color, precision=2,
                   intraday=False, title_fontsize=4,
                   table_fontsize="12px"):

    if not intraday:
        df = time_stamp_converter(df.copy())
        if df.index.dtype.name.startswith('datetime64'):
            df.index = df.index.strftime('%Y-%m-%d')
            # df.index = df.index.date

    div_print(f'{title}', fontsize=title_fontsize,
              bgcolor=bgcolor, text_color=text_color)
    multi([(df.head(num),f"head({num})"),
           (df.tail(num),f"tail({num})")],
          fontsize=table_fontsize, precision=precision,
          intraday=intraday)

# .......................SAMPLE_DF....................................... #

def sample_df(data, num, title, width="auto",
              bgcolor=bgcolor, text_color=text_color
              ):
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
    div_print(f'{title} ({num} random samples)', fontsize=3, width=width,
              bgcolor=bgcolor, text_color=text_color)
    display(HTML(df))


# .......................SEE....................................... #

def see(data, title=None, width="auto", fontsize=4,
        bgcolor=bgcolor, text_color=text_color,
        intraday=False):

    pd.options.display.float_format = '{:,.2f}'.format

    if title != None:
        div_print(f"{title}", fontsize=fontsize, width=width,
                  bgcolor=bgcolor, text_color=text_color)

    if isinstance(data, pd.core.frame.DataFrame):
        if not intraday:
            data = time_stamp_converter(data.copy())
            if data.index.dtype.name.startswith('datetime64'):
                data.index = data.index.strftime('%Y-%m-%d')
                # data.index = data.index.date

        display(HTML("<center>" + data.to_html()));
        sp()
    elif isinstance(data, pd.core.series.Series):
        if data.index.dtype.name.startswith('datetime64'):
            data.index = data.index.strftime('%Y-%m-%d')
            # data.index = data.index.date
        display(HTML("<center>" + data.to_frame().to_html()));
        sp()
    else:
        try:
            display(HTML("<center>" + data.to_frame().to_html()));
            sp()
        except:
            pretty(data, title);
            sp()


# .......................FORCE_DF....................................... #
def date_only(data, intraday=False):
    if intraday == False:
        if data.index.dtype == 'datetime64[ns]':
            data.index = data.index.strftime('%Y-%m-%d')
            # data.index = data.index.date
            return data
        else:
            return data
    else:
        return data


def force_df(data, intraday=False):
    if isinstance(data, pd.core.series.Series):
        return date_only(data, intraday=intraday).to_frame()
    elif isinstance(data, pd.core.frame.DataFrame):
        return date_only(data, intraday=intraday)
    else:
        try:
            return pd.Series(data).to_frame()
        except:
            return div_print("The data cannot be displayed.")



# .......................MULTI....................................... #

def multi(data_list, fontsize='15px', precision=2, intraday=False):
    from IPython.display import display_html

    caption_style = [{
        'selector': 'caption',
        'props': [
            ('background', bgcolor),
            ('border-radius', '3px'),
            ('padding', '5px'),
            ('color', text_color),
            ('font-size', fontsize),
            ('font-weight', 'bold')]}]

    # header_style = [
    #     {'selector': 'thead',
    #      'props': []},
    #     {'selector': 'th.col_heading',
    #      'props': []},
    #     {'selector': '.index_name',
    #      'props': []}, ]

    thousands = ",";
    spaces = "&nbsp;&nbsp;&nbsp;"
    table_styling = caption_style  # + header_style

    stylers = []
    for idx, pair in enumerate(data_list):
        if len(pair) == 2:
            table_attribute_string = "style='display:inline-block'"
        elif pair[2] == 'center':
            table_attribute_string = "style='display:inline-grid'"
        styler = force_df(data_list[idx][0], intraday=intraday).style \
            .set_caption(data_list[idx][1]) \
            .set_table_attributes(table_attribute_string) \
            .set_table_styles(table_styling).format(precision=precision,
                                                    thousands=thousands)
        stylers.append(styler)

    if len(stylers) == 1:
        display_html('<center>' + stylers[0]._repr_html_(), raw=True); sp();
    elif len(stylers) == 2:
        display_html('<center>' + stylers[0]._repr_html_() + spaces + stylers[1]._repr_html_() + spaces, raw=True); sp();
    elif len(stylers) == 3:
        display_html('<center>' + stylers[0]._repr_html_() + spaces + stylers[1]._repr_html_() + spaces + stylers[
            2]._repr_html_() + spaces, raw=True); sp();
    elif len(stylers) == 4:
        display_html('<center>' + stylers[0]._repr_html_() + spaces + stylers[1]._repr_html_() + spaces + stylers[
            2]._repr_html_() + spaces + stylers[3]._repr_html_() + spaces, raw=True); sp();

# .......................LIST_TO_TABLE....................................... #

def list_to_table(display_list, num_cols, title, width="auto",
                  bgcolor=bgcolor, text_color=text_color
                  ):
    div_print(f"{title}", fontsize=4, width=width,
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


# .......................OVERVIEW....................................... #

def overview(df, title=None, bgcolor=bgcolor, text_color=text_color):
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
    div_print(f'{title}: Categorical Data', fontsize=4,
              bgcolor=bgcolor, text_color=text_color)
    display(HTML(categorical_table))
    div_print(f'{title}: Numerical Data', fontsize=4,
              bgcolor=bgcolor, text_color=text_color)
    display(HTML(numerical_table))


# .......................MISSING_VALUES....................................... #

def missing_values(df, bgcolor=bgcolor, text_color=text_color):
    from IPython.display import HTML
    pd.options.display.float_format = '{:,.0f}'.format
    missing_log = []
    for column in df.columns:
        missing_values = df[column].isna().sum()
        missing_log.append([column, missing_values])
    missing = pd.DataFrame(missing_log, columns=['column name', 'missing'])
    div_print(f'Columns and Missing Values', fontsize=3, width="38%",
              bgcolor=bgcolor, text_color=text_color)
    missing = "<center>" + missing.to_html()
    display(HTML(missing))


# ............................FANCY_PLOT....................................... #

def fancy_plot(data, kind="line", title=None, legend_loc='upper right',
               xlabel=None, ylabel=None, logy=False, outerbackcolor=outerbackcolor,
               innerbackcolor=innerbackcolor, fontcolor=fontcolor, cmap='cool',
               label_rot=None
               ):
    import random
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    mpl.rcParams['xtick.color'] = outerbackcolor
    mpl.rcParams['ytick.color'] = outerbackcolor
    mpl.rcParams['font.family'] = 'monospace'
    fig = plt.subplots(facecolor=outerbackcolor, figsize=(13, 7))
    ax = plt.axes();
    if kind == 'line':
        data.plot(kind='line', ax=ax, rot=label_rot, cmap=cmap, logy=logy)
    else:
        data.plot(kind=kind, ax=ax, rot=label_rot, cmap=cmap, logy=logy);
    plt.style.use("ggplot");
    ax.set_facecolor(innerbackcolor)
    ax.grid(color=fontcolor, linestyle=':', linewidth=0.75, alpha=0.75)
    plt.tick_params(labelrotation=40);
    plt.title(title, fontsize=23, pad=20, color=fontcolor);
    plt.ylabel(ylabel, fontsize=18, color=fontcolor);
    plt.xlabel(xlabel, fontsize=18, color=fontcolor);
    plt.xticks(fontsize=10, color=fontcolor)
    plt.yticks(fontsize=10, color=fontcolor)
    if legend_loc is None:
        ax.get_legend().remove()
    else:
        plt.legend(labels=data.columns, fontsize=15, loc=legend_loc,
                   facecolor=outerbackcolor, labelcolor=fontcolor)


# ****************************MINI-PLOT********************************** #
def mini_plot(df, title, ylabel=None, xlabel=None, cmap='cool', kind='line',
              label_rot=None, logy=False, legend_loc=2
              ):
    mpl.rcParams['xtick.color'] = text_color
    mpl.rcParams['ytick.color'] = text_color
    mpl.rcParams['font.family'] = 'monospace'
    fig, ax1 = plt.subplots(figsize=(13, 7), facecolor=outerbackcolor)

    if kind == 'line':
        df.plot(kind='line', ax=ax1, rot=label_rot, cmap=cmap, logy=logy)
    else:
        df.plot(ax=ax1, kind=kind, rot=label_rot, cmap=cmap, logy=logy)
    plt.title(title, color=text_color, size=20, pad=20)
    ax1.grid(color='LightGray', linestyle=':', linewidth=0.5, which='major', axis='both')

    plt.xticks()
    ax1.set_ylabel(ylabel, color=text_color)
    ax1.set_xlabel(xlabel, color=text_color)
    plt.style.use("ggplot");
    ax1.set_facecolor(innerbackcolor)
    if legend_loc is None:
        ax.get_legend().remove()
    else:
        plt.legend(labels=df.columns, fontsize=15, loc=legend_loc,
                   facecolor=outerbackcolor, labelcolor=text_color)
    plt.show()


# ****************************PLOT-BY-DF********************************** #

def plot_by_df(df, sort_param, title, fontsize = 4, num_records=12,
               ylabel=None, xlabel=None, cmap='cool', kind='line',
               label_rot=None, logy=False, legend_loc=2, precision=2,
               thousands=",", intraday=False):
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import ipywidgets as widgets
    from ipywidgets import GridspecLayout

    if not intraday:
        df = time_stamp_converter(df.copy())
        if df.index.dtype.name.startswith('datetime64'):
            df.index = df.index.strftime('%Y-%m-%d')
            # df.index = df.index.date

    out_box1 = widgets.Output(layout={"border": "1px solid black"})
    out_box2 = widgets.Output(layout={"border": "1px solid black"})

    heading_properties = [('font-size', '11px')]
    cell_properties = [('font-size', '11px')]

    dfstyle = [dict(selector="th", props=heading_properties), \
               dict(selector="td", props=cell_properties)]

    with out_box1:
        display(date_only(df.sample(num_records).sort_values(sort_param)).style \
                .format(precision=precision, thousands=thousands) \
                .set_table_styles(dfstyle))

    with out_box2:
        mini_plot(df, title, ylabel=ylabel, xlabel=xlabel, cmap=cmap, kind=kind,
                  label_rot=label_rot, logy=logy, legend_loc=legend_loc)

    grid = GridspecLayout(20, 8)
    grid[:, 0] = out_box1
    grid[:, 1:20] = out_box2
    div_print(f"{title} ({num_records} samples & overall plot)", fontsize=fontsize)
    display(grid)


# *************************MULTI-PLOT-By-DF************************************* #
# MUST PASS list of lists to this function
# [[df, title], [df, title], [df, title], [df, title]]

def multi_plot_by_df(data_list, title, xlabel=None, ylabel=None,
                     legend_loc=2, cmap='cool', num_records=12,
                     sort_param=None, fontsize=3, precision=2, thousands=","):

    div_print(title, fontsize=5)

    for pair in data_list:
        plot_by_df(pair[0], title=pair[1], xlabel=xlabel, fontsize=fontsize,
                   ylabel=ylabel, legend_loc=legend_loc, cmap=cmap,
                   num_records=num_records, sort_param=sort_param,
                   precision=precision, thousands=thousands);sp();

    sp(); sp();
# ************************************************************************************ #

# .......................OUTDATED and Replaced by Multi....................................... #

def seehorz(data_list, title_list, fontsize='15px', precision=2,
            display='inline-block', intraday=False
            ):
    from IPython.display import display_html

    caption_style = [{
        'selector': 'caption',
        'props': [
            ('background', bgcolor),
            ('border-radius', '3px'),
            ('padding', '5px'),
            ('color', text_color),
            ('font-size', fontsize),
            ('font-weight', 'bold')]}]

    header_style = [
        {'selector': 'thead',
         'props': []},
        {'selector': 'th.col_heading',
         'props': []},
        {'selector': '.index_name',
         'props': []}, ]

    thousands = ","
    spaces = "&nbsp;&nbsp;&nbsp;"
    table_attribute_string = "style='display: " + display + "'"

    table_styling = caption_style + header_style

    if len(data_list) == 2:
        styler01 = force_df(data_list[0], intraday=intraday).style \
            .set_table_attributes(table_attribute_string) \
            .set_caption(title_list[0]) \
            .set_table_styles(table_styling).format(precision=precision,
                                                    thousands=thousands)

        styler02 = force_df(data_list[1], intraday=intraday).style \
            .set_table_attributes(table_attribute_string) \
            .set_caption(title_list[1]) \
            .set_table_styles(table_styling).format(precision=precision,
                                                    thousands=thousands)
        # display_html(styler01)
        display_html('<center>' + styler01._repr_html_() + spaces + styler02._repr_html_(), raw=True)
        sp();
        sp()

    elif len(data_list) == 3:
        styler01 = force_df(data_list[0], intraday=intraday).style \
            .set_table_attributes(table_attribute_string) \
            .set_caption(title_list[0]) \
            .set_table_styles(caption_style).format(precision=precision,
                                                    thousands=thousands)
        styler02 = force_df(data_list[1], intraday=intraday).style \
            .set_table_attributes(table_attribute_string) \
            .set_caption(title_list[1]) \
            .set_table_styles(caption_style).format(precision=precision,
                                                    thousands=thousands)
        styler03 = force_df(data_list[2], intraday=intraday).style \
            .set_table_attributes(table_attribute_string) \
            .set_caption(title_list[2]) \
            .set_table_styles(caption_style).format(precision=precision,
                                                    thousands=thousands)
        display_html('<center>' + styler01._repr_html_() + spaces \
                     + styler02._repr_html_() + spaces \
                     + styler03._repr_html_(), raw=True)
        sp();
        sp()

    elif len(data_list) == 4:
        styler01 = force_df(data_list[0], intraday=intraday).style \
            .set_table_attributes(table_attribute_string) \
            .set_caption(title_list[0]) \
            .set_table_styles(caption_style).format(precision=precision)
        styler02 = force_df(data_list[1], intraday=intraday).style \
            .set_table_attributes(table_attribute_string) \
            .set_caption(title_list[1]) \
            .set_table_styles(caption_style).format(precision=precision)
        styler03 = force_df(data_list[2], intraday=intraday).style \
            .set_table_attributes(table_attribute_string) \
            .set_caption(title_list[2]) \
            .set_table_styles(caption_style).format(precision=precision)
        styler04 = force_df(data_list[3], intraday=intraday).style \
            .set_table_attributes(table_attribute_string) \
            .set_caption(title_list[3]) \
            .set_table_styles(caption_style).format(precision=precision)
        display_html('<center>' + styler01._repr_html_() + spaces + \
                     styler02._repr_html_() + spaces + \
                     styler03._repr_html_() + spaces + \
                     styler04._repr_html_(), raw=True)
        sp()
        sp()


# set the dt.strftime format for the index to be just the date
def set_date_format(df):
    df.index = df.index.strftime('%Y-%m-%d')
    return df

