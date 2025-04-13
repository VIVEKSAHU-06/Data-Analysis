# Use virtual environment with older versions of python like 3.7

# need to install streamlit when restart the VS code in venv 

# command to run streamlit - python -m streamlit run app.py

import preprocessor, helper
import streamlit as st 
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    # st.text(data)
    
    df = preprocessor.preprocess(data)
    
    st.dataframe(df)
    
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)
    
    if st.sidebar.button("Show Analysis"):
        
        # Stats area
        num_messages,words,num_media,num_links =   helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
            
        with col2:
            st.header("Total Words")
            st.title(words) 
        
        with col3:
            st.header("Media shared")
            st.title(num_media)
        
        with col4:
            st.header("Links shared")
            st.title(num_links)
    
        #Timeline
        #Monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # Activity map
        st.title("Activity map")
        col1,col2 = st.columns(2)
        
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        # Heatmap
        st.title("Weekly activity map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, cmap="YlGnBu", linewidths=0.5)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
         
        # Finding the busiest user in the group
        if selected_user == 'Overall':
            st.title("Most busy user")
            
            x,new_df = helper.most_busy_users(df)
            fig,ax = plt.subplots()
            
            col1,col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
            
        # wordcloud
        df_wc= helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)
        
        # Emoji analysis
        emoji_df = helper.create_emoji(selected_user,df)
        st.title("Emoji analysis")
        
        col1,col2 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
        
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(8),labels=emoji_df[0].head(8),autopct="%0.2f",startangle=90)
            st.pyplot(fig)

