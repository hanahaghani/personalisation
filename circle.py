from math import pi
import pandas as pd

from bokeh.models import (ColumnDataSource , Plot , Legend , AnnularWedge , LegendItem,Range1d,TabPanel,Row,Column,Slider)

def circle_tab(main_data):
     #تابع اپدیت هنگام تغییر اسلایدر 
    def update(attr,old,new):
        min_value=slider.value
        filtered_data=main_data[main_data['Going_outside']>=min_value]
        
        grouped=filtered_data['Personality'].value_counts()
        #اگر داده ای نبود خارج شو
        if grouped.sum()==0:
            return
        #ساخت دوباره نمودار
        angles=(grouped/grouped.sum()* 2*pi ).cumsum().tolist()
        start =[0] +angles[:-1]
        end=angles
        color_list=[colors.get(p,'gray') for p in grouped.index]
        
        if len(start)==len(end)==len(color_list):
            source.data=dict(
                start=start,
                end= end,
                color=color_list)
    colors={
        "Extrovert":'blue',
        "Introvert":'red'
        }    
   #خواندن یک ستون از داده 
    type_count=main_data['Personality'].value_counts(normalize=True)
    angles=(type_count* 2*pi).cumsum().tolist()
    start =[0] +angles[:-1]
    end=angles
    color_list=[colors.get(p,'gray') for p in type_count.index]
    source=ColumnDataSource(data=dict(
        start=start,
        end=end,
        color=color_list
    ))
    #ایجاد نمودار
    x=Range1d(start=-2 , end=2)
    y=Range1d(start=-2,  end=2)
    plot=Plot(x_range=x,y_range=y)
    plot.title.text=('which personality prefer being alone?')        
    #ساخت حلقه دوناتی
    glyph=AnnularWedge(x=0,y=0,inner_radius=0.9,outer_radius=1.8,start_angle='start',end_angle='end',line_color='white',line_width=3,fill_color='color')
    r=plot.add_glyph(source,glyph)
    #ساخت راهنما
    legend= Legend(location='center')
    for i ,name in enumerate(type_count.index):
        legend.items.append(LegendItem(label=name,renderers=[r],index=i))
    plot.add_layout(legend,'center')
    #ُساخت اسلایدر
    slider=Slider(start=0,end=10,value=2,step=1,title='تمایل به بیرون رفتن')
    slider.on_change('value',update)
   
        
    output=Row(Column((slider)),plot)
    return TabPanel(child=output,title='donut chart')