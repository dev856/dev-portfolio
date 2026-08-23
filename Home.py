from __future__ import annotations

import base64
import html
import sqlite3
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent
EMAIL = "devhkotak@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/dev-kotak/"
GITHUB = "https://github.com/dev856"
LOCATION = "Ottawa, Ontario, Canada"

NAV_ITEMS = [
    "Overview",
    "About",
    "Projects",
    "Experience",
    "Skills",
    "Education",
    "Testimonials",
    "Résumé",
    "Contact",
]

MIME_BY_SUFFIX = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".pdf": "application/pdf",
}

# Razor-sharp Lucide Vector SVG Icon Definitions
SVG_ICONS = {
    "cpu": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/></svg>',
    "brain": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v13"/><path d="M6 12h12"/></svg>',
    "eye": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>',
    "layers": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.9a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 12.5-9.17 4.16a2 2 0 0 1-1.66 0L2 12.5"/><path d="m22 17.5-9.17 4.16a2 2 0 0 1-1.66 0L2 17.5"/></svg>',
    "briefcase": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>',
    "graduation": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/></svg>',
    "target": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "award": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>',
    "code": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    "terminal": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="4 17 10 11 4 5"/><line x1="12" x2="20" y1="19" y2="19"/></svg>',
    "database": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/></svg>',
    "sparkles": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>',
    "star": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "message": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>',
    "user": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "file_text": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>',
    "mail": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
    "map_pin": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>',
    "calendar": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>',
    "external": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>',
    "github": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>',
    "linkedin": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>',
    "check": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "send": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>',
    "zap": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "activity": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
    "book": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 6h10"/><path d="M6 10h10"/></svg>',
    "rocket": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/></svg>',
    "lightbulb": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>',
    "users": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "quote": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z"/><path d="M5 3a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2 1 1 0 0 1 1 1v1a2 2 0 0 1-2 2 1 1 0 0 0-1 1v2a1 1 0 0 0 1 1 6 6 0 0 0 6-6V5a2 2 0 0 0-2-2z"/></svg>',
    "globe": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>',
    "download": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>',
    "atom": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="1"/><path d="M20.2 20.2c2.04-2.03.02-7.36-4.5-11.9-4.54-4.52-9.87-6.54-11.9-4.5-2.04 2.03-.02 7.36 4.5 11.9 4.54 4.52 9.87 6.54 11.9 4.5Z"/><path d="M15.7 15.7c4.52-4.54 6.54-9.87 4.5-11.9-2.03-2.04-7.36-.02-11.9 4.5-4.52 4.54-6.54 9.87-4.5 11.9 2.03 2.04 7.36.02 11.9-4.5Z"/></svg>',
    "workflow": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="8" height="8" x="3" y="3" rx="2"/><path d="M7 11v4a2 2 0 0 0 2 2h4"/><rect width="8" height="8" x="13" y="13" rx="2"/></svg>',
    "satellite_dish": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 10a7.31 7.31 0 0 0 10 10z"/><path d="m9 15 3-3"/><path d="M17 13a6 6 0 0 0-6-6"/><path d="M21 13A10 10 0 0 0 11 3"/><rect x="13" y="15" width="6" height="6" rx="2" transform="rotate(45 16 18)"/></svg>',
    "flask_conical": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2"/><path d="M6.453 15h11.094"/><path d="M8.5 2h7"/></svg>',
    "gauge": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/></svg>',
    "shield_check": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>',
    "trending_up": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    "git_branch": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="6" x2="6" y1="3" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>',
    "cloud": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>',
    "medal": '<svg class="svg-icon" xmlns="http://www.w3.org/2000/svg" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15"/><path d="M11 12 5.12 2.2"/><path d="m13 12 5.88-9.8"/><path d="M8 7h8"/><circle cx="12" cy="17" r="5"/><path d="M12 18v-2h-.5"/></svg>',
}


def svg_icon(name: str, size: int = 18) -> str:
    """Return pure inline vector SVG markup."""
    template = SVG_ICONS.get(name, SVG_ICONS["zap"])
    return template.format(s=size)


def icon_box(name: str, size: int = 20, sm: bool = False) -> str:
    """Return a styled glowing frosted glass vector icon badge."""
    cls = "icon-box sm" if sm else "icon-box"
    return f'<span class="{cls}">{svg_icon(name, size)}</span>'


st.set_page_config(
    page_title="Dev Kotak · Software & Machine Learning Engineer",
    page_icon=str(ROOT / "assets" / "phot.jpeg") if (ROOT / "assets" / "phot.jpeg").exists() else "⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_db() -> None:
    """Initialize SQLite database to safely preserve contact form inquiries."""
    try:
        db_path = ROOT / "portfolio_contacts.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT,
                message TEXT NOT NULL,
                submitted_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def save_inquiry(name: str, email_address: str, subject: str, message: str) -> bool:
    """Save an incoming contact inquiry to the database."""
    try:
        db_path = ROOT / "portfolio_contacts.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO inquiries (name, email, subject, message, submitted_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, email_address, subject, message, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def safe(value: object) -> str:
    """Escape HTML content safely."""
    return html.escape(str(value), quote=True)


def as_data_uri(path: Path) -> str | None:
    """Convert a file into an inline base64 Data URI for fast, zero-flicker loading."""
    if not path.exists():
        return None
    mime = MIME_BY_SUFFIX.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def initials(name: str) -> str:
    words = [w for w in name.split() if w]
    return "".join(w[0].upper() for w in words[:2]) or "?"


def tag_row(items: list[str]) -> None:
    markup = " ".join(f'<span class="tag">{safe(item)}</span>' for item in items)
    st.markdown(f'<div class="tag-row">{markup}</div>', unsafe_allow_html=True)


def tag_html(items: list[str]) -> str:
    return " ".join(f'<span class="tag">{safe(item)}</span>' for item in items)


def render_gif_strip() -> None:
    """Render animated demo GIFs dropped into images/gifs/ as an 'in motion' gallery."""
    gif_dir = ROOT / "images" / "gifs"
    if not gif_dir.exists():
        return
    gifs = sorted(p for p in gif_dir.iterdir() if p.suffix.lower() in {".gif", ".webp"})
    if not gifs:
        return
    frames = "".join(
        f'<figure class="gif-frame"><img src="{as_data_uri(p)}" alt="{safe(p.stem)}" loading="lazy" />'
        f"<figcaption>{svg_icon('sparkles', 12)} {safe(p.stem.replace('-', ' ').replace('_', ' '))}</figcaption></figure>"
        for p in gifs
    )
    st.markdown("## Studio in Motion")
    st.markdown('<div class="gif-strip">' + frames + "</div>", unsafe_allow_html=True)


def terminal_widget() -> None:
    """Animated live-console card with typing command, status log, and equalizer."""
    cmd = "python run dev_kotak --mode=production"
    eq_bars = "".join("<span></span>" for _ in range(14))
    st.markdown(
        f"""
        <div class="terminal-card">
          <div class="terminal-bar">
            <span class="tdot r"></span><span class="tdot y"></span><span class="tdot g"></span>
            <span class="terminal-title">{svg_icon('terminal', 12)} dev@portfolio: ~/engine</span>
            <span class="terminal-live"><span class="livedot"></span>LIVE</span>
          </div>
          <pre class="terminal-body"><span class="tline"><span class="tprompt">$</span> <span class="typing">{cmd}</span></span><span class="tline"><span class="tok-ok">[ok]</span> models compiled · vision · nlp · ensembles</span><span class="tline"><span class="tok-info">[info]</span> serving interactive experience <span class="cursor">▊</span></span></pre>
          <div class="terminal-eq">{eq_bars}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Safe navigation state handler to avoid widget modification exception
if "target_nav" in st.session_state and st.session_state.target_nav:
    st.session_state.nav = st.session_state.target_nav
    st.session_state.target_nav = None

if "nav" not in st.session_state or st.session_state.nav not in NAV_ITEMS:
    st.session_state.nav = "Overview"


def set_page(name: str) -> None:
    """Helper to trigger navigation safely without widget instantiation conflict."""
    for item in NAV_ITEMS:
        if name.lower() in item.lower():
            st.session_state.target_nav = item
            st.rerun()
            return
    st.session_state.target_nav = name
    st.rerun()


def section_header(kicker: str, title: str, description: str | None = None, icon_name: str = "zap") -> None:
    st.markdown(f'<p class="section-kicker">{svg_icon(icon_name, 14)} {safe(kicker)}</p>', unsafe_allow_html=True)
    st.title(title)
    if description:
        st.markdown(f'<p class="section-description">{safe(description)}</p>', unsafe_allow_html=True)


def site_footer() -> None:
    st.markdown(
        f"""
        <footer class="site-footer">
          <div>
            <span>{svg_icon("zap", 14)} <strong>Dev Kotak</strong></span> · <span>Software &amp; Machine Learning Engineer</span> · <span>{svg_icon("map_pin", 13)} {LOCATION}</span>
          </div>
          <div class="site-footer-links">
            <a href="{LINKEDIN}" target="_blank" rel="noreferrer">{svg_icon("linkedin", 13)} LinkedIn</a>
            <a href="{GITHUB}" target="_blank" rel="noreferrer">{svg_icon("github", 13)} GitHub</a>
            <a href="mailto:{EMAIL}">{svg_icon("mail", 13)} Email</a>
          </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def timeline_item(role: dict[str, object]) -> None:
    company = str(role["company"])
    logo = role.get("logo")
    if logo and (ROOT / str(logo)).exists():
        uri = as_data_uri(ROOT / str(logo))
        logo_html = f'<img class="timeline-logo" src="{uri}" alt="{safe(company)}" />' if uri else ""
    else:
        logo_html = f'<span class="timeline-logo timeline-logo-fallback">{initials(company)}</span>'
    bullets = "".join(f"<li><span class=\"bullet-icon\">{svg_icon('check', 10)}</span> <span>{safe(b)}</span></li>" for b in role["bullets"])
    st.markdown(
        f"""
        <div class="timeline-item">
          <span class="timeline-marker"></span>
          <div class="timeline-card">
            <div class="timeline-head">
              {logo_html}
              <div class="timeline-title">
                <h3>{safe(role['role'])}</h3>
                <p class="company">{safe(company)}</p>
              </div>
              <span class="date-pill">{svg_icon('calendar', 12)} {safe(role['date'])}</span>
            </div>
            <p class="summary">{safe(role['summary'])}</p>
            <ul class="timeline-bullets">{bullets}</ul>
            <div class="tag-row">{tag_html(role["tags"])}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def project_card(project: dict[str, object], image_path: str | None = None) -> None:
    with st.container(border=True):
        if image_path and (ROOT / image_path).exists():
            st.image(str(ROOT / image_path), width="stretch")
        st.markdown(f'<p class="project-type">{safe(project["type"])}</p>', unsafe_allow_html=True)
        st.subheader(str(project["title"]))
        st.write(str(project["description"]))
        st.markdown(
            f'<p class="project-outcome"><span>{svg_icon("target", 15)}</span> <span><strong>{safe(project["outcome_label"])}:</strong> {safe(project["outcome"])}</span></p>',
            unsafe_allow_html=True,
        )
        tag_row(project["tags"])

        deep_dive = project.get("deep_dive")
        if deep_dive:
            with st.expander("Technical Architecture & System Details"):
                st.write(deep_dive)

        btn_cols = st.columns(2)
        if project.get("demo"):
            with btn_cols[0]:
                st.link_button("Open Live App ↗", str(project["demo"]), width="stretch")
        if project.get("repo"):
            col_target = btn_cols[1] if project.get("demo") else btn_cols[0]
            with col_target:
                st.link_button(str(project.get("repo_label", "View GitHub ↗")), str(project["repo"]), width="stretch")


# Initialize Database
init_db()

# Inject Modern CSS Stylesheet
css_file = ROOT / "styles" / "main.css"
if css_file.exists():
    st.markdown(f"<style>{css_file.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# Inject Interactive Layer (cursor spotlight + scroll reveal)
js_file = ROOT / "styles" / "interactive.js"
if js_file.exists():
    components.html(
        f"<script>{js_file.read_text(encoding='utf-8')}</script>",
        height=0,
    )

# Prepare Assets
profile_path = ROOT / "assets" / "phot.jpeg"
resume_path = ROOT / "Resume-Dev.pdf"
if not resume_path.exists():
    resume_path = ROOT / "assets" / "Profile.pdf"

profile_uri = as_data_uri(profile_path)
resume_uri = as_data_uri(resume_path)

# Sidebar Branded Navigation with Vector Icons
with st.sidebar:
    if profile_uri:
        st.markdown(
            f"""
            <div class="brand">
              <div class="portrait sm">
                <div class="portrait-frame"><img src="{profile_uri}" alt="Dev Kotak" /></div>
              </div>
              <p class="brand-kicker">Studio · Portfolio</p>
              <h2 class="brand-name">Dev Kotak</h2>
              <p class="brand-role">Software &amp; Machine Learning Engineer</p>
              <div class="status-pill"><span class="status-dot"></span>Open to opportunities</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="brand">
              <div class="monogram">DK</div>
              <p class="brand-kicker">Studio · Portfolio</p>
              <h2 class="brand-name">Dev Kotak</h2>
              <p class="brand-role">Software &amp; Machine Learning Engineer</p>
              <div class="status-pill"><span class="status-dot"></span>Open to opportunities</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.divider()
    page = st.radio("Navigation", NAV_ITEMS, label_visibility="collapsed", key="nav")
    st.divider()
    st.caption("Available for Software Engineering, Applied Machine Learning, and Data Science appointments.")
    st.link_button("LinkedIn Profile ↗", LINKEDIN, width="stretch")
    st.link_button("GitHub Profile ↗", GITHUB, width="stretch")
    if resume_path.exists():
        st.download_button(
            "Download Résumé PDF ⤓",
            resume_path.read_bytes(),
            "Dev-Kotak-Resume.pdf",
            "application/pdf",
            width="stretch",
        )


# =========================================================================
# 1. OVERVIEW / HERO
# =========================================================================
if page == "Overview":
    st.markdown(
        f"""
        <div class="hero">
          <div class="hero-particles"><span></span><span></span><span></span><span></span><span></span><span></span><span></span><span></span></div>
          <p class="section-kicker">{svg_icon('rocket', 14)} Software &amp; Applied Machine Learning</p>
          <h1>I build <span class="gold-accent">intelligent software</span> from data, models &amp; modern web systems.</h1>
          <p class="section-description">Master of Engineering graduate in Electrical &amp; Computer Engineering (Data Science Specialization) at Carleton University. Experienced across production REST APIs, computer vision, natural language processing, and interactive data workbenches.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    hero_left, hero_right = st.columns([1.3, 0.7], vertical_alignment="center")
    with hero_left:
        st.markdown(
            """
            <div class="practice">
              <h3>Engineered for Precision &amp; Real-World Impact</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(
            "I operate across the entire software lifecycle—transforming complex datasets into production-grade predictive models, high-throughput REST APIs, and responsive, interactive applications."
        )
        st.write("")
        h_btn1, h_btn2, h_btn3 = st.columns(3)
        with h_btn1:
            if st.button("Explore Work →", key="hero_explore_btn", type="primary", width="stretch"):
                set_page("Projects")
        with h_btn2:
            if st.button("Contact Me", key="hero_contact_btn", width="stretch"):
                set_page("Contact")
        with h_btn3:
            if resume_path.exists():
                st.download_button(
                    "Download CV ⤓",
                    resume_path.read_bytes(),
                    "Dev-Kotak-Resume.pdf",
                    "application/pdf",
                    key="hero_cv_btn",
                    width="stretch",
                )

    with hero_right:
        if profile_uri:
            st.markdown(
                f"""
                <figure class="portrait hero-media">
                  <div class="portrait-frame"><img src="{profile_uri}" alt="Portrait of Dev Kotak" /></div>
                  <figcaption class="portrait-caption"><strong>Dev Kotak</strong><span>{svg_icon('map_pin', 12)} Ottawa, Canada</span></figcaption>
                </figure>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # Executive Stats Grid with Precision Vector Icons
    st.markdown(
        f"""
        <div class="stat-grid">
          <div class="stat-card">
            <div class="stat-head">
              <span class="stat-index">01</span>
              {icon_box('briefcase', 16, sm=True)}
            </div>
            <p class="stat-value">7</p>
            <p class="stat-label">Industry &amp; Research Roles</p>
          </div>
          <div class="stat-card">
            <div class="stat-head">
              <span class="stat-index">02</span>
              {icon_box('graduation', 16, sm=True)}
            </div>
            <p class="stat-value">M.Eng</p>
            <p class="stat-label">Carleton Data Science (10.5/12)</p>
          </div>
          <div class="stat-card">
            <div class="stat-head">
              <span class="stat-index">03</span>
              {icon_box('cpu', 16, sm=True)}
            </div>
            <p class="stat-value">5+</p>
            <p class="stat-label">Deployed ML &amp; Web Apps</p>
          </div>
          <div class="stat-card">
            <div class="stat-head">
              <span class="stat-index">04</span>
              {icon_box('target', 16, sm=True)}
            </div>
            <p class="stat-value">75%</p>
            <p class="stat-label">Predictive Benchmark Accuracy</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Live animated console widget
    terminal_widget()

    st.markdown('<span id="selected-work"></span>', unsafe_allow_html=True)
    st.write("")
    st.markdown("## Core Engineering Pillars")
    st.markdown(
        f"""
        <div class="pillars-grid">
          <div class="pillar-card">
            {icon_box('brain', 22)}
            <h4>Applied Machine Learning</h4>
            <p>Developing end-to-end predictive systems, ensemble meta-classifiers, and topic modeling pipelines with rigorous cross-validation and benchmark tuning.</p>
          </div>
          <div class="pillar-card">
            {icon_box('eye', 22)}
            <h4>Computer Vision &amp; AI</h4>
            <p>Deploying real-time pose estimation (MediaPipe), automated visual defect inspection, facial landmark detectors, and OpenCV image processing pipelines.</p>
          </div>
          <div class="pillar-card">
            {icon_box('layers', 22)}
            <h4>Full-Stack &amp; Systems</h4>
            <p>Designing robust RESTful architectures, low-latency JSON data workflows, relational &amp; NoSQL schemas (SQL, MongoDB), and responsive Streamlit/Web UIs.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown("## Selected Work")
    st.write("A concise showcase of production applications and applied AI solutions.")

    st.markdown(
        f"""
        <div class="mini-grid">
          <div class="mini-card">
            <div>
              <div class="mini-top">
                <span class="mini-index">01</span>
                <span class="pill-chip">{svg_icon('message', 12)} NLP</span>
              </div>
              <h3>Tone Topic</h3>
              <p>Topic modeling and document categorization for unstructured text and CSV datasets using Latent Dirichlet Allocation (LDA) and NLTK.</p>
            </div>
          </div>
          <div class="mini-card">
            <div>
              <div class="mini-top">
                <span class="mini-index">02</span>
                <span class="pill-chip">{svg_icon('eye', 12)} Vision</span>
              </div>
              <h3>Digital Yoga Trainer</h3>
              <p>Real-time pose estimation and corrective posture feedback using MediaPipe landmark coordinates and OpenCV geometry calculations.</p>
            </div>
          </div>
          <div class="mini-card">
            <div>
              <div class="mini-top">
                <span class="mini-index">03</span>
                <span class="pill-chip">{svg_icon('cpu', 12)} ML</span>
              </div>
              <h3>Multi-label Prediction</h3>
              <p>Ensemble model stacking combining Random Forests with a Logistic Regression meta-learner for complex multi-label classification (75% accuracy).</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Explore All Projects & Applications →", type="primary", key="overview_all_projects_btn"):
        set_page("Projects")

    render_gif_strip()

    st.markdown(
        """
        <div class="marquee"><div class="marquee-track">
        <span>Python</span><span>SQL</span><span>REST APIs</span><span>JSON</span><span>TensorFlow</span><span>PyTorch</span>
        <span>Streamlit</span><span>Plotly</span><span>OpenCV</span><span>MediaPipe</span><span>Google Cloud</span><span>Pandas</span>
        <span>NumPy</span><span>Git</span><span>Node.js</span><span>MongoDB</span><span>Scikit-Learn</span><span>NLTK</span><span>XGBoost</span>
        <span>Python</span><span>SQL</span><span>REST APIs</span><span>JSON</span><span>TensorFlow</span><span>PyTorch</span>
        <span>Streamlit</span><span>Plotly</span><span>OpenCV</span><span>MediaPipe</span><span>Google Cloud</span><span>Pandas</span>
        <span>NumPy</span><span>Git</span><span>Node.js</span><span>MongoDB</span><span>Scikit-Learn</span><span>NLTK</span><span>XGBoost</span>
        </div></div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================================
# 2. ABOUT SECTION
# =========================================================================
elif page == "About":
    section_header(
        "About Dev Kotak",
        "Driven by engineering rigor, analytical depth, and clear communication.",
        "A background spanning software engineering, machine learning research, and interactive data products.",
        icon_name="user",
    )

    about_col1, about_col2 = st.columns([1.1, 0.9], vertical_alignment="top")

    with about_col1:
        with st.container(border=True):
            st.markdown(f'<h3 class="h3-icon">{svg_icon("users", 19)} Professional Narrative</h3>', unsafe_allow_html=True)
            st.write(
                "I am a **Software & Machine Learning Engineer** holding a **Master of Engineering (M.Eng) in Electrical & Computer Engineering with a Collaborative Specialization in Data Science** from **Carleton University** in Ottawa, Canada."
            )
            st.write(
                "My experience combines academic rigor with hands-on industry application. Having completed **7 appointments across research institutes, dynamic AI startups, and healthcare platforms**, I have built software ranging from satellite hydrological forecasting at the **Space Applications Centre (ISRO)** to automated client workflows at the **Ottawa Centre for Cognitive Therapy**."
            )
            st.write(
                "I specialize in bridging the gap between theoretical machine learning models and usable, dependable software applications. I prioritize code maintainability, clean API design, and intuitive user experiences."
            )

    with about_col2:
        with st.container(border=True):
            st.markdown(f'<h3 class="h3-icon">{svg_icon("lightbulb", 19)} Engineering Philosophy</h3>', unsafe_allow_html=True)
            st.markdown(
                """
                - **Data-Driven Precision:** Every architectural and modeling decision is validated through empirical metrics, baseline comparisons, and rigorous cross-validation.
                - **Production-First Mindset:** Models are only as valuable as their ability to reliably serve users via clean APIs, low latency, and robust error handling.
                - **Simplicity & Usability:** Complex data workflows should be encapsulated into frictionless interfaces that empower domain experts and stakeholders.
                """
            )
            tag_row(["Deterministic APIs", "Empirical Evaluation", "Clean Architecture", "Continuous Learning"])

    st.write("")
    st.markdown("### Focus Areas & Capabilities")
    focus_c1, focus_c2, focus_c3 = st.columns(3)
    with focus_c1:
        with st.container(border=True):
            st.markdown(f"{icon_box('brain', 20, sm=True)} &nbsp; **01. Machine Learning Systems**", unsafe_allow_html=True)
            st.write(
                "Supervised & unsupervised learning, ensemble stacking, feature extraction, NLP topic modeling, model interpretability, and hyperparameter optimization."
            )
    with focus_c2:
        with st.container(border=True):
            st.markdown(f"{icon_box('eye', 20, sm=True)} &nbsp; **02. Computer Vision & Signals**", unsafe_allow_html=True)
            st.write(
                "Real-time pose estimation, geometric joint angle calculations, anomaly defect detection, OpenCV spatial filtering, and convolutional neural nets."
            )
    with focus_c3:
        with st.container(border=True):
            st.markdown(f"{icon_box('layers', 20, sm=True)} &nbsp; **03. Backend & Full-Stack**", unsafe_allow_html=True)
            st.write(
                "RESTful API design, JSON workflow automation, schema modeling in PostgreSQL & MongoDB, Streamlit interactive applications, and Plotly visual dashboards."
            )

    st.write("")
    about_btn1, about_btn2 = st.columns(2)
    with about_btn1:
        if st.button("View Career & Research Timeline →", key="about_exp_btn", type="primary", width="stretch"):
            set_page("Experience")
    with about_btn2:
        if st.button("Get in Touch / Contact", key="about_contact_btn", width="stretch"):
            set_page("Contact")


# =========================================================================
# 3. PROJECTS SECTION
# =========================================================================
elif page == "Projects":
    st.markdown('<span id="projects"></span>', unsafe_allow_html=True)
    section_header(
        "Selected Projects",
        "Work I can explain end to end.",
        "Each project highlights the real-world problem, architectural implementation details, and measurable technical outcomes.",
        icon_name="code",
    )

    # Interactive Category Filters
    if "project_filter" not in st.session_state:
        st.session_state.project_filter = "All"

    categories = [
        ("All", "All"),
        ("NLP", "NLP"),
        ("Computer Vision", "Computer Vision"),
        ("Machine Learning", "Machine Learning"),
        ("Data Analytics", "Data Analytics"),
    ]
    f_cols = st.columns(len(categories))
    for i, (label, cat_val) in enumerate(categories):
        with f_cols[i]:
            btn_type = "primary" if st.session_state.project_filter == cat_val else "secondary"
            if st.button(label, key=f"cat_btn_{cat_val}", type=btn_type, width="stretch"):
                st.session_state.project_filter = cat_val
                st.rerun()

    current_filter = st.session_state.project_filter

    # Featured Project: Tone Topic
    if current_filter in ["All", "NLP"]:
        st.write("")
        with st.container(border=True):
            left, right = st.columns([1.2, 1], vertical_alignment="center")
            with left:
                tone_img = ROOT / "images" / "screen06.jpg"
                if tone_img.exists():
                    st.image(str(tone_img), width="stretch")
            with right:
                st.markdown(f'<p class="project-type">{svg_icon("star", 13)} Featured Flagship Project · Natural Language Processing</p>', unsafe_allow_html=True)
                st.markdown("### Tone Topic")
                st.write(
                    "An interactive NLP application that transforms raw unstructured text or uploaded CSV documents into explorable semantic topic models using Latent Dirichlet Allocation (LDA) and NLTK tokenization."
                )
                st.markdown(
                    "<strong>Key Outcome:</strong> Real-time semantic topic distribution &amp; token extraction<br><strong>Contribution:</strong> End-to-end NLP pipeline, LDA modeling, and responsive Streamlit UI",
                    unsafe_allow_html=True,
                )
                tag_row(["Python", "Streamlit", "NLTK", "Gensim", "Pandas", "Topic Modeling", "LDA"])

                with st.expander("Technical Architecture & Pipeline Details"):
                    st.write(
                        "1. **Text Preprocessing:** Tokenization, stop-word removal, lemmatization, and n-gram phrase detection using NLTK and Gensim.\n"
                        "2. **Vector Space Modeling:** Dictionary creation and Bag-of-Words (BoW) corpus mapping with TF-IDF filtering.\n"
                        "3. **Inference & Visualization:** Multithreaded LDA model fitting with coherence score optimization (C_v) and interactive topic distribution matrices."
                    )

                st.link_button("Open Live Application ↗", "https://tonetopic.streamlit.app/", width="stretch")

    st.write("")

    # Grid of projects
    all_projects = [
        {
            "category": "Computer Vision",
            "type": "Computer Vision & Pose Estimation",
            "title": "Digital Yoga Trainer",
            "description": "Real-time pose estimation and posture correction system using MediaPipe landmark detection and OpenCV angular calculations to deliver instant bio-mechanical feedback.",
            "outcome_label": "Key Outcome",
            "outcome": "Live posture joint tracking and real-time corrective feedback",
            "tags": ["Python", "MediaPipe", "OpenCV", "NumPy", "Real-time Vision", "Biomechanics"],
            "repo": "https://github.com/dev856/Yoga-Pose-Estimation",
            "repo_label": "View GitHub Repository ↗",
            "image": "images/Tadasana.jpg",
            "deep_dive": "Calculates 3D landmark Euclidean vectors across shoulder-elbow-wrist and hip-knee-ankle joints. Measures angular deviations against canonical reference postures to deliver corrective auditory and visual overlays at 30+ FPS.",
        },
        {
            "category": "Data Analytics",
            "type": "Data Analytics & Exploration Workbench",
            "title": "InsightSync",
            "description": "Interactive data analytics platform enabling multi-variate statistical distributions, correlation matrices, dynamic filtering, and automated exploratory visual charts for complex datasets.",
            "outcome_label": "Key Outcome",
            "outcome": "Instant exploratory analysis & dynamic interactive Plotly charts",
            "tags": ["Python", "Streamlit", "Plotly", "Pandas", "Data Analytics", "EDA"],
            "demo": "https://insight-sync.streamlit.app/",
            "repo": GITHUB,
            "repo_label": "Explore GitHub Profile ↗",
            "deep_dive": "Automates exploratory data analysis (EDA) with automatic column type inference, missingness analysis, Pearson/Spearman correlation heatmaps, and customizable statistical distribution visualizations.",
        },
        {
            "category": "Machine Learning",
            "type": "Ensemble Machine Learning",
            "title": "Multi-label Dataset Prediction",
            "description": "A competition-grade modeling architecture combining Random Forest base estimators with a Logistic Regression meta-classifier for complex multi-label predictive tasks.",
            "outcome_label": "Measured Result",
            "outcome": "75% measured classification accuracy on competitive benchmark",
            "tags": ["Python", "Scikit-Learn", "Pandas", "Meta-learning", "Ensemble Stacking"],
            "repo": GITHUB,
            "repo_label": "Explore GitHub Profile ↗",
            "deep_dive": "Employs stratified k-fold out-of-fold validation to generate meta-features across diverse tree ensembles, mitigating label correlation biases and maximizing generalization accuracy.",
        },
        {
            "category": "Computer Vision",
            "type": "Computer Vision & Manufacturing",
            "title": "FabriSense",
            "description": "Automated textile inspection and defect detection solution utilizing computer vision preprocessing, spatial feature extraction, and classification algorithms.",
            "outcome_label": "Key Outcome",
            "outcome": "Automated anomaly identification & surface inspection",
            "tags": ["Python", "Streamlit", "OpenCV", "Image Processing", "Defect Detection"],
            "demo": "http://fabrisense.streamlit.app/",
            "repo": GITHUB,
            "repo_label": "Explore GitHub Profile ↗",
            "deep_dive": "Applies adaptive thresholding, morphological filtering, and spatial frequency analysis to identify weaving defects, stains, and structural anomalies in industrial fabric feeds.",
        },
        {
            "category": "Machine Learning",
            "type": "Geospatial Modeling & Remote Sensing",
            "title": "Hydrological Basin Flux Estimator",
            "description": "Geospatial machine learning models developed at ISRO benchmarked across XGBoost, LSTM neural networks, and Random Forests for discharge forecasting from MODIS and ERA5 satellite data.",
            "outcome_label": "Key Outcome",
            "outcome": "Accurate river discharge prediction across Indian river basins",
            "tags": ["Python", "Google Earth Engine", "XGBoost", "LSTM", "Geospatial Data"],
            "repo": GITHUB,
            "repo_label": "Explore GitHub Profile ↗",
            "deep_dive": "Ingests multi-spectral satellite observations, precipitation grids, and digital elevation models to model non-linear runoff dynamics using temporal recurrent networks.",
        },
    ]

    filtered_projects = [
        p for p in all_projects if current_filter == "All" or p["category"] == current_filter
    ]

    grid_cols = st.columns(2)
    for index, proj in enumerate(filtered_projects):
        col = grid_cols[index % 2]
        with col:
            img = proj.get("image")
            project_card(proj, image_path=img)

    st.write("")
    with st.container(border=True):
        p_cta_col1, p_cta_col2 = st.columns([1.5, 1], vertical_alignment="center")
        with p_cta_col1:
            st.markdown("### Looking to build or deploy a custom AI/ML system?")
            st.write("I am available for engineering roles and technical collaborations across predictive modeling, computer vision, and high-performance backend systems.")
        with p_cta_col2:
            if st.button("Start a Conversation", key="proj_contact_btn", type="primary", width="stretch"):
                set_page("Contact")


# =========================================================================
# 4. EXPERIENCE SECTION
# =========================================================================
elif page == "Experience":
    section_header(
        "Experience & Appointments",
        "From research prototypes to production workflows.",
        "Current-first timeline detailing responsibilities, software architectures, and measurable technical achievements.",
        icon_name="briefcase",
    )

    roles = [
        {
            "date": "Jul 2024 — Present",
            "role": "Computer Science Student & Technical Contributor",
            "company": "Ottawa Centre for Cognitive Therapy",
            "summary": "Engineering automated data workflows, cross-platform system integrations, and administrative pipelines across EHR and client scheduling platforms.",
            "bullets": [
                "Implemented robust REST API integrations that streamlined cross-platform data synchronization and improved interaction efficiency by 50%.",
                "Designed deterministic JSON-based scheduling workflows and automation scripts that increased overall system responsiveness by 30%.",
                "Conducted data audit routines and structured schema mappings to guarantee data consistency and patient record privacy.",
            ],
            "tags": ["REST APIs", "JSON", "System Integration", "Workflow Automation", "Python", "Data Synchronization"],
        },
        {
            "date": "Dec 2022 — May 2023",
            "role": "Research Intern",
            "company": "Space Applications Centre, ISRO",
            "summary": "Applied geospatial data science and advanced machine learning to hydrological flux estimation and discharge forecasting across Indian river basins.",
            "bullets": [
                "Extracted and processed multi-spectral MODIS, CHIRPS, ERA5/CFSR, and TRMM satellite observations using Python and Google Earth Engine.",
                "Benchmarked XGBoost, LSTM neural networks, and Random Forest regressors for discharge forecasting and hydraulic parameter modeling.",
                "Optimized feature engineering pipelines across temporal and spatial dimensions to improve cross-basin generalization.",
            ],
            "tags": ["Python", "Google Earth Engine", "XGBoost", "LSTM", "Geospatial Data", "Remote Sensing"],
            "logo": "images/isro1.jpeg",
        },
        {
            "date": "Dec 2022 — Feb 2023",
            "role": "Machine Learning Intern",
            "company": "Jupiter AI Labs",
            "summary": "Engineered applied ML case studies, statistical modeling pipelines, and AI-assisted workflows for client deliveries.",
            "bullets": [
                "Executed end-to-end data pipelines covering SQL extraction, exploratory data analysis, hypothesis testing, and model evaluation.",
                "Integrated prompt-engineering patterns and LLM workflows into internal Python development and project delivery.",
                "Delivered technical presentations and visual analytics dashboards for stakeholder decision-making.",
            ],
            "tags": ["Python", "SQL", "Machine Learning", "Prompt Engineering", "Data Modeling", "LLM Workflows"],
            "logo": "images/jupiter.png",
        },
        {
            "date": "Jun 2022 — Sep 2022",
            "role": "Data Science Intern",
            "company": "Zummit Infolabs",
            "summary": "Built computer vision prototypes for facial landmark detection, emotion classification, and real-time object tracking.",
            "bullets": [
                "Trained and evaluated facial landmark detectors with Dlib and convolutional emotion classifiers with TensorFlow.",
                "Constructed modular computer vision preprocessing pipelines and integrated YOLO-based object detection models.",
                "Optimized video stream frame capture to maintain 30+ FPS during real-time inference.",
            ],
            "tags": ["TensorFlow", "YOLO", "Dlib", "OpenCV", "Computer Vision", "Real-Time Inference"],
            "logo": "images/zummit.png",
        },
        {
            "date": "Jan 2022 — Apr 2022",
            "role": "Machine Learning Intern",
            "company": "CHARUSAT",
            "summary": "Implemented statistical machine learning and predictive modeling algorithms for academic research initiatives.",
            "bullets": [
                "Conducted exploratory feature engineering and supervised model training using Scikit-Learn and Pandas.",
                "Prepared technical documentation and validation metrics comparing model performance across benchmark datasets.",
            ],
            "tags": ["Python", "Scikit-Learn", "Pandas", "Statistical Modeling", "Academic Research"],
            "logo": "images/charusat.jpg",
        },
        {
            "date": "Jun 2021 — Jul 2021",
            "role": "Node.js Intern",
            "company": "Kintu Designs",
            "summary": "Developed backend RESTful services, database schemas, and integration endpoints for dynamic web platforms.",
            "bullets": [
                "Built asynchronous API routes with Express.js and structured NoSQL schemas in MongoDB.",
                "Collaborated with frontend engineers to ensure low-latency JSON payload delivery.",
            ],
            "tags": ["Node.js", "Express", "MongoDB", "REST APIs", "Backend Engineering"],
            "logo": "images/kintu.jpeg",
        },
        {
            "date": "May 2021 — Jun 2021",
            "role": "Data Science & Business Analytics Intern",
            "company": "The Sparks Foundation",
            "summary": "Executed exploratory data analytics and predictive modeling for business intelligence case studies.",
            "bullets": [
                "Identified key business trends and performance drivers through statistical visualizations and regression modeling.",
                "Presented findings with actionable insights and interactive visual charts.",
            ],
            "tags": ["Python", "Data Science", "Exploratory Analysis", "Visualization", "Business Intelligence"],
            "logo": "images/spark.png",
        },
    ]

    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for role in roles:
        timeline_item(role)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    exp_btn1, exp_btn2 = st.columns(2)
    with exp_btn1:
        if st.button("Explore Technical Skills & Capabilities →", key="exp_skills_btn", type="primary", width="stretch"):
            set_page("Skills")
    with exp_btn2:
        if st.button("Review Academic Credentials & Education →", key="exp_edu_btn", width="stretch"):
            set_page("Education")


# =========================================================================
# 5. SKILLS SECTION
# =========================================================================
elif page == "Skills":
    section_header(
        "Capabilities & Stack",
        "Skills backed by applied engineering.",
        "Grouped by technical domain, showing how each tool is leveraged in real production and research environments.",
        icon_name="terminal",
    )

    groups = [
        (
            "01",
            "terminal",
            "Software & Systems",
            "Backend logic, API architectures, schema design, and dependable data pipelines.",
            ["Python", "SQL", "REST APIs", "JSON", "Java", "Node.js", "MongoDB", "C/C++", "Linux", "Docker Basics"],
        ),
        (
            "02",
            "brain",
            "Data Science & ML",
            "Statistical modeling, model evaluation, NLP pipelines, and computer vision algorithms.",
            ["Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "NLTK", "OpenCV", "MediaPipe", "Gensim", "XGBoost"],
        ),
        (
            "03",
            "layers",
            "Product & Delivery",
            "Interactive dashboards, cloud environments, version control, and stakeholder interfaces.",
            ["Streamlit", "Plotly", "Git", "GitHub", "Google Cloud", "HTML5 / CSS3", "Agile / Scrum"],
        ),
    ]

    cards = "".join(
        '<div class="skill-card">'
        f'<div class="skill-card-top"><span class="skill-index">{index}</span>{icon_box(icon_n, 16, sm=True)}</div>'
        f"<div>"
        f"<h3>{safe(title)}</h3>"
        f"<p>{safe(summary)}</p>"
        f"</div>"
        f'<div class="tag-row">{tag_html(skills)}</div>'
        "</div>"
        for index, icon_n, title, summary, skills in groups
    )
    st.markdown(f'<div class="skill-grid">{cards}</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("### Engineering Methodologies")
    meth_left, meth_right = st.columns(2)
    with meth_left:
        with st.container(border=True):
            st.markdown(f'{icon_box("atom", 18, sm=True)} &nbsp; **Applied Machine Learning & Evaluation**', unsafe_allow_html=True)
            st.write(
                "Experience selecting appropriate model architectures (tree ensembles, neural networks, linear meta-models), conducting stratified cross-validation, and optimizing metrics beyond basic accuracy (precision, recall, ROC-AUC, F1-score)."
            )
            tag_row(["Cross-Validation", "Hyperparameter Tuning", "Ensemble Stacking", "Feature Importance"])

    with meth_right:
        with st.container(border=True):
            st.markdown(f'{icon_box("workflow", 18, sm=True)} &nbsp; **Systems Integration & API Design**', unsafe_allow_html=True)
            st.write(
                "Experience connecting disparate software systems via structured RESTful APIs, designing deterministic JSON schema contracts, and automating repetitive data synchronization tasks with high reliability."
            )
            tag_row(["REST Architecture", "JSON Schemas", "Authentication Flows", "Asynchronous Processing"])

    st.write("")
    skills_btn1, skills_btn2 = st.columns(2)
    with skills_btn1:
        if st.button("Explore Applications Built with this Stack →", key="skills_proj_btn", type="primary", width="stretch"):
            set_page("Projects")
    with skills_btn2:
        if st.button("Get in Touch / Discuss Collaboration", key="skills_contact_btn", width="stretch"):
            set_page("Contact")


# =========================================================================
# 6. EDUCATION SECTION
# =========================================================================
elif page == "Education":
    section_header(
        "Academic Credentials",
        "A rigorous systems foundation with a data science focus.",
        "The academic coursework and specialized training behind the software engineering and machine learning practice.",
        icon_name="graduation",
    )

    carleton_uri = as_data_uri(ROOT / "images" / "carleton.jpg")
    charusat_uri = as_data_uri(ROOT / "images" / "charusat.jpg")

    carleton_img_html = f'<img class="edu-logo" src="{carleton_uri}" alt="Carleton University" />' if carleton_uri else ""
    charusat_img_html = f'<img class="edu-logo" src="{charusat_uri}" alt="CHARUSAT" />' if charusat_uri else ""

    st.markdown(
        f"""
        <div class="edu-grid">
          <div class="edu-card">
            {carleton_img_html}
            <span class="date-pill">{svg_icon('calendar', 12)} 2023 — 2025 · Graduate</span>
            <h3>Master of Engineering</h3>
            <p>Electrical &amp; Computer Engineering · Collaborative Specialization in Data Science</p>
            <p><strong>CGPA:</strong> 10.5 / 12.0 &nbsp;·&nbsp; <strong>Location:</strong> Ottawa, Canada</p>
            <strong class="edu-school">Carleton University</strong>
          </div>
          <div class="edu-card">
            {charusat_img_html}
            <span class="date-pill">{svg_icon('calendar', 12)} 2019 — 2023 · Undergraduate</span>
            <h3>Bachelor of Technology</h3>
            <p>Computer Science &amp; Engineering</p>
            <p><strong>CGPA:</strong> 9.25 / 10.0 (WES: 3.92 / 4.0) &nbsp;·&nbsp; <strong>Merit Scholarship Awardee</strong></p>
            <strong class="edu-school">Charotar University of Science and Technology</strong>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown(f'<h3 class="h3-icon">{svg_icon("graduation", 19)} Academic Coursework</h3>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="coursework-grid">
          <div class="coursework-card">
            <h4>{svg_icon('cpu', 15)} Graduate Specialization</h4>
            <ul>
              <li>Applied Programming &amp; Algorithms</li>
              <li>Pattern Classification &amp; Machine Learning</li>
              <li>Advanced Data Visualization</li>
              <li>Data Science Seminar &amp; Research</li>
              <li>Cryptography &amp; Network Security</li>
            </ul>
          </div>
          <div class="coursework-card">
            <h4>{svg_icon('terminal', 15)} Computer Science Foundation</h4>
            <ul>
              <li>Data Structures &amp; Algorithms</li>
              <li>Database Management Systems (SQL)</li>
              <li>Operating Systems &amp; System Architecture</li>
              <li>Computer Networks &amp; Protocols</li>
              <li>Object-Oriented Programming (Java)</li>
            </ul>
          </div>
          <div class="coursework-card">
            <h4>{svg_icon('layers', 15)} Applied Engineering</h4>
            <ul>
              <li>Software Engineering Methodologies</li>
              <li>Artificial Intelligence &amp; Neural Nets</li>
              <li>Python for Scientific Computing</li>
              <li>Web Development &amp; Cloud Fundamentals</li>
              <li>Major Capstone Engineering Project</li>
            </ul>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    edu_btn1, edu_btn2 = st.columns(2)
    with edu_btn1:
        if st.button("Explore Research & Industry Roles →", key="edu_exp_btn", type="primary", width="stretch"):
            set_page("Experience")
    with edu_btn2:
        if resume_path.exists():
            st.download_button(
                "Download Official Résumé PDF ⤓",
                resume_path.read_bytes(),
                "Dev-Kotak-Resume.pdf",
                "application/pdf",
                key="edu_cv_btn",
                width="stretch",
            )


# =========================================================================
# 7. TESTIMONIALS SECTION
# =========================================================================
elif page == "Testimonials":
    section_header(
        "Endorsements & Feedback",
        "Collaborative feedback & peer highlights.",
        "Reflections on technical capability, collaborative problem-solving, and delivery quality.",
        icon_name="message",
    )

    st.markdown(
        """
        <div class="testimonial-grid">
          <div class="testimonial-card">
            <span class="quote-mark">{svg_icon('quote', 30)}</span>
            <p class="testimonial-quote">"Dev brings a remarkable blend of machine learning theory and practical software engineering. His ability to build robust data pipelines and translate complex models into actionable interfaces is outstanding."</p>
            <div class="testimonial-author">
              <div class="testimonial-author-avatar">RE</div>
              <div class="testimonial-author-info">
                <h4>Research &amp; Engineering Mentor</h4>
                <p>Applied AI &amp; Geospatial Science</p>
              </div>
            </div>
          </div>
          <div class="testimonial-card">
            <span class="quote-mark">{svg_icon('quote', 30)}</span>
            <p class="testimonial-quote">"Dev consistently delivers clean, dependable, and high-performance backend and data integration solutions. His technical curiosity and attention to detail make him an asset to any engineering team."</p>
            <div class="testimonial-author">
              <div class="testimonial-author-avatar">TL</div>
              <div class="testimonial-author-info">
                <h4>Technical Lead</h4>
                <p>Systems &amp; Product Integration</p>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    with st.container(border=True):
        t_cta_col1, t_cta_col2 = st.columns([1.5, 1], vertical_alignment="center")
        with t_cta_col1:
            st.markdown("### Ready to connect or discuss an opportunity?")
            st.write("Whether for full-time engineering roles, technical advisory, or project collaboration, I look forward to hearing from you.")
        with t_cta_col2:
            if st.button("Get in Touch", key="testim_contact_btn", type="primary", width="stretch"):
                set_page("Contact")


# =========================================================================
# 8. RÉSUMÉ SECTION
# =========================================================================
elif page == "Résumé":
    section_header(
        "Professional Résumé",
        "A concise view of credentials and experience.",
        "Download the current PDF for comprehensive appointments, technical skills, education, and projects.",
        icon_name="file_text",
    )

    st.markdown(
        f"""
        <div class="resume-panel">
          <p class="section-kicker">{svg_icon('download', 14)} Curriculum Vitae</p>
          <h3>Dev Kotak · Current Résumé</h3>
          <p>Complete record of academic credentials, software &amp; machine learning appointments, technical skills, and selected projects.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    if resume_path.exists():
        st.download_button(
            "Download Résumé PDF ⤓",
            resume_path.read_bytes(),
            "Dev-Kotak-Resume.pdf",
            "application/pdf",
            type="primary",
        )
        st.caption("PDF document · Optimized for ATS and executive review")
    else:
        st.error("The résumé PDF is currently unavailable.")

    st.divider()
    st.markdown("### Executive Summary")
    summary_left, summary_right = st.columns(2)
    with summary_left:
        with st.container(border=True):
            st.markdown(f'{icon_box("award", 18, sm=True)} &nbsp; **Key Qualifications**', unsafe_allow_html=True)
            st.write(
                "- **Graduate Degree:** M.Eng in Electrical & Computer Engineering with Data Science Specialization from Carleton University.\n"
                "- **7 Appointments:** Experience across ISRO (Space Applications Centre), Ottawa Centre for Cognitive Therapy, Jupiter AI Labs, and Zummit Infolabs.\n"
                "- **Core Stack:** Python, SQL, REST APIs, Streamlit, Pandas, Scikit-Learn, TensorFlow, OpenCV, MediaPipe."
            )
    with summary_right:
        with st.container(border=True):
            st.markdown(f'{icon_box("target", 18, sm=True)} &nbsp; **Primary Competencies**', unsafe_allow_html=True)
            st.write(
                "- **Applied Machine Learning:** Classification, Regression, Ensemble Stacking, Evaluation Metrics.\n"
                "- **Computer Vision & NLP:** Pose estimation, Object Detection, Topic Modeling, Text Extraction.\n"
                "- **Product Delivery:** Rapid prototyping with Streamlit, Plotly visual analytics, RESTful backend APIs."
            )


# =========================================================================
# 9. CONTACT SECTION
# =========================================================================
elif page == "Contact":
    section_header(
        "Correspondence",
        "Have a problem to solve?",
        "Email and LinkedIn are the best channels for discussing roles, project collaborations, and technical opportunities.",
        icon_name="mail",
    )

    st.markdown(
        f"""
        <div class="letter-card">
          <p class="section-kicker">{svg_icon('mail', 14)} Direct Contact</p>
          <p class="letter-email"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
          <p>{svg_icon('globe', 14)} Open to software engineering, data science, and applied machine learning roles in Ottawa, across Canada, and remotely.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    email_col, linkedin_col, github_col = st.columns(3)
    with email_col:
        st.link_button("Write an Email ↗", f"mailto:{EMAIL}", width="stretch")
    with linkedin_col:
        st.link_button("LinkedIn Profile ↗", LINKEDIN, width="stretch")
    with github_col:
        st.link_button("GitHub Profile ↗", GITHUB, width="stretch")

    st.write("")
    st.markdown(f'<h3 class="h3-icon">{svg_icon("send", 19)} Send a Direct Message</h3>', unsafe_allow_html=True)
    with st.form("contact_form", clear_on_submit=True):
        f_left, f_right = st.columns(2)
        with f_left:
            name = st.text_input("Your Name *", placeholder="e.g. Alex Morgan")
        with f_right:
            sender_email = st.text_input("Your Email *", placeholder="e.g. alex@company.com")
        subject = st.text_input("Subject", placeholder="e.g. Software Engineering Role / Project Discussion")
        message = st.text_area("Message *", placeholder="Write your message here...", height=140)
        submitted = st.form_submit_button("Send Message ↗", type="primary")

        if submitted:
            if not name.strip() or not sender_email.strip() or not message.strip():
                st.error("Please fill in all required fields (Name, Email, and Message).")
            elif "@" not in sender_email or "." not in sender_email:
                st.error("Please enter a valid email address.")
            else:
                saved = save_inquiry(name.strip(), sender_email.strip(), subject.strip(), message.strip())
                if saved:
                    st.success(f"Thank you, {safe(name)}! Your message has been safely received. I will respond to {safe(sender_email)} promptly.")
                else:
                    st.success(f"Thank you, {safe(name)}! Your message has been noted. You can also reach me directly at {EMAIL}.")


# Render Site Footer
site_footer()
