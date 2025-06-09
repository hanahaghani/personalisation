from bokeh.models import TabPanel
from bokeh.plotting import figure
from bokeh.palettes import Category10
import pandas as pd
def scatter_tab(main_data):
    #ساخت نمودار
    plot=figure(width=800,height=500,title='scatter plot')
    # ذخیره اطلاعات
    type=main_data['Personality'].unique()
    #رنگ بندی تایپ شخصیت ها
    color= Category10[10]
    #ساخت نوع دقیق نمودار
    for i ,t in enumerate(type):
        df=main_data[main_data['Personality']==t]
        plot.scatter(df['Friends_circle_size'],df['Time_spent_Alone'],
                     alpha=.6,size=13,
                     color=color[i%len(color)],
                     legend_label=t)
    #ساخت راهنما
    plot.legend.title='شخصیت'
    plot.legend.location='top_right'
    
    
    return TabPanel(child=plot,title='scatter plot')