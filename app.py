import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Upload Whatsapp extracted chat file : ", type=["txt"])
if uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)
        # You can add further processing and visualization code here
    except Exception as e:
        st.title("Please upload a correctly extracted .txt file from Whatsapp and ensure to omit the media-files.")
        st.stop()

    # Fetch unique users
    user_list = df['User'].unique().tolist()
    user_list.remove('notification')
    user_list.sort()
    user_list.insert(0,"Total Group")
    selected_user = st.sidebar.selectbox("Select User : ",user_list)

    if st.sidebar.button("Analyze") :

        # Stats Area
        st.title("Top Stats")
        num_msgs,words,medias,links = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_msgs)
        with col2:
            st.header("Total Words")
            st.title(len(words))
        with col3:
            st.header("Total Medias")
            st.title(medias)
        with col4:
            st.header("Total Links")
            st.title(len(links))

        # Time Wise analysis
        st.title("Time vs Messages")
        time_df = helper.analyze_with_time(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(time_df['Time'],time_df['Message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # Finding Busiest Users
        if selected_user == "Total Group":
            st.title("Busy Users")
            highest, percentage_df = helper.most_busy_users(df)
            lowest = helper.least_busy_users(df)
            col1,col2 = st.columns(2)
            with col1:
                st.header("Most Busy")
                fig, axes = plt.subplots()
                axes.bar(highest.index, highest.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.header("Least Busy")
                fig, axes = plt.subplots()
                axes.bar(lowest.index, lowest.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            col1, col2 = st.columns(2)
            with col1:
                st.header("Percentages")
                st.dataframe(percentage_df)
            with col2:
                st.header('Pie Chart')
                fig, axes = plt.subplots()
                axes.pie(percentage_df.head(10).Percentage, labels=percentage_df.head(10).User, startangle=140, counterclock=False)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
        wc = helper.create_wordcloud(selected_user,df)
        fig,axes = plt.subplots()
        axes.imshow(wc)
        plt.axis('off')
        st.title("Words Used : ")
        st.pyplot(fig)

        st.title("Most Common Words : ")
        most_common_words = helper.most_commom_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_words[0], most_common_words[1])
        st.pyplot(fig)

        st.title("Emoji Analysis :")
        emjdf = helper.emoji_func(selected_user,df)
        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emjdf)
        with col2:
            fig,ax = plt.subplots()
            ax.barh(emjdf[0].head(20),emjdf[1].head(20))
            st.pyplot(fig)