"""
Marker style definitions for the Complaint Map feature.
Defines colors, icons, and visual treatments per complaint category and status.
"""

from dataclasses import dataclass


@dataclass
class MarkerStyle:
    color: str
    folium_color: str
    icon: str
    icon_prefix: str = 'fa'
    description: str = ''


CATEGORY_STYLES: dict[str, MarkerStyle] = {
    'Water Leakage': MarkerStyle(
        color='#FF4444',
        folium_color='red',
        icon='tint',
        description='Active water leakage reported',
    ),
    'Dirty Water': MarkerStyle(
        color='#FFD700',
        folium_color='orange',
        icon='exclamation-triangle',
        description='Contaminated or discolored water',
    ),
    'No Water': MarkerStyle(
        color='#FF8C00',
        folium_color='darkred',
        icon='ban',
        description='Complete water supply disruption',
    ),
    'Pipe Burst': MarkerStyle(
        color='#2196F3',
        folium_color='blue',
        icon='wrench',
        description='Burst or broken water pipe',
    ),
    'Low Pressure': MarkerStyle(
        color='#9C27B0',
        folium_color='purple',
        icon='arrow-down',
        description='Insufficient water pressure',
    ),
    'Contamination': MarkerStyle(
        color='#FF5722',
        folium_color='darkpurple',
        icon='biohazard',
        description='Water quality contamination',
    ),
    'Billing Issue': MarkerStyle(
        color='#607D8B',
        folium_color='gray',
        icon='file-invoice-dollar',
        description='Billing or payment related',
    ),
    'Other water issue': MarkerStyle(
        color='#795548',
        folium_color='lightgray',
        icon='question-circle',
        description='Uncategorized water issue',
    ),
}

STATUS_STYLES: dict[str, MarkerStyle] = {
    'Resolved': MarkerStyle(
        color='#4CAF50',
        folium_color='green',
        icon='check-circle',
        description='Issue has been resolved',
    ),
    'Rejected': MarkerStyle(
        color='#000000',
        folium_color='black',
        icon='times-circle',
        description='Complaint was rejected',
    ),
    'In Progress': MarkerStyle(
        color='#FF9800',
        folium_color='orange',
        icon='spinner',
        description='Work is in progress',
    ),
    'Pending': MarkerStyle(
        color='#FFC107',
        folium_color='beige',
        icon='clock',
        description='Waiting for assignment or action',
    ),
}


def get_marker_style(
    issue_type: str = '',
    status: str = '',
) -> MarkerStyle:
    if status and status.lower() in ('resolved',):
        return STATUS_STYLES.get('Resolved', STATUS_STYLES['Resolved'])
    if status and status.lower() in ('rejected',):
        return STATUS_STYLES.get('Rejected', STATUS_STYLES['Rejected'])

    normalized = issue_type.strip().title() if issue_type else ''
    for key, style in CATEGORY_STYLES.items():
        if key.lower() == normalized.lower():
            return style
    for key, style in CATEGORY_STYLES.items():
        if key.split(' (')[0].lower() == normalized.lower():
            return style

    return MarkerStyle(
        color='#795548',
        folium_color='lightgray',
        icon='question-circle',
        description='Unknown issue type',
    )


def get_status_style(status: str) -> MarkerStyle:
    normalized = status.strip().title() if status else ''
    for key, style in STATUS_STYLES.items():
        if key.lower() == normalized.lower():
            return style
    return MarkerStyle(
        color='#FFC107',
        folium_color='beige',
        icon='clock',
        description=status or 'Unknown',
    )


def get_category_color_list() -> list[tuple[str, str]]:
    result = []
    for category, style in CATEGORY_STYLES.items():
        result.append((category, style.color))
    for status, style in STATUS_STYLES.items():
        result.append((status, style.color))
    return result
