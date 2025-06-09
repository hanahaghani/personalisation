import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.models import Tabs
from circle import circle_tab
from hist import hist_tab
from scatter import scatter_tab

main_data=pd.read_csv('personality_dataset.csv').dropna().drop_duplicates()

tab_circle=circle_tab(main_data)
tab_hist=hist_tab(main_data)
tab_scatter=scatter_tab(main_data)

tabs=Tabs(tabs=[tab_circle,tab_hist,tab_scatter])

curdoc().add_root(tabs)