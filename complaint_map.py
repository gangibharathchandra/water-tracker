"""
Complaint Map — real-time interactive GIS visualization of all complaints.
Uses Folium + streamlit-folium + OpenStreetMap with clustering, heatmap,
stats cards, filters, and auto-refresh.
"""

from typing import Any

import folium
import streamlit as st
from folium.plugins import Fullscreen, HeatMap, MarkerCluster
from streamlit_folium import folium_static

from map_services import (
    compute_stats,
    filter_complaints,
    get_markers_data,
    invalidate_cache,
    load_complaints,
)
from marker_styles import CATEGORY_STYLES, STATUS_STYLES

_DEFAULT_CENTER = [20.5937, 78.9629]
_DEFAULT_ZOOM = 5
_REFRESH_INTERVAL = 10

_CSS = """
<style>
.map-title {
  font-family: 'Nunito', sans-serif;
  font-weight: 900;
  font-size: 2rem;
  margin-bottom: 0.25rem;
}
.map-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.9rem;
  color: var(--clay-muted, #635F69);
  margin-bottom: 1rem;
}
.stats-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}
.stat-card {
  flex: 1;
  min-width: 100px;
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,0.8);
  border-radius: 20px;
  padding: 14px 18px;
  box-shadow: 8px 8px 16px rgba(160,150,180,0.15), -6px -6px 12px rgba(255,255,255,0.7);
  transition: all 250ms ease;
  text-align: center;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 10px 10px 20px rgba(160,150,180,0.2), -8px -8px 16px rgba(255,255,255,0.8);
}
.stat-value {
  font-family: 'Nunito', sans-serif;
  font-weight: 900;
  font-size: 1.8rem;
  line-height: 1.2;
  color: #332F3A;
}
.stat-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  color: #635F69;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.stat-card.critical .stat-value { color: #DB2777; }
.stat-card.pending .stat-value { color: #F59E0B; }
.stat-card.resolved .stat-value { color: #10B981; }
.stat-card.today .stat-value { color: #7C3AED; }

.filter-container {
  background: rgba(255,255,255,0.5);
  backdrop-filter: blur(16px);
  border-radius: 24px;
  padding: 16px 20px;
  margin-bottom: 16px;
  box-shadow: 6px 6px 12px rgba(160,150,180,0.1), -4px -4px 8px rgba(255,255,255,0.5);
  border: 1px solid rgba(255,255,255,0.6);
}

.legend-container {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(12px);
  border-radius: 20px;
  padding: 14px 18px;
  box-shadow: 4px 4px 12px rgba(160,150,180,0.12);
  border: 1px solid rgba(255,255,255,0.6);
  margin-top: 12px;
}
.legend-title {
  font-family: 'Nunito', sans-serif;
  font-weight: 800;
  font-size: 0.85rem;
  margin-bottom: 8px;
  color: #332F3A;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 3px 0;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.8rem;
  color: #332F3A;
}
.legend-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
  border: 2px solid rgba(255,255,255,0.8);
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}

.placeholder-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  background: rgba(255,255,255,0.6);
  backdrop-filter: blur(16px);
  border-radius: 40px;
  box-shadow: 12px 12px 24px rgba(160,150,180,0.15), -8px -8px 16px rgba(255,255,255,0.6);
  margin: 20px 0;
}
.placeholder-icon {
  font-size: 4rem;
  margin-bottom: 16px;
  opacity: 0.4;
}
.placeholder-title {
  font-family: 'Nunito', sans-serif;
  font-weight: 800;
  font-size: 1.5rem;
  color: #332F3A;
  margin-bottom: 8px;
}
.placeholder-text {
  font-family: 'DM Sans', sans-serif;
  font-size: 1rem;
  color: #635F69;
  max-width: 400px;
}

.control-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-bottom: 12px;
}

@media (max-width: 640px) {
  .stats-row { gap: 8px; }
  .stat-card { min-width: 80px; padding: 10px 12px; }
  .stat-value { font-size: 1.3rem; }
}
</style>
"""


def _render_stats_cards(stats: dict[str, Any]) -> None:
    cards = [
        ('total', 'Total', str(stats['total']), ''),
        ('pending', 'Pending', str(stats['pending']), 'pending'),
        ('resolved', 'Resolved', str(stats['resolved']), 'resolved'),
        ('critical', 'Critical', str(stats['critical']), 'critical'),
        ('today', 'Today', str(stats['today']), 'today'),
    ]

    html = '<div class="stats-row">'
    for _key, label, value, variant in cards:
        cls = f'stat-card {variant}' if variant else 'stat-card'
        html += f'<div class="{cls}"><div class="stat-value">{value}</div><div class="stat-label">{label}</div></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def _render_legend() -> None:
    html = '<div class="legend-container"><div class="legend-title">Legend</div>'
    for cat, style in CATEGORY_STYLES.items():
        html += (
            f'<div class="legend-item"><span class="legend-dot" style="background:{style.color};"></span>{cat}</div>'
        )
    for status, style in STATUS_STYLES.items():
        html += (
            f'<div class="legend-item"><span class="legend-dot" style="background:{style.color};"></span>{status}</div>'
        )
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def _build_map(markers: list[dict[str, Any]]) -> folium.Map:
    if markers:
        center_lat = sum(m['lat'] for m in markers) / len(markers)
        center_lng = sum(m['lng'] for m in markers) / len(markers)
        zoom = 10
    else:
        center_lat, center_lng = _DEFAULT_CENTER
        zoom = _DEFAULT_ZOOM

    m = folium.Map(
        location=[center_lat, center_lng],
        zoom_start=zoom,
        tiles='OpenStreetMap',
        attr='© OpenStreetMap contributors',
        control_scale=True,
    )

    Fullscreen(position='topright').add_to(m)

    if markers:
        cluster = MarkerCluster(name='Complaints', options={'maxClusterRadius': 50})
        for mk in markers:
            popup_html = _build_popup(mk)
            popup = folium.Popup(popup_html, max_width=350)

            color = mk.get('marker_color', 'lightgray')
            icon_name = mk.get('marker_icon', 'info-circle')

            folium.Marker(
                location=[mk['lat'], mk['lng']],
                popup=popup,
                tooltip=mk.get('issue', 'Complaint'),
                icon=folium.Icon(color=color, icon=icon_name, prefix='fa'),
            ).add_to(cluster)

        cluster.add_to(m)

        heat_data = [[mk['lat'], mk['lng']] for mk in markers]
        if heat_data:
            HeatMap(
                heat_data,
                radius=20,
                blur=15,
                max_zoom=1,
                gradient={0.4: '#7C3AED', 0.65: '#DB2777', 1: '#FF4444'},
            ).add_to(m)

    folium.LayerControl().add_to(m)

    return m


def _build_popup(mk: dict[str, Any]) -> str:
    issue = mk.get('issue', 'N/A')
    status = mk.get('status', 'N/A')
    name = mk.get('name', '')
    phone = mk.get('phone', '')
    location = mk.get('location', '')
    description = mk.get('description', '')
    time_val = mk.get('time', '')
    priority = mk.get('priority', '')
    dept = mk.get('department', '')
    ai_status = mk.get('ai_status', '')
    progress = mk.get('progress', 0)
    lat = mk.get('lat', '')
    lng = mk.get('lng', '')
    cid = mk.get('id', '')
    is_demo = mk.get('is_demo_coord', False)

    status_color = mk.get('marker_color', '#333')

    html = f"""
    <div style="min-width:260px;font-family:'DM Sans',sans-serif;">
      <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:8px;">
        <div style="font-family:'Nunito',sans-serif;font-weight:800;font-size:1rem;color:#332F3A;line-height:1.3;">
          {issue}
        </div>
        <span style="display:inline-block;background:{status_color};color:white;padding:2px 10px;border-radius:20px;font-size:0.7rem;font-weight:700;white-space:nowrap;margin-left:8px;">
          {status}
        </span>
      </div>
      <div style="border-top:1px solid #E8E6EE;margin:6px 0;"></div>
      <table style="width:100%;font-size:0.78rem;border-collapse:collapse;">
    """

    def add_row(label, value):
        if value:
            return f"<tr><td style='padding:2px 6px 2px 0;color:#635F69;font-weight:600;width:80px;vertical-align:top;'>{label}</td><td style='padding:2px 0;color:#332F3A;'>{value}</td></tr>"
        return ''

    html += add_row('ID', f'#{cid}')
    html += add_row('Citizen', name)
    if phone:
        html += add_row('Phone', phone)
    loc_display = (
        location
        if location and location.strip().lower() not in ('not specified', 'not mentioned', '')
        else 'Not specified'
    )
    if is_demo:
        loc_display += ' ⚠️ approx'
    html += add_row('Area', loc_display)
    html += add_row('Priority', priority)
    html += add_row('Department', dept)
    html += add_row('Reported', time_val)
    html += add_row('AI Status', ai_status)
    if progress:
        html += add_row('Progress', f'{progress}%')

    if description:
        html += f"""<tr><td style='padding:2px 6px 2px 0;color:#635F69;font-weight:600;width:80px;vertical-align:top;'>Issue</td>
        <td style='padding:2px 0;color:#332F3A;font-size:0.75rem;line-height:1.4;'>{description}</td></tr>"""

    coord_label = f'{lat:.4f}, {lng:.4f}'
    if is_demo:
        coord_label += ' ⚠️ approx'
    html += add_row('Coords', coord_label)

    nav_url = f'https://www.openstreetmap.org/directions?from=&to={lat}%2C{lng}'

    html += '</table>'
    html += f'<div style="margin-top:8px;display:flex;gap:6px;"><a href="{nav_url}" target="_blank" style="flex:1;display:inline-block;padding:7px 0;background:#7C3AED;color:white;border-radius:12px;text-decoration:none;font-size:0.78rem;font-weight:700;text-align:center;">🗺️ Navigate</a></div>'
    html += '</div>'
    return html


def render_complaint_map() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)

    st.markdown('<div class="map-title">🗺️ Complaint Map</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="map-subtitle">Real-time GIS visualization of all water complaints across the region</div>',
        unsafe_allow_html=True,
    )

    if 'map_auto_refresh' not in st.session_state:
        st.session_state.map_auto_refresh = False
    if 'map_show_heatmap' not in st.session_state:
        st.session_state.map_show_heatmap = False

    col_refresh, col_filter, col_heat, col_spacer = st.columns([1, 1, 1, 3])
    with col_refresh:
        auto_on = st.toggle(
            'Auto-refresh (10s)',
            value=st.session_state.map_auto_refresh,
            key='map_auto_refresh_toggle',
        )
        st.session_state.map_auto_refresh = auto_on
    with col_filter:
        if st.button('⟳ Refresh Now', use_container_width=True):
            invalidate_cache()
            st.rerun()
    with col_heat:
        heat_on = st.toggle(
            'Heatmap',
            value=st.session_state.map_show_heatmap,
            key='map_heatmap_toggle',
        )
        st.session_state.map_show_heatmap = heat_on

    df = load_complaints()
    stats = compute_stats(df)

    _render_stats_cards(stats)

    with st.expander('🔍 Filters & Search', expanded=False):
        fcol1, fcol2, fcol3, fcol4 = st.columns(4)
        with fcol1:
            status_options = ['All', 'Pending', 'Resolved', 'In Progress', 'Rejected']
            status_filter = st.selectbox('Status', status_options, key='map_filter_status')
        with fcol2:
            cat_options = ['All'] + sorted(CATEGORY_STYLES.keys())
            category_filter = st.selectbox('Category', cat_options, key='map_filter_cat')
        with fcol3:
            pri_options = ['All', 'Emergency', 'High', 'Medium', 'Low']
            priority_filter = st.selectbox('Priority', pri_options, key='map_filter_pri')
        with fcol4:
            search_text = st.text_input('Search (ID, name, area...)', key='map_search')

    filtered_df = filter_complaints(df, status_filter, category_filter, priority_filter, search_text)
    markers = get_markers_data(filtered_df)

    total_complaints = stats.get('total', 0)
    coords_count = stats.get('with_coords', 0)

    if markers:
        st.markdown(
            f'<div style="font-family:DM Sans,sans-serif;font-size:0.85rem;color:#635F69;margin-bottom:8px;">'
            f'Showing {len(markers)} complaint(s) on map</div>',
            unsafe_allow_html=True,
        )
    else:
        if df.empty:
            st.markdown(
                '<div class="placeholder-card">'
                '<div class="placeholder-icon">🗺️</div>'
                '<div class="placeholder-title">No Complaints Yet</div>'
                '<div class="placeholder-text">Currently no complaints reported. '
                'New complaints will appear here automatically.</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        elif coords_count == 0 and total_complaints > 0:
            st.warning(
                f'There are {total_complaints} complaint(s) in the system, but none have a valid '
                'location specified. Markers can only appear when location details and '
                'coordinates are provided during complaint submission.'
            )
        else:
            st.info('No complaints match the current filters. Try adjusting your filter criteria.')

    m = _build_map(markers)
    folium_static(m, width=None, height=520)

    col_map_leg, col_map_info = st.columns([1, 1])
    with col_map_leg:
        _render_legend()
    with col_map_info:
        if markers:
            coords_count = stats.get('with_coords', 0)
            total = stats.get('total', 0)
            demo_note = ''
            if coords_count < total:
                demo_note = f'<div>🎯 {total - coords_count} with demo coordinates</div>'
            st.markdown(
                f'<div class="legend-container">'
                f'<div class="legend-title">Map Statistics</div>'
                f'<div style="font-family:DM Sans,sans-serif;font-size:0.85rem;color:#635F69;">'
                f'<div>📍 {len(markers)} marker(s) displayed</div>'
                f'<div>📊 {coords_count}/{total} with stored coordinates</div>'
                f'{demo_note}'
                f'<div>🔄 Auto-refresh: {"ON" if auto_on else "OFF"}</div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

    if auto_on:
        refresh_placeholder = st.empty()
        refresh_placeholder.markdown(
            f'<div style="font-family:DM Sans,sans-serif;font-size:0.75rem;color:#635F69;text-align:center;padding:4px;">'
            f'⏳ Auto-refreshing every {_REFRESH_INTERVAL}s</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<meta http-equiv="refresh" content="{_REFRESH_INTERVAL}">',
            unsafe_allow_html=True,
        )
