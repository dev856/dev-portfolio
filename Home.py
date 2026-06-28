import streamlit as st
import base64
import re
import html
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from textwrap import dedent
from custom import GITHUB_PROFILE,LINKEDIN_PROFILE

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Dev Kotak | Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="auto"
)



# --- LOAD CSS ---
def local_css(file_name):
    """Function to load a local CSS file."""
    try:
        with open(file_name, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}. Make sure it's in the correct path.")

local_css("styles/main.css")

# --- ASSET LOADING ---
def get_image_as_base64(path):
    """Function to convert an image to a base64 string."""
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

ASSETS = {
    "profile_pic": "assets/phot.jpeg", "isro": "images/isro1.jpeg",
    "jupiter_ai": "images/jupiter.png", "zummit": "images/zummit1.png",
    "depstar": "images/depstar.png", "kintu": "images/kintu.jpeg",
    "sparks": "images/spark.png",
}

# --- SOCIAL & CONTACT ---
SOCIAL_MEDIA = {
    "LinkedIn": "https://www.linkedin.com/in/dev-kotak/",
    "GitHub": "https://github.com/dev856",
    "CodeChef": "https://www.codechef.com/users/god_001",
    "Email": "mailto:devhkotak@gmail.com"
}

HERO_ACTIONS = {
    "View GitHub": SOCIAL_MEDIA["GitHub"],
    "Connect on LinkedIn": SOCIAL_MEDIA["LinkedIn"],
    "Send Email": SOCIAL_MEDIA["Email"],
}

def safe_text(value):
    return html.escape(str(value), quote=False)

def render_tag_cloud(items, class_name="tag-cloud"):
    return f'<div class="{class_name}">' + "".join(
        f"<span>{safe_text(item)}</span>" for item in items
    ) + "</div>"

def render_section_stats(items):
    cards = "".join(
        '<div class="section-stat-card">'
        f'<span>{safe_text(item["label"])}</span>'
        f'<strong>{safe_text(item["value"])}</strong>'
        f'<p>{safe_text(item["detail"])}</p>'
        '</div>'
        for item in items
    )
    st.html(f'<div class="section-stat-grid">{cards}</div>')

def render_hero():
    profile_pic_b64 = get_image_as_base64(ASSETS["profile_pic"])
    profile_image = (
        f'<img src="data:image/jpeg;base64,{profile_pic_b64}" alt="Dev Kotak">'
        if profile_pic_b64
        else ""
    )
    action_links = "".join(
        f'<a class="hero-action" href="{url}" target="_blank">{label}</a>'
        for label, url in HERO_ACTIONS.items()
    )

    st.markdown(
        f"""
        <section class="hero-panel">
            <div class="hero-copy">
                <span class="eyebrow">Software engineering + data science portfolio</span>
                <h1>Dev Kotak</h1>
                <p>
                    Graduate engineer building practical ML and data tools, from hydrology
                    research models to Streamlit analytics apps and computer vision prototypes.
                </p>
                <div class="hero-proof">
                    <div><strong>M.Eng</strong><span>Data Science focus</span></div>
                    <div><strong>6</strong><span>Applied internships</span></div>
                    <div><strong>15+</strong><span>Core tools</span></div>
                </div>
                <div class="hero-tags">
                    <span>Data Science</span>
                    <span>Machine Learning</span>
                    <span>Python</span>
                    <span>Streamlit</span>
                </div>
                <div class="hero-actions">{action_links}</div>
            </div>
            <div class="hero-visual">
                <div class="profile-orbit">{profile_image}</div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

# --- DATABASE FOR CONTACT FORM ---
def init_db():
    conn = sqlite3.connect('portfolio_contacts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts
        (id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

init_db()

# --- SIDEBAR ---
with st.sidebar:
    profile_pic_b64 = get_image_as_base64(ASSETS["profile_pic"])
    if profile_pic_b64:
        st.markdown(
            f"""
            <div class="sidebar-profile">
                <img src="data:image/jpeg;base64,{profile_pic_b64}" alt="Dev Kotak" class="profile-image">
                <h1>Dev Kotak</h1>
                <p>Aspiring Software & Data Engineer</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="sidebar-profile">
                <h1>Dev Kotak</h1>
                <p>Aspiring Software & Data Engineer</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    choose = option_menu(
        menu_title=None,
        options=["About Me", "Experience", "Skills", "Education", "Projects", "Resume", "Contact"],
        icons=['person-vcard', 'briefcase', 'gear-wide-connected', 'mortarboard', 'kanban', 'file-earmark-person', 'envelope-at'],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#9fb4cc", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px",
                "font-weight": "600",
                "text-align": "left",
                "margin": "4px 0",
                "padding": "11px 14px",
                "border-radius": "6px",
                "color": "#d7e0ea",
                "--hover-color": "rgba(56, 189, 248, 0.10)",
            },
            "nav-link-selected": {
                "background-color": "#e5edf7",
                "color": "#07111f",
            },
        }
    )
    components.html(GITHUB_PROFILE)
    components.html(LINKEDIN_PROFILE,height=400,width=700)
    st.markdown("---")
    st.markdown("<h3 class='sidebar-heading'>Connect</h3>", unsafe_allow_html=True)
    
    icons_html = []
    for platform, link in SOCIAL_MEDIA.items():
        icon_name = platform.lower()
        if icon_name == "email": icon_name = "gmail"
        if icon_name == "linkedin": 
            icons_html.append(f'<a href="{link}" target="_blank" style="margin: 0 10px;"><img src="https://img.icons8.com/ios-filled/50/ffffff/linkedin.png" width="30"></a>')
            continue
        # Using a white icon variant
        icon_path = f"https://cdn.simpleicons.org/{icon_name}/FFFFFF"
        icons_html.append(f'<a href="{link}" target="_blank" style="margin: 0 10px;"><img src="{icon_path}" width="30"></a>')
    
    st.markdown(f'''
    <div class="sidebar-socials">
        {''.join(icons_html)}
    </div>
    ''', unsafe_allow_html=True)
    
# --- MAIN CONTENT SECTIONS ---

def about_me_section():
    render_hero()
    st.markdown('<div class="section-header">Profile Summary</div>', unsafe_allow_html=True)
    render_section_stats([
        {"label": "Current Base", "value": "Carleton", "detail": "Graduate engineering work with a Data Science specialization."},
        {"label": "Build Style", "value": "Practical", "detail": "Readable interfaces, useful analytics, and working ML prototypes."},
        {"label": "Open To", "value": "Internships", "detail": "Software engineering, data science, and applied AI teams."},
    ])
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<div class='about-text'><strong>Hi, I'm Dev.</strong> I am a Master of Engineering student at Carleton University specializing in Electrical & Computer Engineering and Data Science.</div>", unsafe_allow_html=True)
        st.markdown("<div class='about-text'>My recent work spans hydrological flux estimation, pose estimation, topic modeling, dashboards, and model evaluation workflows.</div>", unsafe_allow_html=True)
        st.markdown("<div class='about-text'>I am actively looking for internship opportunities where I can contribute across software engineering, data science, and applied AI.</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(
            """
            <div class="profile-focus-panel">
                <span class="card-eyebrow">Current Focus</span>
                <h3>Applied AI and data products</h3>
                <p>Combining software engineering fundamentals with practical machine learning, visualization, and product thinking.</p>
                <div>
                    <span>Internship-ready</span>
                    <span>Data-driven systems</span>
                    <span>Product-minded engineering</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Academic and Career Interests")
    interests = ["Data Visualization", "Deep Learning", "Recommendation Systems", "Natural Language Processing", "Data Engineering", "Software Engineering"]
    st.html(render_tag_cloud(interests, "premium-tool-cloud compact-cloud"))

def experience_section():
    st.markdown('<div class="section-header">Work Experience</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-kicker">
            Internship and research experience across applied AI, data science, software engineering, and computer vision.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_section_stats([
        {"label": "Experience Range", "value": "2021-2023", "detail": "Research, ML, data science, backend, and chatbot internships."},
        {"label": "Applied Domains", "value": "AI + CV", "detail": "Hydrology, facial analysis, pose estimation, NLP, and automation."},
        {"label": "Working Mode", "value": "End-to-end", "detail": "From data pipelines and modeling to usable prototypes."},
    ])
    experience_data = [
        {"headline": "Research Intern, ISRO", "text": "Worked on ML techniques for hydrological flux estimation over Indian river basins using Python and Google Earth Engine.", "image": get_image_as_base64(ASSETS['isro']), "date": "Dec 2022 - May 2023", "focus": "Machine Learning", "stack": ["Python", "ML", "Google Earth Engine"]},
        {"headline": "ML Intern, Jupiter AI Labs", "text": "Developed E2E ML solutions, integrated ChatGPT with Chrome extensions, and worked on AI Prompt Engineering.", "image": get_image_as_base64(ASSETS['jupiter_ai']), "date": "Dec 2022 - Feb 2023", "focus": "AI Engineering", "stack": ["Python", "ChatGPT", "Prompt Engineering"]},
        {"headline": "Data Science Intern, Zummit Infolabs", "text": "Developed facial feature detectors with Dlib, emotion classifiers with TensorFlow, and object detection models with YOLO.", "image": get_image_as_base64(ASSETS['zummit']), "date": "Jun 2022 - Sep 2022", "focus": "Computer Vision", "stack": ["TensorFlow", "YOLO", "Dlib"]},
        {"headline": "ML Intern, CHARUSAT", "text": "Created a lightweight Yoga Pose estimation solution using MediaPipe and OpenCV.", "image": get_image_as_base64(ASSETS['depstar']), "date": "May 2022 - Jun 2022", "focus": "Computer Vision", "stack": ["MediaPipe", "OpenCV", "Python"]},
        {"headline": "NodeJS Intern, Kintu Designs", "text": "Built a chatbot for a delivery app using Botpress.io and Node.js.", "image": get_image_as_base64(ASSETS['kintu']), "date": "Jun 2021 - Sep 2021", "focus": "Software Engineering", "stack": ["Node.js", "Botpress", "Chatbots"]},
        {"headline": "Data Science Intern, The Sparks Foundation", "text": "Applied supervised and unsupervised ML for predictive tasks.", "image": get_image_as_base64(ASSETS['sparks']), "date": "Jan 2021 - Feb 2021", "focus": "Data Science", "stack": ["Python", "Scikit-Learn", "Pandas"]}
    ]

    filters = ["All"] + sorted({entry["focus"] for entry in experience_data})
    selected_focus = st.segmented_control("Filter experience by focus", filters, default="All")
    if selected_focus != "All":
        experience_data = [entry for entry in experience_data if entry["focus"] == selected_focus]

    timeline_cards = []
    for i, entry in enumerate(experience_data):
        side = "left" if i % 2 == 0 else "right"
        image_html = (
            f'<img src="data:image/jpeg;base64,{entry["image"]}" alt="{safe_text(entry["headline"])}">'
            if entry["image"] else ""
        )
        stack_html = render_tag_cloud(entry["stack"], "timeline-skills")
        timeline_cards.append(
            f'<div class="timeline-container {side}">'
            '<div class="timeline-content">'
            f'<div class="experience-card-top"><div>{image_html}</div><span>{safe_text(entry["focus"])}</span></div>'
            f'<div class="timeline-headline">{safe_text(entry["headline"])}</div>'
            f'<p class="timeline-date">{safe_text(entry["date"])}</p>'
            f'<p class="timeline-description">{safe_text(entry["text"])}</p>'
            f'{stack_html}'
            '</div></div>'
        )
    st.html(f'<div class="timeline">{"".join(timeline_cards)}</div>')

# 0
    # --- SKILLS DATA ---
def _legacy_skills_section():
        st.markdown('<div class="section-header">Technical Skills</div>', unsafe_allow_html=True)
        
        # --- SKILLS DATA ---
        skills_data = {
            "Programming & Databases": {"Python": 95, "Java": 80, "SQL": 90, "C/C++": 75, "MongoDB": 70},
            "Data Science & ML": {"Pandas & NumPy": 95, "Scikit-Learn": 90, "TensorFlow": 85, "PyTorch": 80, "NLTK": 80},
            "Web, Cloud & Viz": {"Streamlit": 90, "Plotly": 85, "HTML/CSS": 80, "GCP": 75, "Git & GitHub": 90}
        }

        all_skill_rows = [
            {"Category": category, "Skill": skill, "Proficiency": proficiency}
            for category, skills in skills_data.items()
            for skill, proficiency in skills.items()
        ]
        skills_df = pd.DataFrame(all_skill_rows)
        st.markdown(
            """
            <div class="section-kicker">
                A focused technical stack across software engineering, applied ML, and data visualization.
            </div>
            """,
            unsafe_allow_html=True,
        )

        skill_cards = []
        for category, skills in skills_data.items():
            top_skills = sorted(skills.items(), key=lambda item: item[1], reverse=True)[:4]
            skill_rows = "".join(
                f"""
                <div class="skill-row">
                    <div><strong>{skill}</strong><span>{proficiency}%</span></div>
                    <div class="skill-bar"><i style="width: {proficiency}%"></i></div>
                </div>
                """
                for skill, proficiency in top_skills
            )
            skill_cards.append(
                f"""
                <article class="skill-stack-card">
                    <span class="card-eyebrow">{category}</span>
                    {skill_rows}
                </article>
                """
            )

        st.markdown(
            f'<div class="skill-stack-grid">{"".join(skill_cards)}</div>',
            unsafe_allow_html=True,
        )
        
        # Create tabs for different visualization methods
        tab1, tab2, tab3 = st.tabs(["Skill Radar", "Sunburst View", "Category Breakdown"])
        
        with tab1:
            # Radar Chart (Spider/Web chart)
            categories = list(skills_data.keys())
            # Calculate average proficiency per category
            category_avg = {cat: sum(skills.values())/len(skills) for cat, skills in skills_data.items()}
            
            # Create radar chart using plotly graph objects
            import plotly.graph_objects as go
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=list(category_avg.values()),
                theta=categories,
                fill='toself',
                name='Skill Proficiency',
                line_color='rgba(100, 200, 255, 0.8)',
                fillcolor='rgba(100, 200, 255, 0.3)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        tickmode='linear',
                        tick0=0,
                        dtick=20,
                        tickfont=dict(size=14)
                    ),
                    angularaxis=dict(
                        direction="clockwise",
                        tickfont=dict(size=16, color='white')
                    )
                ),
                showlegend=False,
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=100, r=100, t=50, b=50),
                height=600,
                font=dict(size=14, color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Interactive skill level selectors
            st.markdown("##### Explore Skills by Proficiency Level")
            col_filter_1, col_filter_2 = st.columns([1, 2])
            with col_filter_1:
                min_proficiency = st.slider("Minimum Proficiency Level", 0, 100, 70, 5)
            with col_filter_2:
                selected_categories = st.multiselect(
                    "Categories",
                    list(skills_data.keys()),
                    default=list(skills_data.keys()),
                )
            
            filtered_skills = [
                (row.Skill, row.Proficiency, row.Category)
                for row in skills_df.itertuples(index=False)
                if row.Proficiency >= min_proficiency and row.Category in selected_categories
            ]
            
            if filtered_skills:
                # Create a dataframe for the filtered skills
                df = pd.DataFrame(filtered_skills, columns=["Skill", "Proficiency", "Category"])
                
                # Display as horizontal bars with better sizing
                fig = px.bar(df, x="Proficiency", y="Skill", color="Category", 
                             orientation='h', text="Proficiency", 
                             color_discrete_sequence=px.colors.qualitative.Bold,
                             template="plotly_dark")
                
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=max(400, len(filtered_skills) * 40),
                    margin=dict(l=120, r=50, t=20, b=20),
                    yaxis=dict(
                        categoryorder='total ascending',
                        tickfont=dict(size=14)
                    ),
                    xaxis=dict(tickfont=dict(size=12)),
                    font=dict(size=12)
                )
                
                # Add animations with better text positioning
                fig.update_traces(
                    texttemplate='%{text}%', 
                    textposition='outside',
                    textfont=dict(size=12, color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No skills match the selected proficiency level.")

        with tab2:
            # Fixed Sunburst Chart
            import plotly.graph_objects as go
            
            # Prepare data for sunburst
            labels = []
            parents = []
            values = []
            colors = []
            
            # Add root
            labels.append("All Skills")
            parents.append("")
            values.append(sum(sum(skills.values()) for skills in skills_data.values()))
            colors.append(50)
            
            # Add categories
            for category, skills in skills_data.items():
                labels.append(category)
                parents.append("All Skills")
                values.append(sum(skills.values()))
                colors.append(sum(skills.values()) / len(skills))
            
            # Add individual skills
            for category, skills in skills_data.items():
                for skill, proficiency in skills.items():
                    labels.append(skill)
                    parents.append(category)
                    values.append(proficiency)
                    colors.append(proficiency)
            
            # Create sunburst chart
            fig = go.Figure(go.Sunburst(
                labels=labels,
                parents=parents,
                values=values,
                branchvalues="total",
                hovertemplate='<b>%{label}</b><br>Value: %{value}<br>Percentage: %{percentParent}<extra></extra>',
                maxdepth=3,
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=30, b=30),
                height=600,
                font=dict(size=14, color='white'),
                title=dict(
                    text="Skills Hierarchy View",
                    x=0.5,
                    font=dict(size=18, color='white')
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("👆 **Click on segments to zoom in and explore specific categories**")

        with tab3:
            # Category breakdown with interactive elements
            selected_category = st.selectbox("Select Skill Category", list(skills_data.keys()))
            
            if selected_category:
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    # Create a horizontal bar chart for selected category
                    category_skills = skills_data[selected_category]
                    df = pd.DataFrame(
                        {"Skill": list(category_skills.keys()), 
                         "Proficiency": list(category_skills.values())}
                    ).sort_values("Proficiency", ascending=False)
                    
                    fig = px.bar(
                        df, 
                        x="Proficiency", 
                        y="Skill", 
                        orientation='h',
                        color="Proficiency",
                        color_continuous_scale=px.colors.sequential.Plasma,
                        template="plotly_dark",
                        text="Proficiency"
                    )
                    
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=120, r=50, t=30, b=30),
                        height=400,
                        coloraxis_showscale=False,
                        yaxis=dict(tickfont=dict(size=14)),
                        xaxis=dict(tickfont=dict(size=12)),
                        font=dict(size=12)
                    )
                    
                    # Add animations and styling with better text
                    fig.update_traces(
                        texttemplate='%{text}%', 
                        textposition='outside',
                        marker_line_color='rgb(8,48,107)',
                        marker_line_width=1.5,
                        textfont=dict(size=12, color='white')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Display skills as tags
                    st.markdown(f"##### {selected_category} Skills")
                    category_skills = skills_data[selected_category]
                    for skill, proficiency in category_skills.items():
                        # Create progress bars with custom colors based on proficiency
                        if proficiency >= 90:
                            color = "#4CAF50"  # Green for high proficiency
                        elif proficiency >= 80:
                            color = "#2196F3"  # Blue for good proficiency
                        elif proficiency >= 70:
                            color = "#FF9800"  # Orange for moderate proficiency
                        else:
                            color = "#F44336"  # Red for basic proficiency
                        
                        st.markdown(
                            f"""
                            <div style="margin-bottom:15px;">
                                <span style="font-weight:bold; color:white; font-size:16px;">{skill}</span>
                                <div style="background-color:#2a2a2a;border-radius:10px;height:20px;width:100%;margin-top:8px;border:1px solid #444;">
                                    <div style="background-color:{color};width:{proficiency}%;height:18px;border-radius:9px;display:flex;align-items:center;justify-content:flex-end;padding-right:5px;">
                                        <span style="font-size:12px; color:white; font-weight:bold;">{proficiency}%</span>
                                    </div>
                                </div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
        
def _legacy_education_section():
    st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-kicker">
            Academic training across computer science, electrical and computer engineering, and data science.
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # --- EDUCATION DATA ---
    # Define image paths in the ASSETS dictionary first
    ASSETS['carleton'] = "images/carleton.jpg" 
    ASSETS['hiramohan'] = "images/school.png" 
    ASSETS['ultravision'] = "images/school.png"

    # Add custom CSS for education cards
    st.markdown("""
    <style>
    .edu-card {
        background: linear-gradient(135deg, rgba(32,32,32,0.8) 0%, rgba(40,40,40,0.4) 100%);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.3s, box-shadow 0.3s;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        overflow: hidden;
        position: relative;
    }
    
    .edu-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border: 1px solid rgba(100,200,255,0.3);
    }
    
    .edu-card-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .edu-icon {
        width: 60px;
        height: 60px;
        margin-right: 15px;
        border-radius: 50%;
        padding: 5px;
        background: rgba(255,255,255,0.1);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .edu-icon img {
        max-width: 100%;
        max-height: 100%;
        border-radius: 50%;
        object-fit: contain;
    }
    
    .edu-title {
        flex-grow: 1;
    }
    
    .edu-title h4 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    .edu-subtitle {
        color: #b3b3b3;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    .edu-duration {
        background: linear-gradient(135deg, #3a7bd5, #00d2ff);
        border-radius: 20px;
        padding: 5px 15px;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
        display: inline-block;
        margin-top: 5px;
    }
    
    .edu-details {
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
    }
    
    .edu-details ul {
        margin: 0;
        padding-left: 20px;
    }
    
    .edu-details li {
        margin-bottom: 8px;
        line-height: 1.4;
    }
    
    .edu-timeline-container {
        position: relative;
        padding-left: 30px;
    }
    
    .edu-timeline-container::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(to bottom, #3a7bd5, #00d2ff);
        border-radius: 4px;
    }
    
    .edu-timeline-container::after {
        content: '';
        position: absolute;
        left: -8px;
        top: 30px;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #00d2ff;
        box-shadow: 0 0 10px #00d2ff;
    }
    
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    
    .styled-table thead tr {
        background-color: #3a7bd5;
        color: #ffffff;
        text-align: left;
    }
    
    .styled-table th,
    .styled-table td {
        padding: 12px 15px;
    }
    
    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
    }
    
    .styled-table tbody tr:nth-of-type(even) {
        background-color: rgba(255,255,255,0.05);
    }
    
    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #3a7bd5;
    }
    
    .course-tag {
        display: inline-block;
        background: linear-gradient(135deg, #3a7bd5, #00d2ff);
        color: white;
        padding: 3px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

    education_summary = [
        {
            "image": get_image_as_base64(ASSETS.get('carleton')) or "https://img.icons8.com/color/96/carleton-university.png",
            "degree": "Master of Engineering - Electrical & Computer Engineering",
            "university": "Carleton University",
            "link": "https://carleton.ca/discover/",
            "duration": "2023 - 2025",
            "accent": "#60a5fa",
            "focus": "Graduate specialization in data science",
            "details": [
                "Collaborative Specialization in Data Science",
                "<b>CGPA:</b> 10.5 / 12.0",
                "<b>Relevant Coursework:</b> Pattern Classification, Applied Programming, Secure Networking, Data Science Seminar, Advanced Data Visualization, Cryptographic Implementations."
            ],
            "color": "linear-gradient(135deg, #4e54c8, #8f94fb)"
        },
        {
            "image": get_image_as_base64(ASSETS.get('depstar')),
            "degree": "Bachelor of Technology - Computer Science & Engineering",
            "university": "Charotar University of Science and Technology",
            "link": "https://www.charusat.ac.in/",
            "duration": "2019 - 2023",
            "accent": "#34d399",
            "focus": "Computer science and software foundations",
            "details": [
                "<b>CGPA:</b> 9.25 / 10.0 (WES Evaluated: 3.92 / 4.0)",
                "Recipient of a merit-based scholarship for all 4 years.",
                "<b>Relevant Coursework:</b> Data Structures & Algorithms, Machine Learning, AI, Software Engineering, Computer Networks, OOP."
            ],
            "color": "linear-gradient(135deg, #11998e, #38ef7d)"
        },
        {
            "image": get_image_as_base64(ASSETS.get('hiramohan')) or "https://img.icons8.com/fluency/96/school.png",
            "degree": "Higher Secondary Education (Class XI-XII)",
            "university": "Hiramohan Vidhyalaya",
            "link": "https://schools.org.in/surendranagar/24080503891/hira-mohan-vidhyalaya.html",
            "duration": "2017 - 2019",
            "accent": "#fbbf24",
            "focus": "Mathematics and science foundation",
            "details": ["<b>Percentage:</b> 82% (Grade A2)", "<b>Coursework:</b> Physics, Chemistry, Mathematics"],
            "color": "linear-gradient(135deg, #f46b45, #eea849)"
        },
        {
            "image": get_image_as_base64(ASSETS.get('ultravision')) or "https://img.icons8.com/fluency/96/school-building.png",
            "degree": "Secondary Education (Class X)",
            "university": "Ultravision Academy",
            "link": "http://www.ultravisionschool.com/",
            "duration": "2016 - 2017",
            "accent": "#a78bfa",
            "focus": "Secondary education",
            "details": ["Completed secondary education with distinction."],
            "color": "linear-gradient(135deg, #614385, #516395)"
        }
    ]

    carleton_modules = {
        "2023-2024": [
            ("ITEC 5010", "Applied Programming", "0.5"),
            ("SYSC 5405", "Pattern Classification and Experiment Design", "0.5"),
            ("SYSC 5500", "Designing Secure Networking and Computer System", "0.5"),
            ("DATA 5000", "Data Science Seminar", "0.5"),
            ("SYSC 5303", "Interactive Networked Systems and Telemedicines", "0.5"),
            ("SYSC 5807", "Cryptography Implementation", "0.5")
        ]
    }

    charusat_modules = {
        "2019/20 Sem 1": [("CE143", "Computer Concepts and Programming", "5"), ("CL142.01", "Environmental Sciences", "2"), ("EE145", "Basics of Electronics and Electrical Engineering", "4"), ("HS105.01 A", "Liberal Arts - Media and Graphic Design", "2"), ("IT144", "ICT workshop", "1"), ("MA143", "Engineering Mathematics- I", "4")],
        "2019/20 Sem 2": [("CE144", "Object Oriented Programming with C++", "5"), ("HS126.01A", "Communication Skills - I", "2"), ("MA144", "Engineering Mathematics - II", "4"), ("ME145", "Elements of Engineering", "4"), ("PY141.01", "Engineering Physics", "4")],
        "2020/21 Sem 3": [("CE244", "Software Group Project - I", "2"), ("CE251", "Java Programming", "5"), ("CE252", "Digital Electronics", "4"), ("CE257", "Data Communications and Networking", "5"), ("EC281.01", "Introduction to Matlab Programming", "2"), ("HS121.02A", "Creativity, Problem Solving and Innovation", "2"), ("MA253", "Discrete Mathematics and Algebra", "4")],
        "2020/21 Sem 4": [("CS245", "Data Structures and Algorithms", "4"), ("CE246", "DataBase Management System", "6"), ("CE255", "Software Group Project- II", "2"), ("CE258", "Microprocessor and Computer Organization", "5"), ("CE259", "Programming in Python", "1"), ("EC282.01", "Prototyping Electronics with Arduino", "2"), ("HS111.02A", "Human Values and Professional Ethics", "2")],
        "2021/22 Sem 5": [("CS341", "Artificial Intelligence", "4"), ("CS343", "Summer Internship I", "3"), ("CS348", "Software Group Project - III", "1"), ("CS350", "Operating System", "4"), ("CS351", "Design and analysis of Algorithm", "4"), ("CS352", "Computer Networks", "4"), ("CS377", "Mobile Application Development", "4"), ("HS131.02A", "Communication and Soft Skills", "2")],
        "2021/22 Sem 6": [("CS344", "Machine Learning", "4"), ("CS345", "Cryptography and Network Security", "5"), ("CS346", "Software Engineering", "4"), ("CS353", "Theory of Computation", "3"), ("CS357", "Software Group Project-IV", "1"), ("CS374", "Modern Networks", "4"), ("HS132.02A", "Contributing Personality Development", "2")],
        "2022/23 Sem 7": [("CS442", "Data Science and Analytics", "5"), ("CS446", "Summer Internship-II", "3"), ("CS449", "Internet of Things", "4"), ("CS450", "Design of Langugage Processor", "4"), ("CS451", "Advanced Computing", "4"), ("CS452", "Software Group Project-V", "1"), ("CS474", "Image Processing and Computer Vision", "5")],
        "2022/23 Sem 8": [("CS453", "Software Project Major", "18")]
    }

    # Create tabs with custom styling
    tab1, tab2 = st.tabs(["Education Journey", "Course Modules"])

    with tab1:
        # Add intro section with animation
        st.markdown("""
        <div class="journey-intro">
            <h3>My Academic Background</h3>
            <p>A concise timeline of the academic path behind my software, data, and machine learning work.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns - one for timeline, one for animation
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create a timeline effect with cards
            st.markdown('<div class="edu-timeline-container">', unsafe_allow_html=True)
            
            for entry in education_summary:
                details_html = "".join([f"<li>{item}</li>" for item in entry["details"]])
                image_src = f"data:image/png;base64,{entry['image']}" if entry['image'] and not entry['image'].startswith('http') else entry['image']
                
                st.markdown(f"""
                <div class="edu-card" style="border-left: 3px solid {entry['accent']};">
                    <div class="edu-card-header">
                        <div class="edu-icon" style="background: {entry['color']}">
                            <img src="{image_src}" alt="{entry['university']}">
                        </div>
                        <div class="edu-title">
                            <h4><a href="{entry['link']}" target="_blank" style="text-decoration: none; color: white;">{entry['degree']}</a></h4>
                            <div class="edu-subtitle">{entry['university']}</div>
                            <div class="edu-meta-row">
                                <span>{entry['duration']}</span>
                                <span>{entry['focus']}</span>
                            </div>
                        </div>
                    </div>
                    <div class="edu-details">
                        <ul>{details_html}</ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-focus-panel">
                <h4>Academic Focus</h4>
                <p>Graduate-level data science, applied programming, secure systems, and machine learning, supported by a computer science foundation.</p>
                <div>
                    <span>Data Science</span>
                    <span>Machine Learning</span>
                    <span>Secure Systems</span>
                    <span>Visualization</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        # Add course module visualization with attractive styling
        st.markdown("""
        <div class="journey-intro">
            <h3>Academic Curriculum</h3>
            <p>Coursework grouped by program and academic year.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create an expandable section for Carleton courses
        with st.expander("🎓 Carleton University Modules", expanded=True):
            for year, modules in carleton_modules.items():
                st.markdown(f"<h4 style='margin-top: 20px;'>Academic Year: {year}</h4>", unsafe_allow_html=True)
                
                # Create HTML table for better styling
                # Generate the HTML table as a single string
                table_html = ['<table class="styled-table"><thead><tr><th>Course Code</th><th>Module Title</th><th>Credits</th></tr></thead><tbody>']
                for code, title, credit in modules:
                    table_html.append(f'<tr><td>{code}</td><td>{title}</td><td>{credit}</td></tr>')
                table_html.append('</tbody></table>')
                st.markdown("".join(table_html), unsafe_allow_html=True)

                # Add a visual representation of key skills gained
                st.markdown("<h5 style='margin-top: 15px;'>Key Skills Gained:</h5>", unsafe_allow_html=True)
                
                # Extract keywords from course titles
                all_titles = " ".join([title for _, title, _ in modules])
                keywords = ["Programming", "Data Science", "Networking", "Cryptography", "Design", "Systems"]
                
                # Display as tags
                tags_html = "".join([f'<span class="course-tag">{keyword}</span>' for keyword in keywords if keyword.lower() in all_titles.lower()])
                
                st.markdown(f"<div style='margin-top: 10px; margin-bottom: 20px;'>{tags_html}</div>", unsafe_allow_html=True)
        
        # Create expandable sections for each academic year at Charusat
        st.markdown("<h4 style='margin-top: 30px; border-top: 1px solid #444; padding-top: 20px;'>🎓 Charotar University of Science and Technology Modules</h4>", unsafe_allow_html=True)
        
        # Group semesters by academic year
        grouped_semesters = {
            "First Year (2019-2020)": ["2019/20 Sem 1", "2019/20 Sem 2"],
            "Second Year (2020-2021)": ["2020/21 Sem 3", "2020/21 Sem 4"],
            "Third Year (2021-2022)": ["2021/22 Sem 5", "2021/22 Sem 6"],
            "Final Year (2022-2023)": ["2022/23 Sem 7", "2022/23 Sem 8"]
        }
        
        for year_label, semesters in grouped_semesters.items():
            with st.expander(f"📚 {year_label}", expanded=False):
                cols = st.columns(2)
                for i, sem in enumerate(semesters):
                    with cols[i % 2]:
                        st.markdown(f"<h5 style='margin-top: 10px;'>{sem}</h5>", unsafe_allow_html=True)
                        
                        # Create HTML table for better styling
                        table_html = ['<table class="styled-table"><thead><tr><th>Code</th><th>Module</th><th>Credits</th></tr></thead><tbody>']
                        if sem in charusat_modules:
                            for code, title, credit in charusat_modules[sem]:
                                table_html.append(f'<tr><td>{code}</td><td>{title}</td><td>{credit}</td></tr>')
                        table_html.append('</tbody></table>')
                        st.markdown("".join(table_html), unsafe_allow_html=True)
                
                # Calculate total credits for the year
                total_credits = sum(int(credit) for sem_name in semesters if sem_name in charusat_modules for _, _, credit in charusat_modules[sem_name])
                st.markdown(f"<p style='text-align: right; width: 100%; margin-top: 10px;'><b>Total Credits for {year_label}:</b> {total_credits}</p>", unsafe_allow_html=True)



def projects_section():
    st.markdown('<div class="section-header">Selected Projects</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-kicker">
            Practical projects across computer vision, NLP, and model evaluation, built as usable demos rather than isolated notebooks.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_section_stats([
        {"label": "Project Shape", "value": "Applied", "detail": "ML, NLP, and computer vision projects with practical interfaces."},
        {"label": "Delivery", "value": "Prototype", "detail": "Streamlit apps, notebooks, pipelines, and measurable model outcomes."},
        {"label": "Signal", "value": "Hands-on", "detail": "Each project reflects implementation, evaluation, and presentation."},
    ])
    projects = {
        "Digital Yoga Trainer": {
            "description": "Developed a lightweight solution for real-time Yoga pose estimation and correction using MediaPipe and OpenCV.",
            "stack": ["Python", "MediaPipe", "OpenCV", "NumPy"],
            "github": "https://github.com/dev856/Yoga-Pose-Estimation",
            "type": "Computer Vision",
            "impact": "Real-time posture feedback",
            "role": "Pose estimation pipeline"
        },
        "Multi-label Dataset Prediction": {
            "description": "Engineered a winning solution for a Kaggle-style competition. Employed RandomForest and a meta-learning approach with Logistic Regression, achieving 75% accuracy.",
            "stack": ["Python", "Scikit-Learn", "Pandas", "Meta-learning"],
            "github": "https://github.com/dev856",
            "type": "Machine Learning",
            "impact": "75% predictive accuracy",
            "role": "Modeling and evaluation"
        },
        "Tone Topic - Topic Modeling Tool": {
            "description": "Built a Streamlit application that uses Latent Dirichlet Allocation (LDA) for topic modeling on text and CSV data to gather insights.",
            "stack": ["Streamlit", "NLTK", "Gensim", "Pandas"],
            "github": "https://github.com/dev856",
            "type": "NLP",
            "impact": "Interactive topic exploration",
            "role": "End-to-end app build"
        }
    }

    project_types = ["All"] + sorted({details["type"] for details in projects.values()})
    selected_type = st.pills("Project type", project_types, default="All")
    search_term = st.text_input("Search projects or tech stack", placeholder="Try Python, Streamlit, NLP...")

    filtered_projects = []
    for title, details in projects.items():
        search_blob = " ".join([title, details["description"], details["type"], *details["stack"]]).lower()
        type_match = selected_type == "All" or details["type"] == selected_type
        search_match = not search_term or search_term.lower() in search_blob
        if type_match and search_match:
            filtered_projects.append((title, details))

    if not filtered_projects:
        st.info("No projects match the current filters.")
        return

    project_cards = []
    for title, details in filtered_projects:
        tags = render_tag_cloud(details["stack"], "project-tags")
        project_cards.append(
            '<article class="project-panel">'
            f'<div class="project-panel-top"><span>{safe_text(details["type"])}</span></div>'
            f'<div class="premium-card-title">{safe_text(title)}</div>'
            '<div class="project-outcome-grid">'
            f'<div class="project-outcome"><span>Outcome</span><strong>{safe_text(details["impact"])}</strong></div>'
            f'<div class="project-outcome"><span>Role</span><strong>{safe_text(details["role"])}</strong></div>'
            '</div>'
            f'<p>{safe_text(details["description"])}</p>'
            f'{tags}'
            f'<a class="project-link" href="{safe_text(details["github"])}" target="_blank">Open GitHub</a>'
            '</article>'
        )
    st.html(f'<div class="project-grid">{ "".join(project_cards) }</div>')


def resume_section():
    st.markdown('<div class="section-header">Resume</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-kicker">
            Download or review the current resume with education, projects, experience, and technical skills.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_section_stats([
        {"label": "Document", "value": "PDF", "detail": "One concise resume covering education, projects, skills, and experience."},
        {"label": "Best Fit", "value": "Internship", "detail": "Software engineering, data science, applied AI, and analytics roles."},
        {"label": "Review Path", "value": "Download", "detail": "Use the button below for the latest local resume file."},
    ])
    resume_path = "assets/Profile.pdf"

    try:
        with open(resume_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        
        # Download button remains the same
        st.download_button(
            label="📥 Download Resume", 
            data=pdf_bytes, 
            file_name="Resume-Dev-kotak.pdf", 
            mime="application/pdf"  # Corrected MIME type for PDF
        )
        
        # Use st.pdf to display the PDF (requires streamlit-pdf package)
        st.pdf(pdf_bytes, height=800)  # Using st.pdf introduced in v1.49

    except FileNotFoundError:
        st.error("Resume PDF not found. Please make sure 'assets/Profile.pdf' exists.")

def contact_section():
    st.markdown('<div class="section-header">Get In Touch</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-kicker">
            Open to internship conversations, applied AI work, data products, and software engineering collaborations.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_section_stats([
        {"label": "Best Channel", "value": "Email", "detail": "Best for internship opportunities and project details."},
        {"label": "Quick Intro", "value": "LinkedIn", "detail": "Good for short messages, referrals, and professional context."},
        {"label": "Code", "value": "GitHub", "detail": "Project repos and technical work samples."},
    ])
    col1, col2 = st.columns([1, 1])
    with col1:
        st.html(
            '<div class="contact-intro">'
            '<strong>Let’s talk about useful technical work.</strong>'
            '<p>I am open to internship conversations, applied AI work, data products, and software engineering projects.</p>'
            '</div>'
        )
        st.markdown(
            f"""
            <div class="contact-actions">
                <a href="{SOCIAL_MEDIA['Email']}" target="_blank">Email</a>
                <a href="{SOCIAL_MEDIA['LinkedIn']}" target="_blank">LinkedIn</a>
                <a href="{SOCIAL_MEDIA['GitHub']}" target="_blank">GitHub</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form(key="contact_form", clear_on_submit=True):
            name = st.text_input("Your Name", placeholder="John Doe")
            email = st.text_input("Your Email", placeholder="john.doe@example.com")
            message = st.text_area("Your Message", placeholder="Hi Dev, let's connect!")
            if st.form_submit_button(label="Send Message"):
                if not all([name, email, message]):
                    st.warning("Please fill out all fields.")
                elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
                    st.warning("Please enter a valid email address.")
                else:
                    conn = sqlite3.connect('portfolio_contacts.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
                    conn.commit()
                    conn.close()
                    st.success("Thank you for your message! I'll get back to you soon.")
    with col2:
        st.markdown(
            """
            <div class="contact-panel">
                <span class="card-eyebrow">Response Channels</span>
                <h3>Best ways to reach me</h3>
                <p>Email is best for opportunities and project discussions. LinkedIn works well for quick introductions.</p>
                <div>
                    <span>Internships</span>
                    <span>Applied AI</span>
                    <span>Data projects</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def skills_section():
    st.markdown('<div class="section-header">Technical Skills</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-kicker">
            A focused, practical stack for building data-driven software, machine learning workflows, and interactive analytics products.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_section_stats([
        {"label": "Core Stack", "value": "15+", "detail": "Languages, ML tools, cloud, and visualization libraries."},
        {"label": "Primary Focus", "value": "Data + AI", "detail": "Applied machine learning, analytics, and product-facing dashboards."},
        {"label": "Delivery Tools", "value": "Streamlit", "detail": "Fast prototypes, interactive apps, and stakeholder-ready reporting."},
    ])

    skills_data = {
        "Programming & Databases": {
            "summary": "Core engineering tools for backend logic, data processing, and persistence.",
            "skills": {"Python": 95, "SQL": 90, "Java": 80, "C/C++": 75, "MongoDB": 70},
            "focus": ["Backend logic", "Data modeling", "Query design"],
            "accent": "#60a5fa",
        },
        "Data Science & ML": {
            "summary": "Applied machine learning, model experimentation, and statistical data workflows.",
            "skills": {"Pandas & NumPy": 95, "Scikit-Learn": 90, "TensorFlow": 85, "PyTorch": 80, "NLTK": 80},
            "focus": ["Modeling", "Experimentation", "NLP"],
            "accent": "#34d399",
        },
        "Web, Cloud & Visualization": {
            "summary": "Tools for shipping usable interfaces, dashboards, and visual analytics.",
            "skills": {"Streamlit": 90, "Git & GitHub": 90, "Plotly": 85, "HTML/CSS": 80, "GCP": 75},
            "focus": ["Dashboards", "Version control", "Cloud basics"],
            "accent": "#a78bfa",
        },
    }

    cards = []
    for index, (category, details) in enumerate(skills_data.items(), start=1):
        skill_rows = "".join(
            '<div class="premium-skill-row">'
            f'<div><strong>{html.escape(skill, quote=False)}</strong><span>{level}%</span></div>'
            f'<div class="premium-skill-bar"><i style="--level: {level}%"></i></div>'
            '</div>'
            for skill, level in details["skills"].items()
        )
        focus_tags = "".join(
            f"<span>{html.escape(item, quote=False)}</span>" for item in details["focus"]
        )
        cards.append(
            '<article class="premium-skill-card" '
            f'style="--card-accent: {details["accent"]};">'
            '<div class="premium-card-head">'
            '<span class="card-eyebrow">Skill Area</span>'
            f'<span class="premium-card-index">{index:02d}</span>'
            '</div>'
            f'<div class="premium-card-title">{html.escape(category, quote=False)}</div>'
            f'<p>{html.escape(details["summary"], quote=False)}</p>'
            f'<div class="premium-focus-tags">{focus_tags}</div>'
            f'{skill_rows}'
            '</article>'
        )

    st.html(f'<div class="premium-skill-grid">{"".join(cards)}</div>')

    st.markdown("#### Core Tooling")
    tools = [
        "Python", "SQL", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch",
        "Streamlit", "Plotly", "Git", "GitHub", "Google Cloud", "MongoDB", "HTML/CSS"
    ]
    st.html(
        '<div class="premium-tool-cloud">'
        + "".join(f"<span>{html.escape(tool, quote=False)}</span>" for tool in tools)
        + "</div>"
    )


def education_section():
    st.markdown('<div class="section-header">Education Journey</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-kicker">
            Academic training across computer science, electrical and computer engineering, and data science.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_section_stats([
        {"label": "Graduate Focus", "value": "M.Eng", "detail": "Electrical and Computer Engineering with Data Science specialization."},
        {"label": "Foundation", "value": "B.Tech", "detail": "Computer Science and Engineering with strong software fundamentals."},
        {"label": "Academic Strength", "value": "CGPA", "detail": "Strong performance across graduate and undergraduate coursework."},
    ])

    education_summary = [
        {
            "degree": "Master of Engineering - Electrical & Computer Engineering",
            "school": "Carleton University",
            "duration": "2023 - 2025",
            "level": "Graduate",
            "focus": "Collaborative Specialization in Data Science",
            "details": ["CGPA: 10.5 / 12.0", "Pattern Classification", "Applied Programming", "Advanced Data Visualization", "Secure Networking"],
            "accent": "#60a5fa",
        },
        {
            "degree": "Bachelor of Technology - Computer Science & Engineering",
            "school": "Charotar University of Science and Technology",
            "duration": "2019 - 2023",
            "level": "Undergraduate",
            "focus": "Computer science and software engineering foundation",
            "details": ["CGPA: 9.25 / 10.0", "WES Evaluated: 3.92 / 4.0", "Merit scholarship recipient", "Machine Learning", "Software Engineering"],
            "accent": "#34d399",
        },
        {
            "degree": "Higher Secondary Education",
            "school": "Hiramohan Vidhyalaya",
            "duration": "2017 - 2019",
            "level": "Senior Secondary",
            "focus": "Physics, Chemistry, and Mathematics",
            "details": ["Percentage: 82%", "Grade A2", "Science stream"],
            "accent": "#fbbf24",
        },
        {
            "degree": "Secondary Education",
            "school": "Ultravision Academy",
            "duration": "2016 - 2017",
            "level": "Secondary",
            "focus": "Secondary education with distinction",
            "details": ["Completed secondary education with distinction"],
            "accent": "#a78bfa",
        },
    ]

    cards = []
    for entry in education_summary:
        detail_tags = "".join(
            f"<span>{html.escape(detail, quote=False)}</span>" for detail in entry["details"]
        )
        cards.append(
            '<article class="premium-education-card" '
            f'style="--edu-accent: {entry["accent"]};">'
            '<div class="education-card-top">'
            f'<span class="education-duration">{html.escape(entry["duration"], quote=False)}</span>'
            f'<span class="education-level">{html.escape(entry["level"], quote=False)}</span>'
            '</div>'
            f'<div class="premium-card-title">{html.escape(entry["degree"], quote=False)}</div>'
            f'<strong class="education-school">{html.escape(entry["school"], quote=False)}</strong>'
            f'<p>{html.escape(entry["focus"], quote=False)}</p>'
            f'<div class="education-tags">{detail_tags}</div>'
            '</article>'
        )

    st.html(f'<div class="premium-education-grid">{"".join(cards)}</div>')

    st.markdown("#### Academic Coursework")
    coursework = {
        "Graduate Focus": ["Applied Programming", "Pattern Classification", "Data Science Seminar", "Advanced Data Visualization", "Cryptography Implementation"],
        "Computer Science Foundation": ["Data Structures", "Algorithms", "Database Management", "Machine Learning", "Artificial Intelligence", "Computer Networks"],
        "Software Practice": ["Software Engineering", "Object Oriented Programming", "Java Programming", "Python Programming", "Major Software Project"],
    }
    course_cards = []
    for group, courses in coursework.items():
        course_cards.append(
            '<article class="coursework-card">'
            f'<span class="card-eyebrow">{html.escape(group, quote=False)}</span>'
            f'<div>{"".join(f"<span>{html.escape(course, quote=False)}</span>" for course in courses)}</div>'
            '</article>'
        )
    st.html(f'<div class="coursework-grid">{"".join(course_cards)}</div>')


# --- PAGE ROUTING ---
PAGES = {"About Me": about_me_section, "Experience": experience_section, "Skills": skills_section, "Education": education_section, "Projects": projects_section, "Resume": resume_section, "Contact": contact_section}
if choose in PAGES:
    PAGES[choose]()
else:
    st.error("Page not found!")

# --- FOOTER ---
st.markdown("---")
# UPDATED: Year changed to 2025
st.markdown("<p style='text-align: center; color: #94A3B8;'> </p>", unsafe_allow_html=True)
