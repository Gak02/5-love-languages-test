import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# japanize_matplotlibの代わりに直接フォント設定を行う
import matplotlib as mpl
import plotly.graph_objects as go

# 日本語フォント設定（代替方法）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Hiragino Sans GB', 'Microsoft YaHei', 'sans-serif']

# ページ設定
st.set_page_config(
    page_title="5つの愛の言語テスト",
    page_icon="❤️",
    layout="wide",
)

# アプリのタイトルとイントロ
st.title("5つの愛の言語テスト")
st.markdown("""
このテストは、あなたの「愛の言語」の傾向を診断するものです。
各質問に対して、あなたにとってより嬉しいと感じる方を選んでください。
""")

# 愛の言語の定義
love_languages = {
    'words': '言葉による肯定',
    'time': '質の高い時間',
    'gifts': 'プレゼント',
    'service': '奉仕行為',
    'touch': '身体的接触'
}

# 質問と各選択肢の愛の言語マッピング
questions = [
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "パートナーに「ありがとね」って言ってもらえる", "language": "words"},
            {"text": "パートナーとふたりだけで過ごせる", "language": "time"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "自分の担当だけどストレスありすぎてできないことを代わりにやってくれる", "language": "service"},
            {"text": "外で一緒にいるとき、パートナーが腕を回してくれる", "language": "touch"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "パートナーとのんびり一緒に過ごせる時間がある", "language": "time"},
            {"text": "パートナーがちょっとしたプレゼントで感謝を伝えてくれる", "language": "gifts"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "優しいことを言うだけじゃなくて、実際に行動してくれる", "language": "service"},
            {"text": "パートナーから「愛してる」って言ってもらえる", "language": "words"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "話してるときに途中でさえぎられない", "language": "time"},
            {"text": "やらなきゃいけないことを一緒に取り組んでくれる", "language": "service"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "愛情の印として、小さなプレゼントをくれる", "language": "gifts"},
            {"text": "人前で自然に手をつないだり触れたりできる", "language": "touch"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "パートナーと身体的に親密な時間を持てる", "language": "touch"},
            {"text": "特に理由なくパートナーに褒められる", "language": "words"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "洗濯とか車にガソリン入れるとか、思いがけず何かしてくれる", "language": "service"},
            {"text": "自分のことをちゃんと考えて選んでくれたプレゼントをくれる", "language": "gifts"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "普段の生活の中でよくスキンシップをとる", "language": "touch"},
            {"text": "ちゃんと話を聞いてくれて、気持ちをわかろうとしてくれる", "language": "time"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "パートナーに「すごいね！」とか「尊敬する！」って言ってもらえる", "language": "words"},
            {"text": "サプライズでプレゼントをくれる", "language": "gifts"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "ワクワクするようなプレゼントをもらえる", "language": "gifts"},
            {"text": "何かの作業を手伝ってくれる", "language": "service"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "ハグして気持ちがつながってると感じられる", "language": "touch"},
            {"text": "特に何するでもなく、一緒にいられるだけで嬉しい", "language": "time"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "パートナーから褒められる", "language": "words"},
            {"text": "自分の負担を減らすために何かしてくれる", "language": "service"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "パートナーとハグする", "language": "touch"},
            {"text": "パートナーからプレゼントをもらう", "language": "gifts"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "邪魔されずにパートナーとゆっくり過ごせる", "language": "time"},
            {"text": "パートナーに背中をさすってもらったりマッサージしてもらう", "language": "touch"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "自分が頑張ったことにポジティブな反応をくれる", "language": "words"},
            {"text": "パートナーと一緒にどこかに出かけられる", "language": "time"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "忙しいのに手伝ってくれる", "language": "service"},
            {"text": "特別な理由がなくても、愛のこもったメッセージをくれる", "language": "words"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "パートナーとよくキスする", "language": "touch"},
            {"text": "家事や仕事などをいつもより多くやってくれる", "language": "service"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "普段の中で、ついでに小さなプレゼントを買ってきてくれる", "language": "gifts"},
            {"text": "特に何もしなくても、一緒にいられるのが嬉しい", "language": "time"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "「あなたのこと、すごく大切だよ」って言ってくれる", "language": "words"},
            {"text": "プレゼントが楽しみで記念日が待ち遠しい", "language": "gifts"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "プレゼントを贈り合うのが関係の大事な一部になってる", "language": "gifts"},
            {"text": "パートナーが励ましてくれる", "language": "words"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "自分の好きなことに興味を持ってくれるのが伝わってくる", "language": "time"},
            {"text": "実際に助かることをしてくれる", "language": "service"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "自分が疲れてるのをわかって手伝ってくれる", "language": "service"},
            {"text": "パートナーと触れ合える", "language": "touch"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "一緒に趣味や活動を楽しめる", "language": "time"},
            {"text": "パートナーが旅行から帰ってきて、お土産をくれる", "language": "gifts"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "パートナーと手をつなぐ", "language": "touch"},
            {"text": "見た目のことで褒めてもらえる", "language": "words"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "励ましの言葉をくれる", "language": "words"},
            {"text": "パートナーのそばにぴったり座れる", "language": "touch"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "「買い物行こうか？」とか用事を代わってくれる", "language": "service"},
            {"text": "パートナーと一緒に何かするのが楽しい", "language": "time"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "よく考えて選んでくれたプレゼントをもらう", "language": "gifts"},
            {"text": "少し離れてたあと、ハグできるのが嬉しい", "language": "touch"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "話してるときにスマホを見ずにちゃんと向き合ってくれる", "language": "time"},
            {"text": "「ありがとね」ってちゃんと言ってくれる", "language": "words"}
        ]
    },
    {
        "question": "自分的に嬉しいのは…",
        "options": [
            {"text": "自分のために、あまり好きじゃないことでもしてくれる", "language": "service"},
            {"text": "サプライズで小さなプレゼントをもらう", "language": "gifts"}
        ]
    }
]

# セッション状態を初期化
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
    
if 'results' not in st.session_state:
    st.session_state.results = {
        'words': 0,
        'time': 0,
        'gifts': 0,
        'service': 0,
        'touch': 0
    }

if 'completed' not in st.session_state:
    st.session_state.completed = False

# 次の質問に進む関数
def next_question(language):
    # 選択された言語のカウントを増やす
    st.session_state.results[language] += 1
    
    # 次の質問に進む
    st.session_state.current_question += 1
    
    # すべての質問が終わったら完了フラグを立てる
    if st.session_state.current_question >= len(questions):
        st.session_state.completed = True

# 結果をレーダーチャートで表示する関数
def display_results():
    # データを作成
    labels = [love_languages[lang] for lang in ['words', 'time', 'gifts', 'service', 'touch']]
    values = [st.session_state.results[lang] for lang in ['words', 'time', 'gifts', 'service', 'touch']]
    
    # 結果のパーセンテージを計算
    total = sum(values)
    percentages = [round(value / total * 100, 1) for value in values]
    
    # 結果をテーブルとして表示
    results_df = pd.DataFrame({
        '愛の言語': labels,
        'スコア': values,
        'パーセンテージ': [f"{p}%" for p in percentages]
    })
    results_df = results_df.sort_values('スコア', ascending=False)
    
    st.subheader("あなたの愛の言語の結果")
    st.dataframe(results_df, use_container_width=True, hide_index=True)
    
    # 主要な愛の言語の説明
    primary_language = results_df.iloc[0]['愛の言語']
    st.subheader(f"あなたの最も重要な愛の言語は「{primary_language}」です")
    
    if primary_language == '言葉による肯定':
        st.markdown("""
        **言葉による肯定**を愛の言語とする人は、パートナーからの言葉によるサポートや褒め言葉、感謝の言葉によって愛を感じます。
        「ありがとう」「素晴らしいね」「愛してる」などの言葉が特に重要です。
        """)
    elif primary_language == '質の高い時間':
        st.markdown("""
        **質の高い時間**を愛の言語とする人は、パートナーと一緒に過ごす集中した時間によって愛を感じます。
        スマホを置いて会話に集中したり、一緒に活動を楽しんだりする時間が特に重要です。
        """)
    elif primary_language == 'プレゼント':
        st.markdown("""
        **プレゼント**を愛の言語とする人は、贈り物（大小問わず）を通じて愛情を感じます。
        プレゼントを受け取ることで、パートナーが自分のことを考えていることを実感できます。
        """)
    elif primary_language == '奉仕行為':
        st.markdown("""
        **奉仕行為**を愛の言語とする人は、パートナーが行動で示してくれることによって愛を感じます。
        家事を手伝ったり、負担を減らす行動をしてくれることが特に重要です。
        """)
    elif primary_language == '身体的接触':
        st.markdown("""
        **身体的接触**を愛の言語とする人は、触れ合うことによって愛情を感じます。
        ハグ、キス、手をつなぐなどの身体的な近さが特に重要です。
        """)
    
    # 新しいレーダーチャートを作成して表示
    fig = create_radar_chart(st.session_state.results)
    st.plotly_chart(fig, use_container_width=True)
    
    # レーダーチャートの下にメッセージ
    st.markdown("""
    ## 愛の言語について
    
    「5つの愛の言語」は、ゲイリー・チャップマン博士によって提唱された理論です。この理論では、人はそれぞれ異なる方法で愛情を表現し、受け取ると考えます。
    
    パートナーとのより良い関係のために、お互いの愛の言語を理解し、相手が重視する方法で愛情を表現することが大切です。
    
    このテスト結果は、あなたがどのように愛情を受け取りたいかを示しています。パートナーとこの結果について話し合ってみてはいかがでしょうか？
    """)
    
    # リセットボタン
    if st.button("テストをリセットする"):
        st.session_state.current_question = 0
        st.session_state.results = {
            'words': 0,
            'time': 0,
            'gifts': 0,
            'service': 0,
            'touch': 0
        }
        st.session_state.completed = False
        st.rerun()

# レーダーチャートを作成する関数
def create_radar_chart(scores):
    """
    より美しく見やすいレーダーチャートを作成する関数
    
    Parameters:
    -----------
    scores : dict
        各愛の言語のスコア
        
    Returns:
    --------
    plotly の Figure オブジェクト
    """
    # スコアとカテゴリの取得
    labels = [love_languages[lang] for lang in ['words', 'time', 'gifts', 'service', 'touch']]
    values = [scores[lang] for lang in ['words', 'time', 'gifts', 'service', 'touch']]
    
    # データを円形にするために最初の値を最後にも追加
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]
    
    # 最大値を計算
    max_value = max(values)
    
    # カラー設定
    main_color = '#4361EE'  # メインカラー
    bg_color = 'rgba(240, 242, 246, 0.5)'  # バックグラウンド
    grid_color = 'rgba(200, 200, 200, 0.6)'  # グリッド線
    
    fig = go.Figure()
    
    # スコアのプロット
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=labels_closed,
        fill='toself',
        name='あなたのスコア',
        line=dict(
            color=main_color,
            width=3
        ),
        fillcolor=f'rgba(67, 97, 238, 0.3)',  # メインカラーに透明度追加
        hoverinfo='text',
        hovertext=[f'{labels[i]}: {values[i]}' for i in range(len(labels))] + [f'{labels[0]}: {values[0]}'],
    ))
    
    # 軸の最大値を少し拡張して余白を作る
    axis_max = max(12, max_value + 1)
    
    # レイアウト設定
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, axis_max],
                tickfont=dict(size=11),
                tickmode='linear',
                nticks=6,  # 目盛りの数を調整
                gridcolor=grid_color,
                linecolor=grid_color,
            ),
            angularaxis=dict(
                tickfont=dict(size=13, family="Arial, sans-serif"),
                gridcolor=grid_color,
                linecolor=grid_color,
            ),
            bgcolor=bg_color
        ),
        showlegend=False,  # 凡例は不要なので非表示
        margin=dict(l=80, r=80, t=60, b=60),  # 余白を増やして見やすく
        height=500,  # 適切な高さ
        title=dict(
            text="あなたの5つの愛の言語",
            font=dict(size=18, family="Arial, sans-serif"),
            x=0.5,
            y=0.95
        ),
        paper_bgcolor='rgba(0,0,0,0)',  # 透明な背景
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    # カテゴリごとのスコア表示を追加（チャート上部）
    categories_text = '<br>'.join([f'<b>{labels[i]}:</b> {values[i]}' for i in range(len(labels))])
    fig.add_annotation(
        xref='paper',
        yref='paper',
        x=0.98,
        y=0.98,
        text=categories_text,
        showarrow=False,
        font=dict(size=12),
        align='right',
        bgcolor='rgba(255, 255, 255, 0.7)',
        bordercolor='rgba(200, 200, 200, 0.8)',
        borderwidth=1,
        borderpad=4,
        borderradius=4
    )
    
    # 各カテゴリにカラーマーカーを追加
    for i, (label, value) in enumerate(zip(labels, values)):
        angle = (i / len(labels)) * 2 * np.pi
        r_position = value
        
        # マーカーポイントを強調
        fig.add_trace(go.Scatterpolar(
            r=[r_position],
            theta=[label],
            mode='markers',
            marker=dict(
                size=10,
                color=main_color,
                line=dict(width=2, color='white')
            ),
            showlegend=False,
            hoverinfo='text',
            hovertext=f'{label}: {value}'
        ))
    
    return fig

# メイン処理
if st.session_state.completed:
    display_results()
else:
    # 現在の質問を表示
    current_q = questions[st.session_state.current_question]
    st.progress((st.session_state.current_question) / len(questions))
    st.write(f"質問 {st.session_state.current_question + 1}/{len(questions)}")
    
    # オプションを表示して選択を処理
    st.subheader(current_q["question"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(current_q["options"][0]["text"], use_container_width=True):
            next_question(current_q["options"][0]["language"])
            st.rerun()
    
    with col2:
        if st.button(current_q["options"][1]["text"], use_container_width=True):
            next_question(current_q["options"][1]["language"])
            st.rerun()

# 最後に研究結果についての脚注を追加
st.markdown("""
---
**注意**: 添付の研究論文では、「奉仕行為」と「贈り物」が「犠牲的愛」として一つの因子に統合される可能性が示されていますが、
このアプリでは従来の5つの愛の言語の枠組みを使用しています。
""")
