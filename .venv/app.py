import helper
import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    user_list= df['User'].unique().tolist()
    user_list.sort()
    user_list.remove('Group Notification')
    user_list.insert(0,'Overall')

    selected_user=st.sidebar.selectbox("Select analysis with respect to",user_list)

    if st.sidebar.button('Analyze'):
        num_messages, num_words, num_mm, num_links= helper.fetchstats(selected_user, df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Total Media Shared")
            st.title(num_mm)

        with col4:
            st.header("Total Links Shared")
            st.title(num_links)

    if selected_user=='Overall':
        st.title('Most Active Users')
        x,new_df=helper.most_active_users(df)
        fig, ax = plt.subplots()
        col1,col2=st.columns(2)

        with col1:
            ax.bar(x.index,x.values)
            plt.xticks(rotation=90)
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    df_wc=helper.create_wc(selected_user, df)
    fig,ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    mw_df=helper.most_common_words(selected_user, df)
    st.title('Most Common Words')
    st.dataframe(mw_df)

    st.title('Most Common Words Graph')
    fig,ax = plt.subplots()
    ax.barh(mw_df[0],mw_df[1])
    st.pyplot(fig)

    me_df=helper.analyze_emoji(selected_user, df)
    st.title('Most Common Emoji')
    col1,col2=st.columns(2)
    with col1:
        st.dataframe(me_df)
    with col2:
        fig,ax=plt.subplots()
        ax.pie(me_df[1],labels=me_df[0],autopct='%0.2f')
        st.pyplot(fig)

    timeline=helper.monthly_timeline(selected_user, df)
    st.title('Monthly Timeline')
    fig,ax = plt.subplots()
    ax.plot(timeline['time'],timeline['Message'])
    plt.xticks(rotation=90)
    st.pyplot(fig)

    week=helper.week_map(selected_user, df)
    week_df=week.reset_index()
    week_df.columns = ['Day', 'Count']

    st.title('Weekly Timeline')
    st.dataframe(week)
    fig,ax = plt.subplots()
    ax.plot(week_df['Day'], week_df['Count'], marker='o')
    st.pyplot(fig)

