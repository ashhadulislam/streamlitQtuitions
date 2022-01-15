import streamlit as st
import numpy as np
import pandas as pd
import random

import plotly.express as px
import os
from collections import Counter
import plotly.graph_objects as go


# @st.cache
def app():
    header=st.container()
    daily_data_show = st.container()
    segment_show = st.container()
    subject_show = st.container()
    week_day_show = st.container()
    top_subjects = st.container()
    footer = st.container() 


    with header:
        # st.title("Private tuition requirements in Qatar over time")
        st.subheader("Analyse and understand the tuition market")


    with daily_data_show:
        st.header("Daily advertisement analysis")
        st.subheader("Please choose the dates")
        df=pd.read_csv("data/mpt_data.csv")
        print(df.head())
        df["date_posted"]=pd.to_datetime(df["date_posted"],format="%Y-%m-%d")
        df=df.sort_values(["date_posted"])
        first_date=list(df["date_posted"])[0]
        last_date=list(df["date_posted"])[-1]

        col1, col2 = st.columns(2)        
        start_date = col1.date_input('Start date', first_date)
        end_date = col2.date_input('The final date', last_date)
        if start_date < end_date:
            pass
            # st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
        else:
            st.error('Error: End date must fall after start date.')
        
        st.subheader("Please choose the segment")
        df_dated=df[(df["date_posted"]>start_date) & (df["date_posted"]<end_date)]
        uniq_segs=["All"]
        uniq_segs.extend(list(df_dated.segment.unique()))
        # uniq_segs.append("All")
        

        segment_name=st.selectbox('Select Segment', options=uniq_segs, index = 0)
        
        if segment_name=="All":
            df_group_dates=df_dated.groupby(["date_posted"]).count().reset_index()
        else:
            df_segment=df_dated[df_dated["segment"]==segment_name]
            df_group_dates=df_segment.groupby(["date_posted"]).count().reset_index()

        fig = px.line( x=df_group_dates["date_posted"], y=df_group_dates["title"])

        fig.update_layout(
            title="Daily private tuition postings for "+segment_name,
            xaxis_title="Date",
            yaxis_title="Number of postings",
        #     legend_title="Legend Title",
        #     font=dict(
        #         family="Courier New, monospace",
        #         size=18,
        #         color="RebeccaPurple"
        #     )
        )



        st.plotly_chart(fig, use_container_width=True)

        


    with segment_show:   
        st.header("Most trending segments") 
        col1, col2 = st.columns(2)
        seg_start_date = col1.date_input('First date', start_date)
        seg_end_date = col2.date_input('End date', end_date)
        if seg_start_date < seg_end_date:
            # st.success('A Start date: `%s`\n\nEnd date:`%s`' % (seg_start_date, seg_end_date))
            pass
        else:
            st.error('Error: End date must fall after start date.')

        df_dated=df[(df["date_posted"]>seg_start_date) & (df["date_posted"]<seg_end_date)]

        df_group_segment=df_dated.groupby(["segment"]).count().reset_index()
        df_group_segment=df_group_segment.sort_values(["title"],ascending=False)
        fig = px.bar( x=df_group_segment['segment'], y=df_group_segment['title'])

        fig.update_layout(
            title="Popularity of Different Segments",
            xaxis_title="Segment Name",
            yaxis_title="Number of postings in last 60 days",
        #     legend_title="Legend Title",
        #     font=dict(
        #         family="Courier New, monospace",
        #         size=18,
        #         color="RebeccaPurple"
        #     )
        )
        st.plotly_chart(fig, use_container_width=True)

        
      

        
    with subject_show:

        st.header("Most trending subjects for top segments") 
        st.subheader("Top trending segments and their subjects")
        col1, col2 = st.columns(2)        
        segsub_start_date = col1.date_input('Start', seg_start_date)
        segsub_end_date = col2.date_input('Last date',seg_end_date)
        if segsub_start_date < segsub_end_date:
            # st.success('The Start date: `%s`\n\nEnd date:`%s`' % (segsub_start_date, segsub_end_date))
            pass
        else:
            st.error('Error: End date must fall after start date.')

        df_dated=df[(df["date_posted"]>segsub_start_date) & (df["date_posted"]<segsub_end_date)]

        df_group_segment=df_dated.groupby(["segment"]).count().reset_index()
        df_group_segment=df_group_segment.sort_values(["title"],ascending=False)
        uniq_segments_ordered=list(df_group_segment["segment"])
        count_segments=st.selectbox("Number of top segments", [i for i in range(1,len(uniq_segments_ordered))],index=0)
        uniq_segments_ordered=uniq_segments_ordered[:count_segments]
        rank_count=1
        for uniq_segment in uniq_segments_ordered:

            df_segment_wise=df_dated[df_dated["segment"]==uniq_segment]
        #     print(df_segment_wise.head())
            df_segment_wise_group_subject=df_segment_wise.groupby(["subject"]).count().reset_index()
            df_segment_wise_group_subject=df_segment_wise_group_subject.sort_values(["title"],ascending=False)
            

            


        #     fig = px.bar(df_segment_wise_group_subject, x='subject', y='title')
            fig = px.bar(x=df_segment_wise_group_subject['subject'], y=df_segment_wise_group_subject['title'])    

            fig.update_layout(
                title="#"+str(rank_count)+": "+str(uniq_segment),
                xaxis_title="Subject Name",
                yaxis_title="Number of postings in last 60 days",
            #     legend_title="Legend Title",
            #     font=dict(
            #         family="Courier New, monospace",
            #         size=18,
            #         color="RebeccaPurple"
            #     )
            )
            
            uniq_segment=uniq_segment.replace("/","")
            print(uniq_segment)
            

            
            st.plotly_chart(fig, use_container_width=True)
            print("Plotted")
            rank_count+=1
        


    with week_day_show:
        st.header("Advertisements every day of the week") 
        st.subheader("Advertisements made in different weekdays")
        col1, col2 = st.columns(2)        
        weekday_start_date = col1.date_input('Beginning', segsub_start_date)
        weekday_end_date = col2.date_input('The End date',segsub_end_date)
        if weekday_start_date < weekday_end_date:
            # st.success('Start date: `%s`\n\nEnd date:`%s`' % (segsub_start_date, segsub_end_date))
            pass
        else:
            st.error('Error: End date must fall after start date.')

        df_dated=df[(df["date_posted"]>weekday_start_date) & (df["date_posted"]<weekday_end_date)]
        df_dated["day"]=df_dated["date_posted"].dt.dayofweek
        df_group_days=df_dated.groupby(["day"]).count().reset_index()
        dict_num_days={
            0:"Mon",
            1:"Tues",
            2:"Wed",
            3:"Thurs",    
            4:"Fri",    
            5:"Sat",    
            6:"Sun",    
            
        }
        df_group_days["day"]=df_group_days["day"].replace(dict_num_days)

        fig = px.line(df_group_days, x="day", y="title")

        fig.update_layout(
            title="Postings by day of week",
            xaxis_title="Day",
            yaxis_title="Number of postings",
        #     legend_title="Legend Title",
        #     font=dict(
        #         family="Courier New, monospace",
        #         size=18,
        #         color="RebeccaPurple"
        #     )
        )
        st.plotly_chart(fig, use_container_width=True)
        

    with top_subjects:
        st.header("Ranking of individual subjects") 
        st.subheader("Based on the count of advertisements")
        col1, col2 = st.columns(2)        
        ranking_sub_start_date = col1.date_input('Date Start', weekday_start_date)
        ranking_sub_end_date = col2.date_input('Date End',weekday_end_date)
        if ranking_sub_start_date < ranking_sub_end_date:
            # st.success('Start date: `%s`\n\nEnd date:`%s`' % (segsub_start_date, segsub_end_date))
            pass
        else:
            st.error('Error: End date must fall after start date.')

        df_dated=df[(df["date_posted"]>ranking_sub_start_date) & (df["date_posted"]<ranking_sub_end_date)]
        all_subjects=[]
        for subj in list(df.subject):
            if subj=="MATHS":
                subj="Mathematics"
            all_subjects.append(subj)
        counter_subjects=Counter(all_subjects)
        sorted_counter_subjects={k: v for k, v in sorted(counter_subjects.items(), 
                key=lambda item: item[1],reverse=True)}    
        top_count=st.selectbox("Number of top subjects", [i for i in range(1,len(list(sorted_counter_subjects.keys())))],index=5)
        colors=[]
        col1=random.uniform(0,1)
        col2=random.uniform(col1,col1+0.05)
        for i in range(top_count):
            newcolor=random.uniform(col1,col2)    
            colors.append(newcolor)
            col1=newcolor
            col2=newcolor+0.05
            
            
        top_subjects=list(sorted_counter_subjects.keys())[:top_count]
        top_subject_counts=list(sorted_counter_subjects.values())[:top_count]
        print("Colors are ",colors)    

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_subjects,
            y=top_subject_counts,
            marker_color=colors
        ))

        fig.update_layout(
            title="Top "+str(top_count)+" subjects by advertisement count",
            xaxis_title="Subject",
            yaxis_title="Count Of Advertisements",
        #     legend_title="Legend Title",
        #     font=dict(
        #         family="Courier New, monospace",
        #         size=18,
        #         color="RebeccaPurple"
        #     )
        )
        st.plotly_chart(fig, use_container_width=True)


    with footer:
        st.header("Read the detailed discussion on ")
        st.write("Medium](https://ashhadulislam.medium.com/freelance-tutoring-in-qatar-33a27bee1403)")

