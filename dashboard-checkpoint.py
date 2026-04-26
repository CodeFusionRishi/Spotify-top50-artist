"""
Multi-page Spotify Dashboard
"""
import subprocess, sys

for pkg in ["panel", "hvplot", "holoviews", "pandas"]:
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import os
import pandas as pd
import panel as pn
import hvplot.pandas
import holoviews as hv

pn.extension(
    "tabulator", 
    design="material",
    sizing_mode="stretch_width",
    raw_css=["""
  body, .bk, .bk-root, .pn-loading, .card, 
  .bk-canvas-events, .bk-plot-wrapper,
  .panel-widget-box, .widget-box,
  .bk-toolbar, .bk-toolbar-button,
  select, input, .bk-input {
    background-color: #121212 !important;
    color: white !important;
    border-color: #1DB954 !important;
  }
  .bk-btn, .bk-btn-default {
    background-color: #1e1e1e !important;
    color: white !important;
    border: 1px solid #1DB954 !important;
  }
  option { background-color: #1e1e1e !important; color: white !important; }
  .pn-tabs-header { background: #121212 !important; }
"""]
)
hv.extension("bokeh")

# ── LOAD DATA ────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), "Spotify.csv")
df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

# ── GLOBALS ──────────────────────────────────────────────────────────────────
hv_opts = dict(
    bgcolor='#121212',
    color='#1DB954',
    fontscale=1.1,
    tools=['hover'],
    responsive=True,
    height=300
)
hv_cmap = ['#1DB954','#17a349','#0f7a35','#1ed760','#57e58a','#85eaab','#b3f0cc']

tabs = pn.Tabs(dynamic=True, sizing_mode="stretch_width")

# ── PAGE 1: HOME ─────────────────────────────────────────────────────────────
home_html = pn.pane.HTML("""
<div style="min-height:85vh; background: radial-gradient(ellipse at top, #1a3a2a 0%, 
#121212 50%, #0a0a0a 100%); display:flex; flex-direction:column; 
align-items:center; justify-content:center; padding:40px; position:relative; overflow:hidden;">
  
  <!-- Decorative blurred circles -->
  <div style="position:absolute; top:-100px; left:-100px; width:400px; height:400px;
  background:#1DB954; border-radius:50%; opacity:0.05; filter:blur(80px)"></div>
  <div style="position:absolute; bottom:-100px; right:-100px; width:500px; height:500px;
  background:#1DB954; border-radius:50%; opacity:0.05; filter:blur:100px"></div>
  
  <!-- Spotify logo circle -->
  <div style="width:120px; height:120px; background:#1DB954; border-radius:50%;
  display:flex; align-items:center; justify-content:center; margin-bottom:30px;
  box-shadow: 0 0 40px #1DB95466">
    <svg viewBox="0 0 24 24" width="60" height="60" fill="black">
      <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 
      17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779
      -.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659
      .301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38
      -.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84
      c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2
      -.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3
      .719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
    </svg>
  </div>
  
  <!-- Title -->
  <h1 style="color:#1DB954; font-size:52px; font-weight:900; margin:0; 
  text-align:center; letter-spacing:-1px">Spotify Top 50 World</h1>
  <p style="color:#aaa; font-size:18px; margin:12px 0 40px 0">
  Global Music Analytics Dashboard</p>
  
  <!-- Stats preview -->
  <div style="display:flex; gap:40px; margin-bottom:40px">
    <div style="text-align:center">
      <div style="color:#1DB954; font-size:28px; font-weight:bold">27,800</div>
      <div style="color:#aaa; font-size:12px">Data Points</div>
    </div>
    <div style="text-align:center">
      <div style="color:#1DB954; font-size:28px; font-weight:bold">556</div>
      <div style="color:#aaa; font-size:12px">Days Tracked</div>
    </div>
    <div style="text-align:center">
      <div style="color:#1DB954; font-size:28px; font-weight:bold">50</div>
      <div style="color:#aaa; font-size:12px">Songs/Day</div>
    </div>
  </div>
  
  <!-- Spotify branding -->
  <div style="position:absolute; bottom:20px; left:30px; 
  color:#1DB954; font-size:13px; font-weight:bold">Spotify Analytics</div>
</div>
""", sizing_mode='stretch_width')

home_page = pn.Column(home_html, sizing_mode='stretch_width')

# ── PAGE 2: OVERVIEW ─────────────────────────────────────────────────────────
total_tracks = df['song'].nunique()
total_artists = df['artist'].nunique()
total_dates = df['date'].nunique()
avg_popularity = round(df['popularity'].mean(), 1)

def kpi_card(label, value, subtitle):
    return f"""
    <div style="flex:1; min-width:180px; background:#1e1e1e; border:1px solid #1DB954;
    border-radius:12px; padding:20px; text-align:center; margin:8px">
      <div style="font-size:13px; color:#aaa">{label} ♫</div>
      <div style="font-size:36px; font-weight:bold; color:white">{value}</div>
      <div style="font-size:12px; color:#1DB954">{subtitle}</div>
    </div>
    """

kpi_html = f"""
<div style="display:flex; flex-wrap:wrap; gap:10px; width:100%">
    {kpi_card("Tracks", f"{total_tracks/1000:.1f}K", "Total Unique Songs")}
    {kpi_card("Artists", f"{total_artists/1000:.1f}K", "Total Unique Artists")}
    {kpi_card("Dates", str(total_dates), "Days Tracked")}
    {kpi_card("Avg Popularity", str(avg_popularity), "Mean Popularity")}
</div>
"""
kpi_row = pn.pane.HTML(kpi_html, sizing_mode="stretch_width")

chart_a_df = df.groupby('position')['popularity'].mean().reset_index()
chart_a = chart_a_df.hvplot.line(
    x='position', y='popularity', title="Average Popularity by Position",
    **hv_opts
)

chart_b_df = df.groupby('artist')['popularity'].mean().nlargest(10).sort_values().reset_index()
chart_b = chart_b_df.hvplot.barh(
    x='artist', y='popularity', title="Top 10 Artists by Popularity",
    **hv_opts
)

chart_c_df = df.groupby(['date', 'album_type']).size().reset_index(name='count')
chart_c = chart_c_df.hvplot.area(
    x='date', y='count', by='album_type', title="Total Songs by Album Type per Date",
    cmap=hv_cmap[:3], alpha=0.8,
    **hv_opts
)

# New Section 1: KPI Pipeline
pipeline_html = """
<div style="display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; width:100%; padding:20px 0;">
    <div style="background:#1e1e1e; border:1px solid #1DB954; border-radius:8px; padding:15px 30px; font-weight:bold; color:white;">27,800 Rows</div>
    <div style="color:#1DB954; font-size:24px;">→</div>
    <div style="background:#1e1e1e; border:1px solid #1DB954; border-radius:8px; padding:15px 30px; font-weight:bold; color:white;">50 Songs/Day</div>
    <div style="color:#1DB954; font-size:24px;">→</div>
    <div style="background:#1e1e1e; border:1px solid #1DB954; border-radius:8px; padding:15px 30px; font-weight:bold; color:white;">556 Days</div>
    <div style="color:#1DB954; font-size:24px;">→</div>
    <div style="background:#1e1e1e; border:1px solid #1DB954; border-radius:8px; padding:15px 30px; font-weight:bold; color:white;">Top 50 Chart</div>
</div>
"""
sec1_pipeline = pn.Column(
    pn.pane.HTML('<div style="color:#1DB954; font-size:18px; font-weight:bold; padding:10px 0">📊 KPI Pipeline</div>'),
    pn.pane.HTML(pipeline_html),
    css_classes=['card'],
    sizing_mode='stretch_width'
)

# New Section 2: Popularity Heatmap
dates_sampled = df['date'].sort_values().unique()[::7]
sampled_df = df[df['date'].isin(dates_sampled)]
sec2_heatmap_chart = sampled_df.hvplot.heatmap(
    x='date', y='position', C='popularity',
    cmap='Greens', colorbar=True,
    title='Popularity Heatmap by Position & Date',
    xlabel='Date', ylabel='Chart Position',
    bgcolor='#121212', fontscale=1.0,
    responsive=True, height=350
)
sec2_heatmap = pn.Column(
    pn.pane.HTML('<div style="color:#1DB954; font-size:18px; font-weight:bold; padding:10px 0">📊 Popularity Heatmap: Position vs Date (sampled)</div>'),
    sec2_heatmap_chart,
    css_classes=['card'],
    sizing_mode='stretch_width'
)

# New Section 3: Scatter Plot (EDA)
df['duration_min'] = df['duration_ms'] / 60000
sec3_scatter_chart = df.hvplot.scatter(
    x='duration_min', y='popularity',
    by='album_type',
    color=['#1DB954','#17a349','#85eaab'],
    alpha=0.5, size=6,
    title='Popularity vs Duration (minutes) by Album Type',
    xlabel='Duration (min)', ylabel='Popularity',
    bgcolor='#121212', fontscale=1.1,
    responsive=True, height=320,
    tools=['hover']
)
sec3_scatter = pn.Column(
    pn.pane.HTML('<div style="color:#1DB954; font-size:18px; font-weight:bold; padding:10px 0">📊 Popularity vs Duration — Scatter EDA</div>'),
    sec3_scatter_chart,
    css_classes=['card'],
    sizing_mode='stretch_width'
)

# New Section 4: EDA Summary Stats Table
eda_stats = df[['popularity','duration_ms','total_tracks','position']].describe().round(2)
eda_stats.index.name = 'Stat'
eda_stats = eda_stats.reset_index()

sec4_table = pn.widgets.Tabulator(
    eda_stats, sizing_mode='stretch_width', height=250, name='EDA Summary', theme='midnight'
)
sec4_summary = pn.Column(
    pn.pane.HTML('<div style="color:#1DB954; font-size:18px; font-weight:bold; padding:10px 0">📊 EDA Summary Statistics</div>'),
    sec4_table,
    css_classes=['card'],
    sizing_mode='stretch_width'
)

overview_page = pn.Column(
    pn.Spacer(height=20),
    kpi_row,
    pn.Spacer(height=20),
    pn.Row(chart_a, chart_b, sizing_mode='stretch_width'),
    pn.Spacer(height=20),
    chart_c,
    pn.Spacer(height=40),
    sec1_pipeline,
    pn.Spacer(height=20),
    sec2_heatmap,
    pn.Spacer(height=20),
    sec3_scatter,
    pn.Spacer(height=20),
    sec4_summary,
    sizing_mode="stretch_width"
)


# ── PAGE 3: ARTISTS ──────────────────────────────────────────────────────────
sorted_artist_list = sorted(df['artist'].unique().tolist())

album_type_filter = pn.widgets.CheckBoxGroup(
    name='',
    options=['album','single','compilation'],
    value=['album','single','compilation'],
    inline=False,
    margin=(10, 0, 10, 0)
)

artist_select = pn.widgets.Select(
    name='Artist Name',
    options=['All'] + sorted_artist_list,
    value='All',
    margin=(10, 0, 10, 0)
)

popularity_slider = pn.widgets.RangeSlider(
    name='Popularity',
    start=0, end=100,
    value=(0,100), step=1,
    margin=(10, 0, 10, 0)
)

filters_panel = pn.Column(
    pn.pane.Markdown("### **Filters**", styles={'color': '#1DB954'}),
    pn.pane.Markdown("**Album Type**", styles={'color': 'white'}),
    album_type_filter,
    artist_select,
    popularity_slider,
    css_classes=['card'],
    width=220,
    sizing_mode="fixed"
)

def get_filtered_df():
    df_filtered = df.copy()
    if artist_select.value != 'All':
        df_filtered = df_filtered[df_filtered['artist'] == artist_select.value]
    df_filtered = df_filtered[
        (df_filtered['popularity'] >= popularity_slider.value[0]) &
        (df_filtered['popularity'] <= popularity_slider.value[1]) &
        (df_filtered['album_type'].isin(album_type_filter.value))
    ]
    return df_filtered

@pn.depends(album_type_filter, artist_select, popularity_slider)
def chart1_top_duration(*args):
    df_f = get_filtered_df()
    if df_f.empty: return hv.Text(0,0,"No data").opts(bgcolor='#121212', color='white')
    df_f['duration_hrs'] = df_f['duration_ms'] / 3_600_000
    res = df_f.groupby('artist')['duration_hrs'].sum().nlargest(10).sort_values().reset_index()
    return res.hvplot.barh(x='artist', y='duration_hrs', title="Top 10 Artists by Total Duration (HRS)", **hv_opts).opts(xaxis=None)

@pn.depends(album_type_filter, artist_select, popularity_slider)
def chart2_avg_pop(*args):
    df_f = get_filtered_df()
    if df_f.empty: return hv.Text(0,0,"No data").opts(bgcolor='#121212', color='white')
    res = df_f.groupby('artist')['popularity'].mean().nlargest(10).sort_values().reset_index()
    return res.hvplot.barh(x='artist', y='popularity', title="Average Popularity by Artist", **hv_opts).opts(xaxis=None)

@pn.depends(album_type_filter, artist_select, popularity_slider)
def chart3_top_tracks(*args):
    df_f = get_filtered_df()
    if df_f.empty: return hv.Text(0,0,"No data").opts(bgcolor='#121212', color='white')
    res = df_f.groupby('artist')['song'].count().nlargest(10).sort_values().reset_index()
    return res.hvplot.barh(x='artist', y='song', title="Top 10 Artists by Number of Tracks", **hv_opts).opts(xaxis=None)

@pn.depends(album_type_filter, artist_select, popularity_slider)
def chart4_tracks_pie(*args):
    df_f = get_filtered_df()
    if df_f.empty: return hv.Text(0,0,"No data").opts(bgcolor='#121212', color='white')
    res = df_f.groupby('artist')['song'].count().nlargest(8).reset_index()
    opts = hv_opts.copy()
    if 'color' in opts:
        del opts['color']
    return res.hvplot.bar(x='artist', y='song', title="Total Tracks by Artist", color='artist', cmap=hv_cmap, legend=False, rot=45, **opts).opts(bgcolor='#121212', xaxis=None)

@pn.depends(album_type_filter, artist_select, popularity_slider)
def chart5_scatter(*args):
    df_f = get_filtered_df()
    if df_f.empty: return hv.Text(0,0,"No data").opts(bgcolor='#121212', color='white')
    df_f['duration_min'] = df_f['duration_ms'] / 60000
    res = df_f.groupby(['song', 'album_type']).agg({'duration_min': 'mean', 'popularity': 'mean'}).reset_index()
    return res.hvplot.scatter(x='duration_min', y='popularity', by='album_type', title="Avg Popularity and Avg Duration by Song", cmap=hv_cmap[:3], alpha=0.6, **hv_opts).opts(bgcolor='#121212')

@pn.depends(album_type_filter, artist_select, popularity_slider)
def chart6_pop_time(*args):
    df_f = get_filtered_df()
    if df_f.empty: return hv.Text(0,0,"No data").opts(bgcolor='#121212', color='white')
    top5 = df_f['artist'].value_counts().nlargest(5).index
    res = df_f[df_f['artist'].isin(top5)].groupby(['date', 'artist'])['popularity'].mean().reset_index()
    return res.hvplot.line(x='date', y='popularity', by='artist', title="Popularity Over Time by Top 5 Artists", cmap=hv_cmap[:5], **hv_opts).opts(bgcolor='#121212')

chart_grid = pn.GridBox(
    chart1_top_duration, chart2_avg_pop, chart3_top_tracks,
    chart4_tracks_pie, chart5_scatter, chart6_pop_time,
    ncols=3, sizing_mode='stretch_width'
)

artists_page = pn.Row(
    filters_panel,
    pn.Spacer(width=20),
    chart_grid,
    sizing_mode="stretch_width"
)


# ── FINAL ASSEMBLY ───────────────────────────────────────────────────────────
tabs.append(('🏠 Home', home_page))
tabs.append(('📊 Overview', overview_page))
tabs.append(('🎤 Artists', artists_page))

template = pn.template.FastListTemplate(
    title='Spotify Top 50 World',
    main=[tabs],
    accent_base_color='#1DB954',
    header_background='#1DB954',
    theme='dark',
    main_max_width='100%',
)
template.servable()
