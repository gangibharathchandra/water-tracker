"""
Data services for the Complaint Map feature.
Handles loading, filtering, statistics, and marker preparation.
"""

from datetime import datetime
from typing import Any

import pandas as pd

from database import get_all_complaints
from marker_styles import get_marker_style

_CACHE: dict[str, Any] = {}
_CACHE_TTL_SECONDS = 5


def load_complaints(force: bool = False) -> pd.DataFrame:
    now = datetime.now()
    last = _CACHE.get('complaints_ts')
    if not force and last is not None:
        elapsed = (now - last).total_seconds()
        if elapsed < _CACHE_TTL_SECONDS:
            return _CACHE['complaints_df']

    df = get_all_complaints()
    if df is None or df.empty:
        df = pd.DataFrame()

    _CACHE['complaints_df'] = df
    _CACHE['complaints_ts'] = now
    return df


def compute_stats(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {
            'total': 0,
            'pending': 0,
            'resolved': 0,
            'rejected': 0,
            'in_progress': 0,
            'critical': 0,
            'today': 0,
            'with_coords': 0,
        }

    total = len(df)
    resolved = int((df['Status'] == 'Resolved').sum()) if 'Status' in df.columns else 0
    rejected = int((df['Status'] == 'Rejected').sum()) if 'Status' in df.columns else 0
    in_progress = int((df['Status'] == 'In Progress').sum()) if 'Status' in df.columns else 0
    pending = total - resolved - rejected - in_progress

    priority_col = None
    for col in ['Priority', 'priority']:
        if col in df.columns:
            priority_col = col
            break

    critical = 0
    if priority_col:
        critical = int(df[priority_col].str.lower().isin(['emergency', 'high']).sum())

    today_count = 0
    time_col = None
    for col in ['Time', 'time', 'Created', 'created_at']:
        if col in df.columns:
            time_col = col
            break
    if time_col:
        today_str = datetime.now().strftime('%Y-%m-%d')
        today_count = int(df[time_col].astype(str).str.contains(today_str).sum())

    with_coords = 0
    lat_col = 'Latitude' if 'Latitude' in df.columns else 'latitude'
    lng_col = 'Longitude' if 'Longitude' in df.columns else 'longitude'
    if lat_col in df.columns and lng_col in df.columns:
        valid = df[lat_col].notna() & df[lng_col].notna()
        with_coords = int(valid.sum())

    return {
        'total': total,
        'pending': pending,
        'resolved': resolved,
        'rejected': rejected,
        'in_progress': in_progress,
        'critical': critical,
        'today': today_count,
        'with_coords': with_coords,
    }


_DEMO_COORDS = [
    (17.3850, 78.4867),  # Hyderabad Central
    (17.4435, 78.3772),  # HITEC City
    (17.4459, 78.3475),  # Gachibowli
    (17.4447, 78.3854),  # Madhapur
    (17.4857, 78.4030),  # Kukatpally
    (17.4377, 78.4480),  # Ameerpet
    (17.4196, 78.4370),  # Banjara Hills
    (17.4319, 78.4076),  # Jubilee Hills
    (17.4399, 78.4983),  # Secunderabad
    (17.3616, 78.4747),  # Charminar
]


def get_markers_data(df: pd.DataFrame) -> list[dict[str, Any]]:
    if df.empty:
        return []

    lat_col = 'Latitude' if 'Latitude' in df.columns else 'latitude'
    lng_col = 'Longitude' if 'Longitude' in df.columns else 'longitude'
    if lat_col not in df.columns or lng_col not in df.columns:
        return []

    markers = []
    demo_idx = 0
    for _, row in df.iterrows():
        lat = row.get(lat_col)
        lng = row.get(lng_col)
        is_demo = False
        if pd.isna(lat) or pd.isna(lng):
            if not _DEMO_COORDS:
                continue
            lat, lng = _DEMO_COORDS[demo_idx % len(_DEMO_COORDS)]
            demo_idx += 1
            is_demo = True

        issue = str(row.get('Issue', row.get('issue', '')))
        status = str(row.get('Status', row.get('status', 'Pending')))
        style = get_marker_style(issue, status)

        markers.append(
            {
                'lat': float(lat),
                'lng': float(lng),
                'id': row.get('id', row.get('ID', '')),
                'issue': issue,
                'status': status,
                'priority': row.get('Priority', row.get('priority', '')),
                'name': row.get('Name', row.get('name', '')),
                'phone': row.get('Phone', row.get('phone', '')),
                'location': row.get('Location', row.get('location', '')),
                'description': row.get('Description', row.get('description', '')),
                'time': row.get('Time', row.get('time', '')),
                'department': row.get('Department', row.get('department', '')),
                'marker_color': style.folium_color,
                'marker_icon': style.icon,
                'ai_status': row.get('AI Status', ''),
                'progress': row.get('Progress', 0),
                'is_demo_coord': is_demo,
            }
        )

    return markers


def filter_complaints(
    df: pd.DataFrame,
    status_filter: str | None = None,
    category_filter: str | None = None,
    priority_filter: str | None = None,
    search_text: str | None = None,
) -> pd.DataFrame:
    if df.empty:
        return df

    result = df.copy()

    if status_filter and status_filter != 'All':
        status_col = 'Status' if 'Status' in df.columns else 'status'
        if status_col in result.columns:
            result = result[result[status_col].str.lower() == status_filter.lower()]

    if category_filter and category_filter != 'All':
        issue_col = 'Issue' if 'Issue' in df.columns else 'issue'
        if issue_col in result.columns:
            result = result[result[issue_col].str.lower().str.contains(category_filter.lower())]

    if priority_filter and priority_filter != 'All':
        pri_col = 'Priority' if 'Priority' in df.columns else 'priority'
        if pri_col in result.columns:
            result = result[result[pri_col].str.lower() == priority_filter.lower()]

    if search_text:
        text = search_text.lower()
        search_cols = [
            col for col in ['Issue', 'Location', 'Name', 'Description', 'Department'] if col in result.columns
        ]
        if search_cols:
            mask = result[search_cols[0]].astype(str).str.lower().str.contains(text, na=False)
            for col in search_cols[1:]:
                mask |= result[col].astype(str).str.lower().str.contains(text, na=False)
            result = result[mask]

    return result


def invalidate_cache() -> None:
    _CACHE.pop('complaints_df', None)
    _CACHE.pop('complaints_ts', None)
