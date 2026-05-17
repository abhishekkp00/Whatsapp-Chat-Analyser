import streamlit as st
import preprocessor
import helper

import plotly.express as px
import plotly.graph_objects as go
import zipfile
import os
import tempfile
 

# Configure Streamlit page
st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon="💬", layout="wide")

def extract_and_find_chat(zip_file):
    """Extract zip file and find WhatsApp chat export files."""
    try:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Extract zip file
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find all .txt files that might be chat exports
        chat_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    chat_files.append(file_path)
        
        return temp_dir, chat_files
    except zipfile.BadZipFile:
        return None, []
    except Exception as e:
        st.error(f"Error extracting zip: {str(e)}")
        return None, []

# Sidebar for file upload
with st.sidebar:
    st.title("💬 WhatsApp Chat Analyzer")
    st.write("---")
    
    uploaded_file = st.file_uploader("Upload WhatsApp Chat Export (.zip or .txt)", type=['zip', 'txt'])
    st.write("**How to export:**")
    st.write("1. Open WhatsApp")
    st.write("2. Select Chat → More → Export")
    st.write("3. Choose 'Without Media'")
    st.write("4. (Optional) Compress to .zip file")

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'zip':
        # Handle zip file
        st.info("📦 Processing zip file...")
        temp_dir, chat_files = extract_and_find_chat(uploaded_file)
        
        if not chat_files:
            st.error("❌ No .txt files found in the zip. Please ensure the zip contains WhatsApp chat exports.")
        else:
            # If multiple files found, let user choose
            if len(chat_files) > 1:
                st.write(f"Found {len(chat_files)} chat files in the zip:")
                selected_file = st.selectbox("Select which chat to analyze:", chat_files)
            else:
                selected_file = chat_files[0]
            
            # Read the selected file
            try:
                with open(selected_file, 'r', encoding='utf-8') as f:
                    data = f.read()
                df = preprocessor.preprocess(data)
                
                if df.empty:
                    st.error("❌ Could not parse chat file. Please ensure it's a valid WhatsApp export.")
                else:
                    st.success("✅ Chat loaded successfully!")
                    file_loaded = True
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                file_loaded = False
    else:
        # Handle txt file (original behavior)
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)
        
        if df.empty:
            st.error("❌ Could not parse chat file. Please ensure it's a valid WhatsApp export.")
            file_loaded = False
        else:
            st.success("✅ Chat loaded successfully!")
            file_loaded = True
    
    if 'df' in locals() and not df.empty and 'file_loaded' in locals() and file_loaded:
        
        # Fetch unique users
        user_list = df['user'].unique().tolist()
        if 'group_notification' in user_list:
            user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
        
        st.sidebar.write("---")
        selected_user = st.sidebar.selectbox("Select User:", user_list)
        
        st.sidebar.write("---")
        
        if st.sidebar.button("🔍 Show Analysis"):
            # Statistics
            num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
            
            st.title("📊 WhatsApp Chat Analysis")
            st.write(f"User: **{selected_user}**")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("💬 Messages", num_messages)
            with col2:
                st.metric("📝 Words", words)
            with col3:
                st.metric("📸 Media", num_media)
            with col4:
                st.metric("🔗 Links", num_links)
            
            st.write("---")
            
            # Most busy users
            if selected_user == 'Overall':
                st.subheader("👥 Most Active Users")
                x, new_df = helper.most_busy_users(df)
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.dataframe(new_df)
                with col2:
                    mu_df = x.reset_index()
                    mu_df.columns = ['user', 'messages']
                    fig = px.bar(mu_df, x='user', y='messages', color='messages', title='Most Active Users', color_continuous_scale='Reds')
                    fig.update_layout(xaxis_tickangle=45, height=420)
                    st.plotly_chart(fig, use_container_width=True)
                
                st.write("---")
            
            # WordCloud
            st.subheader("☁️ Word Cloud")
            try:
                wc = helper.create_wordcloud(selected_user, df)
                # WordCloud returns a WordCloud object; convert to array for display
                wc_img = None
                try:
                    wc_img = wc.to_array()
                except Exception:
                    # fallback: generate blank image
                    wc_img = None
                if wc_img is not None:
                    st.image(wc_img, use_column_width=True)
                else:
                    st.info("No data to generate word cloud")
            except Exception as e:
                st.warning(f"Could not generate word cloud: {str(e)}")
            
            st.write("---")
            
            # Most common words
            st.subheader("📚 Most Common Words")
            most_common_df = helper.most_common_words(selected_user, df)
            
            if len(most_common_df) > 0:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(most_common_df)
                with col2:
                    mc_df = most_common_df.copy()
                    fig = px.bar(mc_df.sort_values('frequency'), x='frequency', y='word', orientation='h', title='Most Common Words', color='frequency', color_continuous_scale='reds')
                    fig.update_layout(height=420)
                    st.plotly_chart(fig, use_container_width=True)
            
            st.write("---")
            
            # Emoji analysis
            st.subheader("😊 Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, df)
            
            if len(emoji_df) > 0:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    ep = emoji_df.head(10)
                    fig = px.pie(ep, values='frequency', names='emoji', title='Top Emojis')
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No emojis found in messages")
            
            st.write("---")
            
            # Monthly timeline (interactive)
            st.subheader("📈 Monthly Timeline")
            try:
                timeline = helper.monthly_timeline(selected_user, df)
                if len(timeline) > 0 and 'message' in timeline.columns and 'time' in timeline.columns:
                    fig = px.line(timeline, x='time', y='message', markers=True, title='Messages Over Months')
                    fig.update_traces(line=dict(color='green'), marker=dict(size=8))
                    fig.update_layout(xaxis_tickangle=45, yaxis_title='Number of Messages', height=450)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📊 No monthly data available for the selected user")
            except Exception as e:
                st.error(f"Error generating monthly timeline: {str(e)}")

            st.write("---")

            # Daily timeline (interactive)
            st.subheader("📅 Daily Timeline")
            try:
                daily_timeline = helper.daily_timeline(selected_user, df)
                if len(daily_timeline) > 0 and 'only_date' in daily_timeline.columns and 'message' in daily_timeline.columns:
                    fig = px.line(daily_timeline, x='only_date', y='message', markers=True, title='Messages Over Days')
                    fig.update_traces(line=dict(color='black'), marker=dict(size=6))
                    fig.update_layout(xaxis=dict(tickangle=45), yaxis_title='Number of Messages', height=450)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📊 No daily data available for the selected user")
            except Exception as e:
                st.error(f"Error generating daily timeline: {str(e)}")

            st.write("---")

            # Activity by day (interactive)
            st.subheader("📊 Activity by Day of Week")
            try:
                busy_day = helper.week_activity_map(selected_user, df)
                if len(busy_day) > 0:
                    bd_df = busy_day.reset_index()
                    bd_df.columns = ['day', 'messages']
                    fig = px.bar(bd_df, x='day', y='messages', color='messages', color_continuous_scale='Purples', title='Activity by Day of Week')
                    fig.update_layout(xaxis_tickangle=45, yaxis_title='Number of Messages', height=450)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📊 No day activity data available")
            except Exception as e:
                st.error(f"Error generating day activity: {str(e)}")

            st.write("---")

            # Activity by month (interactive)
            st.subheader("📅 Activity by Month")
            try:
                busy_month = helper.month_activity_map(selected_user, df)
                if len(busy_month) > 0:
                    bm_df = busy_month.reset_index()
                    bm_df.columns = ['month', 'messages']
                    fig = px.bar(bm_df, x='month', y='messages', color='messages', color_continuous_scale='Oranges', title='Activity by Month')
                    fig.update_layout(xaxis_tickangle=45, yaxis_title='Number of Messages', height=450)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📊 No month activity data available")
            except Exception as e:
                st.error(f"Error generating month activity: {str(e)}")

            st.write("---")

            # Activity heatmap (interactive)
            st.subheader("🔥 Activity Heatmap (Day vs Hour)")
            try:
                user_heatmap = helper.activity_heatmap(selected_user, df)
                if isinstance(user_heatmap, (list, tuple)):
                    # safety: ensure it's a dataframe
                    user_heatmap = user_heatmap[0]
                if hasattr(user_heatmap, 'shape') and user_heatmap.shape[0] > 0 and user_heatmap.shape[1] > 0:
                    z = user_heatmap.values
                    x = [str(c) for c in user_heatmap.columns]
                    y = user_heatmap.index.tolist()
                    heat = go.Figure(data=go.Heatmap(z=z, x=x, y=y, colorscale='YlOrRd', colorbar=dict(title='Message Count')))
                    heat.update_layout(title='Activity Heatmap (Hour of Day vs Day of Week)', xaxis_title='Hour', yaxis_title='Day of Week', height=500)
                    st.plotly_chart(heat, use_container_width=True)
                else:
                    st.info("🔥 No heatmap data available for the selected user")
            except Exception as e:
                st.error(f"Error generating heatmap: {str(e)}")

else:
    st.title("👋 Welcome to WhatsApp Chat Analyzer")
    st.write("""This application analyzes WhatsApp chat exports and provides detailed insights.
    
    **Features:**
    - 📊 Message Statistics
    - 👥 User Activity Analysis
    - ☁️ Word Cloud Visualization
    - 📚 Word Frequency Analysis
    - 😊 Emoji Analysis
    - 📈 Timeline Trends
    - 🔥 Activity Heatmaps
    
    **Getting Started:**
    1. Export your WhatsApp chat (without media)
    2. Upload the .txt file using the sidebar
    3. Select a user or "Overall" for group analysis
    4. Click "Show Analysis" to view the dashboard
    """)
    st.info("📤 Upload a WhatsApp chat export to begin!")










