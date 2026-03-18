import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib as mpl

st.set_page_config(
    page_title="Ecommerce Funnel Analysis",
    page_icon="📊",
    layout="wide"
)

# ── Global matplotlib style ────────────────────────────────
mpl.rcParams.update({
    'font.family':        'serif',
    'font.size':          11,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.spines.left':   False,
    'axes.grid':          True,
    'axes.grid.axis':     'x',
    'grid.color':         '#f0f0f0',
    'grid.linewidth':     0.8,
    'axes.facecolor':     '#ffffff',
    'figure.facecolor':   '#ffffff',
    'xtick.color':        '#666666',
    'ytick.color':        '#333333',
    'text.color':         '#1a1a1a',
    'axes.labelcolor':    '#555555',
    'axes.labelsize':     10,
    'xtick.labelsize':    9,
    'ytick.labelsize':    9,
})

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Main background */
.stApp {
    background-color: #f8f7f4;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f1117 !important;
    border-right: 1px solid #1e2130;
}
section[data-testid="stSidebar"] * {
    color: #c8c8c8 !important;
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: #888 !important;
    font-size: 12px !important;
}
section[data-testid="stSidebar"] h1 {
    color: #ffffff !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 18px !important;
    letter-spacing: 0.02em;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #e8e4dc;
    border-radius: 8px;
    padding: 16px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
[data-testid="metric-container"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #999 !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px !important;
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

/* Chart containers */
[data-testid="stPlotlyChart"],
.element-container .stImage {
    background: #ffffff;
    border-radius: 10px;
    border: 1px solid #e8e4dc;
    padding: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* Subheaders */
h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #1a1a1a !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    background: #ffffff !important;
    border: 1px solid #e8e4dc !important;
    border-radius: 8px !important;
    color: #555 !important;
}
.streamlit-expanderContent {
    background: #ffffff !important;
    border: 1px solid #e8e4dc !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* Divider */
hr {
    border: none !important;
    border-top: 1px solid #e8e4dc !important;
    margin: 24px 0 !important;
}

/* Info box */
.stAlert {
    background: #f0f4ff !important;
    border: 1px solid #c8d4f8 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
}

/* Slider */
.stSlider label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #999 !important;
}

/* Caption */
.stCaption {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    color: #aaa !important;
    letter-spacing: 0.04em !important;
}

/* Spinner */
.stSpinner > div {
    border-color: #1a1a1a !important;
}

/* Multiselect tags */
.stMultiSelect span[data-baseweb="tag"] {
    background-color: #1a1a1a !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

DATA_PATH = '/Users/prasannapingale/ecommerce-funnel-analysis/data/2019-Oct.csv'

# ── Color palette ──────────────────────────────────────────
PRIMARY   = '#1a1a1a'
ACCENT    = '#2563eb'
ACCENT2   = '#64a0f7'
ACCENT3   = '#bcd4fc'
MUTED     = '#9ca3af'
DANGER    = '#dc2626'
SUCCESS   = '#16a34a'
BG        = '#ffffff'
GRID      = '#f3f4f6'

def chart_style(ax, grid_axis='x'):
    ax.set_facecolor(BG)
    ax.figure.set_facecolor(BG)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#e5e7eb')
    ax.tick_params(colors='#6b7280', labelsize=9)
    ax.xaxis.label.set_color('#6b7280')
    ax.yaxis.label.set_color('#6b7280')
    if grid_axis == 'x':
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, color=GRID, linewidth=0.8)
        ax.yaxis.grid(False)
    elif grid_axis == 'y':
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color=GRID, linewidth=0.8)
        ax.xaxis.grid(False)
    else:
        ax.grid(False)

@st.cache_data
def load_data():
    df = pd.read_csv(
        DATA_PATH,
        parse_dates=['event_time'],
        usecols=['event_time', 'event_type', 'user_id',
                 'product_id', 'category_code', 'brand', 'price'],
        nrows=500000
    )
    df['hour'] = df['event_time'].dt.hour
    df['day_of_week'] = df['event_time'].dt.day_name()
    df[['cat_l1', 'cat_l2', 'cat_l3']] = (
        df['category_code']
        .str.split('.', expand=True, n=2)
        .reindex(columns=[0, 1, 2])
    )
    df['price_bucket'] = pd.cut(
        df['price'],
        bins=[0, 50, 100, 200, 500, 1000, 2000, float('inf')],
        labels=['$0–50', '$50–100', '$100–200',
                '$200–500', '$500–1k', '$1k–2k', '$2k+']
    )
    return df

@st.cache_data
def load_cohort_data():
    chunks = []
    reader = pd.read_csv(
        DATA_PATH,
        parse_dates=['event_time'],
        usecols=['event_time', 'event_type', 'user_id',
                 'product_id', 'category_code', 'brand', 'price'],
        chunksize=500000
    )
    for chunk in reader:
        chunks.append(chunk[chunk['event_type'] == 'purchase'])
    df_p = pd.concat(chunks, ignore_index=True)
    df_p['purchase_date'] = pd.to_datetime(df_p['event_time']).dt.date
    return df_p

df = load_data()

# ── Sidebar ────────────────────────────────────────────────
st.sidebar.markdown("## Ecommerce\nFunnel Analysis")
st.sidebar.markdown("---")

all_cats = sorted(df['cat_l1'].dropna().unique().tolist())
selected_cats = st.sidebar.multiselect(
    "Categories",
    options=all_cats,
    default=all_cats
)
price_min, price_max = st.sidebar.slider(
    "Price range ($)",
    min_value=0, max_value=2000,
    value=(0, 2000), step=50
)
top_n_brands = st.sidebar.slider(
    "Brands to show",
    min_value=5, max_value=15, value=10
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "REES46 Multi-Category Store  \n"
    "October 2019 · 500k sample  \n\n"
    "Prasanna Pingale"
)

# ── Filter ─────────────────────────────────────────────────
df_f = df[
    (df['cat_l1'].isin(selected_cats)) &
    (df['price'] >= price_min) &
    (df['price'] <= price_max)
].copy()

# ── Header ─────────────────────────────────────────────────
st.markdown("""
<div style="padding: 32px 0 8px 0;">
    <div style="font-family: 'DM Mono', monospace; font-size: 11px;
                letter-spacing: 0.1em; text-transform: uppercase;
                color: #999; margin-bottom: 8px;">
        Product Analytics · October 2019
    </div>
    <h1 style="font-family: 'Playfair Display', serif; font-size: 38px;
               font-weight: 700; color: #1a1a1a; margin: 0;
               letter-spacing: -0.02em; line-height: 1.1;">
        Ecommerce Funnel Analysis
    </h1>
    <p style="font-family: 'DM Sans', sans-serif; font-size: 15px;
              color: #6b7280; margin-top: 10px; font-weight: 300;">
        REES46 Multi-Category Store · 42M events · 13 product categories
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Dynamic insights panel ─────────────────────────────────
cat_insights = (
    df_f.groupby(['cat_l1', 'event_type'])
    .size().unstack(fill_value=0)
    .rename(columns={'view': 'views', 'cart': 'carts',
                     'purchase': 'purchases'})
)
for c in ['views', 'carts', 'purchases']:
    if c not in cat_insights.columns:
        cat_insights[c] = 0
cat_insights['v2p'] = (
    cat_insights['purchases'] / cat_insights['views'] * 100
).round(2)
cat_insights = cat_insights[cat_insights['views'] > 100]

df_bi = df_f.dropna(subset=['brand'])
top_b = df_bi['brand'].value_counts().head(10).index
brand_insights = (
    df_bi[df_bi['brand'].isin(top_b)]
    .groupby(['brand', 'event_type']).size()
    .unstack(fill_value=0)
    .rename(columns={'view': 'views', 'cart': 'carts',
                     'purchase': 'purchases'})
)
for c in ['views', 'carts', 'purchases']:
    if c not in brand_insights.columns:
        brand_insights[c] = 0
brand_insights['v2p'] = (
    brand_insights['purchases'] / brand_insights['views'] * 100
).round(2)

pf_i = (
    df_f.groupby(['price_bucket', 'event_type'])
    .size().unstack(fill_value=0)
    .rename(columns={'view': 'views', 'cart': 'carts',
                     'purchase': 'purchases'})
)
for c in ['views', 'carts', 'purchases']:
    if c not in pf_i.columns:
        pf_i[c] = 0
pf_i['v2p'] = (pf_i['purchases'] / pf_i['views'] * 100).round(2)

cart_ev  = df_f[df_f['event_type'] == 'cart']
purch_ev = df_f[df_f['event_type'] == 'purchase'][
    ['user_id', 'product_id']].copy()
purch_ev['purchased'] = 1
aband = cart_ev.merge(
    purch_ev.drop_duplicates(),
    on=['user_id', 'product_id'], how='left'
)
aband['purchased'] = aband['purchased'].fillna(0)
aband_rate = (aband['purchased'] == 0).mean() * 100 if len(aband) > 0 else 0

with st.expander("💡  Key insights — current filter selection", expanded=True):
    i1, i2, i3, i4 = st.columns(4)

    with i1:
        if len(cat_insights) > 0:
            top_cat      = cat_insights['v2p'].idxmax()
            top_cat_rate = cat_insights['v2p'].max()
            worst_cat    = cat_insights['v2p'].idxmin()
            worst_rate   = cat_insights['v2p'].min()
            st.markdown(
                f"<div style='font-family:DM Mono,monospace;font-size:10px;"
                f"letter-spacing:.07em;text-transform:uppercase;color:#999'>"
                f"Category</div>"
                f"<div style='font-size:15px;font-weight:500;color:#1a1a1a;"
                f"margin:4px 0'>🏆 {top_cat} — {top_cat_rate:.2f}%</div>"
                f"<div style='font-size:13px;color:#dc2626'>"
                f"⚠ {worst_cat} — {worst_rate:.2f}%</div>",
                unsafe_allow_html=True
            )

    with i2:
        if len(brand_insights) > 0:
            top_brand      = brand_insights['v2p'].idxmax()
            top_brand_rate = brand_insights['v2p'].max()
            avg_p          = df_bi[df_bi['brand'] == top_brand]['price'].mean()
            st.markdown(
                f"<div style='font-family:DM Mono,monospace;font-size:10px;"
                f"letter-spacing:.07em;text-transform:uppercase;color:#999'>"
                f"Brand</div>"
                f"<div style='font-size:15px;font-weight:500;color:#1a1a1a;"
                f"margin:4px 0'>🏆 {top_brand} — {top_brand_rate:.2f}%</div>"
                f"<div style='font-size:13px;color:#6b7280'>"
                f"Avg price ${avg_p:,.0f}</div>",
                unsafe_allow_html=True
            )

    with i3:
        if len(pf_i) > 0 and pf_i['views'].sum() > 0:
            top_price      = pf_i['v2p'].idxmax()
            top_price_rate = pf_i['v2p'].max()
            st.markdown(
                f"<div style='font-family:DM Mono,monospace;font-size:10px;"
                f"letter-spacing:.07em;text-transform:uppercase;color:#999'>"
                f"Price sweet spot</div>"
                f"<div style='font-size:15px;font-weight:500;color:#1a1a1a;"
                f"margin:4px 0'>💰 {top_price}</div>"
                f"<div style='font-size:13px;color:#6b7280'>"
                f"{top_price_rate:.2f}% conversion rate</div>",
                unsafe_allow_html=True
            )

    with i4:
        if len(aband) > 0:
            st.markdown(
                f"<div style='font-family:DM Mono,monospace;font-size:10px;"
                f"letter-spacing:.07em;text-transform:uppercase;color:#999'>"
                f"Cart abandonment</div>"
                f"<div style='font-size:15px;font-weight:500;color:#1a1a1a;"
                f"margin:4px 0'>🛒 {aband_rate:.1f}% abandoned</div>"
                f"<div style='font-size:13px;color:#16a34a'>"
                f"{100-aband_rate:.1f}% complete purchase</div>",
                unsafe_allow_html=True
            )

st.markdown("---")

# ── KPIs ───────────────────────────────────────────────────
views     = int((df_f['event_type'] == 'view').sum())
carts     = int((df_f['event_type'] == 'cart').sum())
purchases = int((df_f['event_type'] == 'purchase').sum())
v2p = round(purchases / views * 100, 2) if views > 0 else 0
v2c = round(carts     / views * 100, 2) if views > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total views",     f"{views:,}")
c2.metric("Total carts",     f"{carts:,}")
c3.metric("Total purchases", f"{purchases:,}")
c4.metric("View → cart",     f"{v2c:.2f}%")
c5.metric("View → purchase", f"{v2p:.2f}%")

st.markdown("---")

# ── Row 1: Funnel + Category ───────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### Purchase funnel")
    fig, ax = plt.subplots(figsize=(6, 4))
    chart_style(ax, grid_axis='y')
    stages = ['Views', 'Carts', 'Purchases']
    pct    = [100, v2c, v2p]
    counts = [views, carts, purchases]
    bars = ax.bar(stages, pct,
                  color=[PRIMARY, ACCENT, ACCENT2],
                  edgecolor='none', width=0.5,
                  zorder=3)
    for bar, count, p in zip(bars, counts, pct):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 1.5,
                f'{count:,}',
                ha='center', fontsize=8.5,
                color='#1a1a1a', fontweight='500',
                fontfamily='DM Sans')
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height()/2,
                f'{p:.1f}%',
                ha='center', va='center',
                fontsize=10, color='white',
                fontweight='600',
                fontfamily='DM Sans')
    ax.set_ylim(0, 120)
    ax.set_ylabel('')
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.0f%%'))
    plt.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col2:
    st.markdown("### Conversion by category")
    cat_f = (
        df_f.groupby(['cat_l1', 'event_type'])
        .size().unstack(fill_value=0)
        .rename(columns={'view': 'views', 'cart': 'carts',
                         'purchase': 'purchases'})
    )
    for c in ['views', 'carts', 'purchases']:
        if c not in cat_f.columns:
            cat_f[c] = 0
    cat_f['v2p'] = (
        cat_f['purchases'] / cat_f['views'] * 100
    ).round(2)
    cat_f = cat_f[cat_f['views'] > 100].sort_values('v2p')

    fig, ax = plt.subplots(figsize=(6, 4))
    chart_style(ax, grid_axis='x')
    colors = [PRIMARY if v == cat_f['v2p'].max()
              else ACCENT3 for v in cat_f['v2p']]
    bars = ax.barh(cat_f.index, cat_f['v2p'],
                   color=colors, edgecolor='none',
                   height=0.6, zorder=3)
    avg = cat_f['v2p'].mean()
    ax.axvline(avg, color=MUTED, linestyle='--',
               linewidth=1, label=f'Avg {avg:.2f}%', zorder=4)
    for i, v in enumerate(cat_f['v2p']):
        ax.text(v + 0.04, i, f'{v}%',
                va='center', fontsize=8,
                color='#6b7280', fontfamily='DM Sans')
    ax.set_xlabel('View-to-purchase %')
    ax.legend(fontsize=8, frameon=False)
    plt.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()

st.markdown("---")

# ── Row 2: Brand + Price ───────────────────────────────────
col3, col4 = st.columns([1, 1], gap="large")

with col3:
    st.markdown(f"### Top {top_n_brands} brands — conversion vs price")
    df_brand = df_f.dropna(subset=['brand'])
    top_brands = df_brand['brand'].value_counts().head(top_n_brands).index
    bf = (
        df_brand[df_brand['brand'].isin(top_brands)]
        .groupby(['brand', 'event_type']).size()
        .unstack(fill_value=0)
        .rename(columns={'view': 'views', 'cart': 'carts',
                         'purchase': 'purchases'})
    )
    for c in ['views', 'carts', 'purchases']:
        if c not in bf.columns:
            bf[c] = 0
    bf['v2p'] = (bf['purchases'] / bf['views'] * 100).round(2)
    bf['avg_price'] = (
        df_brand[df_brand['brand'].isin(top_brands)]
        .groupby('brand')['price'].mean().round(0)
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    chart_style(ax, grid_axis='both')
    ax.scatter(bf['avg_price'], bf['v2p'],
               s=bf['views'] / 150,
               color=ACCENT, alpha=0.75,
               edgecolors='white', linewidth=1.5,
               zorder=5)
    for brand, row in bf.iterrows():
        if row['v2p'] > bf['v2p'].quantile(0.5):
            ax.annotate(
                brand,
                (row['avg_price'], row['v2p']),
                textcoords='offset points',
                xytext=(8, 4), fontsize=8,
                color='#374151',
                fontfamily='DM Sans'
            )
    ax.set_xlabel('Avg price ($)')
    ax.set_ylabel('View-to-purchase %')
    plt.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()

with col4:
    st.markdown("### Conversion by price range")
    pf = (
        df_f.groupby(['price_bucket', 'event_type'])
        .size().unstack(fill_value=0)
        .rename(columns={'view': 'views', 'cart': 'carts',
                         'purchase': 'purchases'})
    )
    for c in ['views', 'carts', 'purchases']:
        if c not in pf.columns:
            pf[c] = 0
    pf['v2p'] = (pf['purchases'] / pf['views'] * 100).round(2)

    fig, ax = plt.subplots(figsize=(6, 4))
    chart_style(ax, grid_axis='y')
    colors = [PRIMARY if v == pf['v2p'].max()
              else ACCENT3 for v in pf['v2p']]
    ax.bar(pf.index.astype(str), pf['v2p'],
           color=colors, edgecolor='none',
           width=0.6, zorder=3)
    for i, v in enumerate(pf['v2p']):
        ax.text(i, v + 0.05, f'{v}%',
                ha='center', fontsize=8,
                color='#6b7280', fontfamily='DM Sans')
    ax.set_xlabel('Price range')
    ax.set_ylabel('View-to-purchase %')
    ax.tick_params(axis='x', rotation=30)
    plt.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()

st.markdown("---")

# ── Row 3: Time patterns ───────────────────────────────────
st.markdown("### Conversion rate by hour of day (UTC)")

conv_hour = (
    df_f.groupby(['hour', 'event_type'])
    .size().unstack(fill_value=0)
)
if 'purchase' in conv_hour.columns and 'view' in conv_hour.columns:
    conv_hour['conv_pct'] = (
        conv_hour['purchase'] / conv_hour['view'] * 100
    ).round(2)
    fig, ax = plt.subplots(figsize=(14, 3))
    chart_style(ax, grid_axis='y')
    ax.plot(conv_hour.index, conv_hour['conv_pct'],
            marker='o', color=PRIMARY,
            linewidth=2, markersize=5,
            markerfacecolor='white',
            markeredgewidth=2,
            zorder=5)
    ax.fill_between(conv_hour.index, conv_hour['conv_pct'],
                    alpha=0.06, color=PRIMARY)
    ax.set_xlabel('Hour (UTC)')
    ax.set_ylabel('Conversion %')
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f%%'))
    plt.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()

st.markdown("---")

# ── Row 4: Cart abandonment ────────────────────────────────
st.markdown("### Cart abandonment by sub-category")

cart_events  = df_f[df_f['event_type'] == 'cart'].copy()
purch_events = df_f[df_f['event_type'] == 'purchase'][
    ['user_id', 'product_id']].copy()
purch_events['purchased'] = 1
abandoned = cart_events.merge(
    purch_events.drop_duplicates(),
    on=['user_id', 'product_id'], how='left'
)
abandoned['purchased'] = abandoned['purchased'].fillna(0)

cat_ab = (
    abandoned.groupby('category_code')
    .agg(total_carts=('purchased', 'count'),
         abandoned=('purchased', lambda x: (x == 0).sum()))
    .assign(abandonment_rate=lambda x:
            (x['abandoned'] / x['total_carts'] * 100).round(1))
    .query('total_carts >= 10')
    .sort_values('abandonment_rate', ascending=True)
    .tail(12)
)

if len(cat_ab) > 0:
    fig, ax = plt.subplots(figsize=(14, 5))
    chart_style(ax, grid_axis='x')
    colors = [DANGER if r > 50 else ACCENT
              for r in cat_ab['abandonment_rate']]
    ax.barh(
        cat_ab.index.str.replace('electronics.', 'elec.')
                   .str.replace('appliances.', 'appl.'),
        cat_ab['abandonment_rate'],
        color=colors, edgecolor='none',
        height=0.6, zorder=3
    )
    overall_rate = (abandoned['purchased'] == 0).sum() / len(abandoned) * 100
    ax.axvline(overall_rate, color=MUTED, linestyle='--',
               linewidth=1,
               label=f'Overall avg: {overall_rate:.1f}%', zorder=4)
    for i, v in enumerate(cat_ab['abandonment_rate']):
        ax.text(v + 0.3, i, f'{v}%',
                va='center', fontsize=8,
                color='#6b7280', fontfamily='DM Sans')
    ax.set_xlabel('Abandonment rate %')
    ax.legend(fontsize=8.5, frameon=False)
    plt.tight_layout(pad=1.5)
    st.pyplot(fig, use_container_width=True)
    plt.close()

st.markdown("---")

# ── Row 5: Cohort heatmap ──────────────────────────────────
st.markdown("### Cohort retention — % of buyers who purchased again")
st.markdown(
    "<p style='color:#6b7280;font-size:13px;margin-top:-8px'>"
    "Full October 2019 dataset (347k buyers). "
    "Each row = first purchase cohort. "
    "Each column = % who purchased again N days later.</p>",
    unsafe_allow_html=True
)

with st.spinner("Building cohort table..."):
    df_purchases = load_cohort_data()

first_purchase = (
    df_purchases.groupby('user_id')['purchase_date']
    .min().reset_index()
    .rename(columns={'purchase_date': 'cohort_date'})
)
df_purchases = df_purchases.merge(first_purchase, on='user_id')
df_purchases['days_since_first'] = (
    pd.to_datetime(df_purchases['purchase_date']) -
    pd.to_datetime(df_purchases['cohort_date'])
).dt.days

cohort_sizes = (
    first_purchase.groupby('cohort_date')
    .size().reset_index(name='cohort_size')
)
retention = (
    df_purchases[df_purchases['days_since_first'] > 0]
    .groupby(['cohort_date', 'days_since_first'])['user_id']
    .nunique().reset_index(name='returning_users')
)
retention = retention.merge(cohort_sizes, on='cohort_date')
retention['retention_rate'] = (
    retention['returning_users'] / retention['cohort_size'] * 100
).round(2)

retention_pivot = retention.pivot_table(
    index='cohort_date',
    columns='days_since_first',
    values='retention_rate',
    fill_value=0
)
day_cols = [d for d in range(1, 15) if d in retention_pivot.columns]
retention_pivot = retention_pivot[day_cols]

num_cohorts = st.slider(
    "Cohorts to display",
    min_value=5, max_value=25, value=15
)
heat_data = retention_pivot.head(num_cohorts)

fig, ax = plt.subplots(figsize=(16, num_cohorts * 0.42 + 1.5))
ax.set_facecolor(BG)
fig.set_facecolor(BG)

im = ax.imshow(heat_data.values,
               cmap='Blues', aspect='auto',
               vmin=0, vmax=12)

for i in range(heat_data.shape[0]):
    for j in range(heat_data.shape[1]):
        val = heat_data.values[i, j]
        color = 'white' if val > 6 else '#374151'
        ax.text(j, i, f'{val:.1f}%',
                ha='center', va='center',
                fontsize=8, color=color,
                fontweight='600',
                fontfamily='DM Sans')

ax.set_xticks(range(len(heat_data.columns)))
ax.set_xticklabels(
    [f'Day {d}' for d in heat_data.columns],
    fontsize=8.5, color='#6b7280'
)
ax.set_yticks(range(len(heat_data.index)))
ax.set_yticklabels(
    [str(d) for d in heat_data.index],
    fontsize=8.5, color='#6b7280'
)
ax.set_xlabel('Days since first purchase',
              fontsize=10, color='#6b7280', labelpad=12)
ax.set_ylabel('First purchase cohort',
              fontsize=10, color='#6b7280', labelpad=12)
ax.tick_params(length=0)
for spine in ax.spines.values():
    spine.set_visible(False)

cbar = plt.colorbar(im, ax=ax, shrink=0.5, pad=0.02)
cbar.set_label('Retention %', fontsize=8.5, color='#6b7280')
cbar.ax.tick_params(labelsize=8, colors='#6b7280')
cbar.outline.set_visible(False)

avg_vals = retention_pivot.mean().round(1)
for j, val in enumerate(avg_vals[:len(heat_data.columns)]):
    ax.text(j, len(heat_data) + 0.65, f'{val}%',
            ha='center', va='center',
            fontsize=8, color=ACCENT,
            fontweight='600', fontfamily='DM Sans')
ax.text(-0.65, len(heat_data) + 0.65, 'Avg',
        ha='center', va='center',
        fontsize=8, fontweight='700',
        color=ACCENT, fontfamily='DM Sans')

plt.tight_layout(pad=1.5)
st.pyplot(fig, use_container_width=True)
plt.close()

avg_day1  = retention_pivot[1].mean().round(1)
avg_day7  = retention_pivot[7].mean().round(1)  if 7  in retention_pivot.columns else 0
avg_day14 = retention_pivot[14].mean().round(1) if 14 in retention_pivot.columns else 0

col_a, col_b, col_c = st.columns(3)
col_a.metric("Avg day-1 retention",  f"{avg_day1}%")
col_b.metric("Avg day-7 retention",  f"{avg_day7}%")
col_c.metric("Avg day-14 retention", f"{avg_day14}%")

st.info(
    f"**Key insight:** Day-1 retention averages {avg_day1}% — "
    f"dropping to {avg_day7}% by day 7 and {avg_day14}% by day 14. "
    "The steep early drop suggests the highest-leverage retention "
    "window is within 24 hours of first purchase."
)

st.markdown("---")
st.markdown(
    "<p style='font-family:DM Mono,monospace;font-size:10px;"
    "color:#bbb;letter-spacing:.05em;text-align:center;padding:8px 0'>"
    "Prasanna Pingale · REES46 Multi-Category Store (Kaggle) · "
    "Python · pandas · matplotlib · Streamlit</p>",
    unsafe_allow_html=True
)