import numpy as np
from bokeh.models import Row,Column,ColumnDataSource,Slider,CheckboxGroup,TabPanel,RangeSlider
from bokeh.palettes import Category10
from bokeh.plotting import figure

def hist_tab(main_data):
    #ساخت هیستوگرام
    def make_dataset(selected_types,friend_range_start=0,friend_range_end=15,bin_value=10):
        source_info=[]
        filtered=main_data[
            (main_data['Personality'].isin(selected_types))&
            (main_data['Friends_circle_size']>=friend_range_start)&
            (main_data['Friends_circle_size']<=friend_range_end)
        ]
        color=Category10[10]
        for i,personality in enumerate(selected_types):
            sub_dataframe=filtered[filtered['Personality']==personality]
            count,edges=np.histogram(sub_dataframe['Friends_circle_size'],bins=bin_value)
            
            source=ColumnDataSource(data=dict(
                top=count,
                left=edges[:-1],
                right=edges[1:]
            ))
            
            source_info.append({
                'source':source,
                'Personality':personality,
                'color':color[i % len(color)]
            })
        return source_info
    #طراحی هیستوگرام
    def hist_plot(source_info):
        p=figure(width=800,height=500,title="تعداد دوست به تفکیک شخصیت")
        for item in source_info:
            p.quad(
                fill_alpha=.6,
                top='top',left='left',right='right',bottom=0,
                source=item['source'],
                fill_color=item['color'],
                legend_label=item['Personality']
                )
            p.legend.title="نوع شخصیت"
            p.legend.location="top_right"
        return p
    #ایجاد تغییرات توسط کاربر
    def update(attr,old,new):
        checked=[chbox.labels[i] for i in chbox.active]
        dataset=make_dataset(checked,friend_range_start=rangeslider.value[0],friend_range_end=rangeslider.value[1] ,bin_value=slider.value)
        #پاک کردن نمودار قبلی
        plot.renderers=[]
        #رسم دوباره نمودار
        for item in dataset:
            plot.quad(
                fill_alpha=.6,
                top='top',left='left',right='right',bottom=0,
                source=item['source'],
                fill_color=item['color'],
                legend_label=item['Personality']
                )
       
    #ذخیره اطلاعات
    type_count=sorted(list(set(main_data['Personality'])))
    #ساخت دکمه و اسلایدر
    chbox=CheckboxGroup(labels=type_count,active=[0,1])
    slider=Slider(start=1,end=30,step=2,value=10,title='دانه بندی هیستوگرام')
    rangeslider=RangeSlider(start=0,end=15,step=1,value=(3,8),title='تعداد دوست')
    #شرط  برای اسلایدر 
    init_data=[chbox.labels[i] for i in chbox.active]
    source_info=make_dataset(init_data,friend_range_start=rangeslider.value[0],friend_range_end=rangeslider.value[1],bin_value=slider.value)
    plot=hist_plot(source_info)
    #فعال سازی دکمه و اسلایدر
    chbox.on_change('active',update)
    slider.on_change('value',update)
    rangeslider.on_change('value',update)
    #نمای خروجی
    layout=Row(Column(chbox,slider,rangeslider),plot)
    return TabPanel(child=layout,title="histogram chart")