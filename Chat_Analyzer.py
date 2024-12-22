import streamlit as st
import Processor, info
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

# Add the file uploader to the sidebar
uploaded_files = st.sidebar.file_uploader(
    "Choose a CSV file", accept_multiple_files=True
)

# Loop through each uploaded file and display information in the sidebar
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.getvalue()
    st.sidebar.write("**Filename:**", uploaded_file.name)
    data = bytes_data.decode('utf-8')
    df = Processor.Processor(data)

    # Fetching all Unique Users for the drop-down menu
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "OverAll")
    selected_user = st.sidebar.selectbox("Show Analysis WRT", user_list)

    if st.sidebar.button("Show Analysis"):
        # Fetch statistics
        num_messages, words, num_media_messages, links = info.fetch_stats(selected_user, df)
        st.title('Stats for the WhatsApp Chat')

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages:")
            st.title(num_messages)

        with col2:
            st.header("Total Words:")
            st.title(words)

        with col3:
            st.header("Total Media Shared:")
            st.title(num_media_messages)

        with col4:
            st.header("Total Links Shared:")
            st.title(links)

        # Monthly timeline
        st.title("Monthly Timeline")
        timeline = info.monthly_timeline(selected_user, df)
        if timeline.empty:
            st.warning("No data available for the monthly timeline.")
        else:
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = info.daily_timeline(selected_user, df)
        if daily_timeline.empty:
            st.warning("No data available for the daily timeline.")
        else:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = info.week_activity_map(selected_user, df)
            if busy_day.empty:
                st.warning("No data available for the weekly activity map.")
            else:
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = info.month_activity_map(selected_user, df)
            if busy_month.empty:
                st.warning("No data available for the monthly activity map.")
            else:
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

        # Weekly Activity Map
        st.title("Weekly Activity Map (Heatmap)")

        # Generate the heatmap data
        user_heatmap = info.activity_heatmap(selected_user, df)

        # Validate the heatmap data
        if user_heatmap.empty:
            st.warning("No data available for the activity heatmap.")
        else:
            # Customize and plot the heatmap
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.heatmap(
                user_heatmap,
                cmap='coolwarm',   # Color palette for visual appeal
                annot=True,        # Display values in the heatmap cells
                fmt='g',           # Format for displaying values
                linewidths=0.5,    # Line width between cells
                linecolor='gray',  # Color for the grid lines
                cbar_kws={'label': 'Message Count'},  # Colorbar label
                ax=ax
            )
            ax.set_title("Activity Heatmap", fontsize=16, fontweight='bold')
            ax.set_xlabel("Hour of the Day", fontsize=12)
            ax.set_ylabel("Day of the Week", fontsize=12)
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
            plt.yticks(rotation=0)   # Keep y-axis labels horizontal
            st.pyplot(fig)


        # Most Engaged User of the Chat
        if selected_user == 'OverAll':
            st.title('Most Engaged User')
            x, new_df = info.Most_Engaged_User(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='maroon')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.title('WordCloud:')
        df_wc = info.creating_worldCloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Commonly Used Words
        most_common_df = info.commonly_used_words(selected_user, df)
        if not most_common_df.empty:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1], color='maroon')
            plt.xticks(rotation='vertical')
            st.title('Commonly Used Words')
            st.pyplot(fig)

        # Emoji Analysis
        emoji_df = info.emoji_analysis(selected_user, df)
        if not emoji_df.empty:
            st.title("Emoji Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)
