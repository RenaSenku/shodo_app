import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# データ読み込み
DATA_FILE = "shodo_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

st.title("🖌️ 書道カウンセリングツール")

# --- サイドバー ---
st.sidebar.header("🔍 フィルター")

# フィルター
reason = st.sidebar.multiselect("始めた理由で絞る", df["始めた理由"].unique())
nayami = st.sidebar.multiselect("悩みで絞る", df["悩み"].unique())
tool = st.sidebar.multiselect("道具で絞る", df["道具"].unique())

filtered_df = df.copy()

if reason:
    filtered_df = filtered_df[filtered_df["始めた理由"].isin(reason)]
if nayami:
    filtered_df = filtered_df[filtered_df["悩み"].str.contains('|'.join(nayami), na=False)]
if tool:
    filtered_df = filtered_df[filtered_df["道具"].isin(tool)]

st.subheader("🎯 フィルター結果")
st.dataframe(filtered_df)

# --- グラフ分析 ---
st.subheader("📊 書道を始めた理由（人数）")
reason_counts = df["始めた理由"].value_counts()
st.bar_chart(reason_counts)

st.subheader("📊 よくある悩み（キーワード別）")
all_nayami = df["悩み"].dropna().str.split("、|,| ").explode()
nayami_counts = all_nayami.value_counts()
st.bar_chart(nayami_counts)

# --- 個人カルテ ---
st.subheader("🧑‍🏫 個人カルテを見る")
names = df["名前"].dropna().unique()
selected_name = st.selectbox("名前を選んでください", names)

if selected_name:
    person = df[df["名前"] == selected_name].iloc[0]
    st.markdown(f"""
    ### 📝 {selected_name}さんの情報
    - 始めた理由: **{person['始めた理由']}**
    - 目標: **{person['目標']}**
    - 悩み: **{person['悩み']}**
    - 指導メモ: {person['指導メモ']}
    - 道具: {person['道具']}
    """)

# --- 新規データ入力 ---
st.subheader("🆕 新しい生徒のデータを追加")

with st.form("new_entry"):
    col1, col2 = st.columns(2)
    with col1:
        new_name = st.text_input("名前")
        new_age = st.text_input("年代")
        new_reason = st.text_input("始めた理由")
        new_goal = st.text_input("目標")
    with col2:
        new_nayami = st.text_input("悩み（カンマ区切り）")
        new_memo = st.text_input("指導メモ")
        new_tool = st.text_input("道具")

    submitted = st.form_submit_button("追加する")
    if submitted:
        new_data = pd.DataFrame([{
            "名前": new_name,
            "年代": new_age,
            "始めた理由": new_reason,
            "目標": new_goal,
            "悩み": new_nayami,
            "指導メモ": new_memo,
            "道具": new_tool
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"{new_name} さんのデータを追加しました！")
