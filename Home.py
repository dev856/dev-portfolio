from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parent
EMAIL = "devhkotak@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/dev-kotak/"
GITHUB = "https://github.com/dev856"

MIME_BY_SUFFIX = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".pdf": "application/pdf",
}


st.set_page_config(
    page_title="Dev Kotak | Software & ML Engineer",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="auto",
)


def safe(value: object) -> str:
    return html.escape(str(value), quote=True)


def as_data_uri(path: Path) -> str | None:
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


def section_header(kicker: str, title: str, description: str | None = None) -> None:
    st.markdown(f'<p class="section-kicker">{safe(kicker)}</p>', unsafe_allow_html=True)
    st.title(title)
    if description:
        st.markdown(f'<p class="section-description">{safe(description)}</p>', unsafe_allow_html=True)


def timeline_item(role: dict[str, object]) -> None:
    company = str(role["company"])
    logo = role.get("logo")
    if logo:
        uri = as_data_uri(ROOT / str(logo))
        logo_html = f'<img class="timeline-logo" src="{uri}" alt="" />' if uri else ""
    else:
        logo_html = f'<span class="timeline-logo timeline-logo-fallback">{initials(company)}</span>'
    bullets = "".join(f"<li>{safe(b)}</li>" for b in role["bullets"])
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
              <span class="date-pill">{safe(role['date'])}</span>
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
        if image_path:
            st.image(str(ROOT / image_path), width="stretch")
        st.markdown(f'<p class="project-type">{safe(project["type"])}</p>', unsafe_allow_html=True)
        st.subheader(str(project["title"]))
        st.write(str(project["description"]))
        st.markdown(
            f'<p class="project-outcome"><strong>{safe(project["outcome_label"])}:</strong> {safe(project["outcome"])}</p>',
            unsafe_allow_html=True,
        )
        tag_row(project["tags"])
        if project.get("demo"):
            st.link_button("Open live app", str(project["demo"]))
        if project.get("repo"):
            st.link_button(str(project.get("repo_label", "View repository")), str(project["repo"]))


st.markdown(f"<style>{(ROOT / 'styles' / 'main.css').read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


profile_path = ROOT / "assets" / "phot.jpeg"
resume_path = ROOT / "assets" / "Profile.pdf"
profile_uri = as_data_uri(profile_path)
resume_uri = as_data_uri(resume_path)

with st.sidebar:
    if profile_uri:
        st.markdown(
            f'<div class="avatar-ring"><img src="{profile_uri}" alt="Dev Kotak" /></div>',
            unsafe_allow_html=True,
        )
    st.markdown("## Dev Kotak")
    st.markdown(
        '<div class="status-pill"><span class="status-dot"></span>Available for work</div>',
        unsafe_allow_html=True,
    )
    st.divider()
    page = st.radio(
        "Explore",
        ["👋 Overview", "🚀 Projects", "💼 Experience", "🧠 Skills", "🎓 Education", "📄 Résumé", "✉️ Contact"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Open to software engineering, data science, and applied AI opportunities.")
    st.link_button("🔗 LinkedIn", LINKEDIN, width="stretch")
    st.link_button("🐙 GitHub", GITHUB, width="stretch")


if page == "👋 Overview":
    st.markdown(
        """
        <div class="hero">
          <p class="section-kicker">Software &amp; machine learning engineer</p>
          <h1 class="hero-title">I build <span class="serif-accent">useful software</span> from data and models.</h1>
          <p class="section-description">Recent engineering graduate with experience across product integrations, applied machine learning, computer vision, and interactive analytics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    hero_left, hero_right = st.columns([1.35, 0.65], vertical_alignment="center")
    with hero_left:
        st.markdown("### A practical, product-minded approach")
        st.write("I work across the full path from messy data and technical experiments to clear interfaces that people can actually use.")
        resume_href = f' href="{resume_uri}" download="Dev-Kotak-Resume.pdf"' if resume_uri else ' href="#"'
        st.markdown(
            f"""
            <div class="hero-actions">
              <a class="btn btn-primary" href="#selected-work">View projects <span aria-hidden="true">→</span></a>
              <a class="btn btn-ghost"{resume_href}>Download résumé</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hero_right:
        if profile_uri:
            st.markdown(
                f"""
                <div class="hero-media">
                  <div class="avatar-ring lg"><img src="{profile_uri}" alt="Dev Kotak portrait" /></div>
                  <span class="float-chip chip-a">🤖 Applied AI</span>
                  <span class="float-chip chip-b">💼 7+ roles</span>
                  <span class="float-chip chip-c">🎓 M.Eng</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.divider()
    st.markdown(
        """
        <div class="stat-grid">
          <div class="stat-card">
            <span class="stat-icon">💼</span>
            <div><p class="stat-value">7</p><p class="stat-label">Roles</p></div>
          </div>
          <div class="stat-card">
            <span class="stat-icon">🎓</span>
            <div><p class="stat-value">M.Eng</p><p class="stat-label">Education</p></div>
          </div>
          <div class="stat-card">
            <span class="stat-icon">🎯</span>
            <div><p class="stat-value">Data + AI</p><p class="stat-label">Focus</p></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<span id="selected-work"></span>', unsafe_allow_html=True)
    st.markdown("## Selected work")
    st.write("A small set of projects showing how I approach modeling, interfaces, and delivery.")
    st.markdown(
        """
        <div class="mini-grid">
          <div class="mini-card">
            <span class="mini-icon">🧠</span>
            <h3>Tone Topic</h3>
            <p class="mini-meta">NLP · Streamlit</p>
            <p>Topic modeling for text and CSV data.</p>
          </div>
          <div class="mini-card">
            <span class="mini-icon">🧘</span>
            <h3>Digital Yoga Trainer</h3>
            <p class="mini-meta">Computer vision</p>
            <p>Real-time pose estimation and feedback.</p>
          </div>
          <div class="mini-card">
            <span class="mini-icon">🤖</span>
            <h3>Multi-label Prediction</h3>
            <p class="mini-meta">Machine learning</p>
            <p>Model stacking with a measured 75% accuracy result.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.link_button("✨ See all projects", "#projects")
    st.markdown(
        """
        <div class="marquee"><div class="marquee-track">
        <span>Python</span><span>SQL</span><span>REST APIs</span><span>JSON</span><span>TensorFlow</span><span>PyTorch</span>
        <span>Streamlit</span><span>Plotly</span><span>OpenCV</span><span>MediaPipe</span><span>Google Cloud</span><span>Pandas</span>
        <span>NumPy</span><span>Git</span><span>Node.js</span><span>MongoDB</span>
        <span>Python</span><span>SQL</span><span>REST APIs</span><span>JSON</span><span>TensorFlow</span><span>PyTorch</span>
        <span>Streamlit</span><span>Plotly</span><span>OpenCV</span><span>MediaPipe</span><span>Google Cloud</span><span>Pandas</span>
        <span>NumPy</span><span>Git</span><span>Node.js</span><span>MongoDB</span>
        </div></div>
        """,
        unsafe_allow_html=True,
    )


elif page == "🚀 Projects":
    st.markdown('<span id="projects"></span>', unsafe_allow_html=True)
    section_header("Selected projects", "Work I can explain end to end.", "Each project is presented through the problem, the implementation, and the outcome.")
    with st.container(border=True):
        left, right = st.columns([1.2, 1], vertical_alignment="center")
        with left:
            st.image(str(ROOT / "images" / "screen06.jpg"), width="stretch")
        with right:
            st.markdown("### Tone Topic")
            st.caption("Natural language processing")
            st.write("An interactive Streamlit application that turns unstructured text or CSV data into explorable topics using Latent Dirichlet Allocation.")
            st.markdown("**Outcome:** Interactive topic exploration<br>**Contribution:** End-to-end application build", unsafe_allow_html=True)
            tag_row(["Python", "Streamlit", "NLTK", "Gensim", "Pandas"])
            st.link_button("🚀 Open live application", "https://tonetopic.streamlit.app/")
    st.write("")
    left, right = st.columns(2)
    with left:
        project_card({"type": "Computer vision", "title": "Digital Yoga Trainer", "description": "Real-time pose estimation and correction using MediaPipe landmarks and OpenCV.", "outcome_label": "Outcome", "outcome": "Live posture feedback", "tags": ["Python", "MediaPipe", "OpenCV", "NumPy"], "repo": "https://github.com/dev856/Yoga-Pose-Estimation"}, "images/Tadasana.jpg")
    with right:
        project_card({"type": "Machine learning", "title": "Multi-label Dataset Prediction", "description": "A competition solution combining Random Forest predictions with a Logistic Regression meta-learner.", "outcome_label": "Result", "outcome": "75% predictive accuracy", "tags": ["Python", "Scikit-Learn", "Pandas", "Meta-learning"], "repo": GITHUB, "repo_label": "Explore GitHub profile"})


elif page == "💼 Experience":
    section_header("Experience", "From research prototypes to product workflows.", "Current-first experience focused on responsibilities and technical outcomes.")
    roles = [
        {"date": "Jul 2024 — Present", "role": "Computer Science Student", "company": "Ottawa Centre for Cognitive Therapy", "summary": "Building integrations and data workflows across scheduling and CRM/EHR systems.", "bullets": ["Implemented REST API integrations that improved cross-platform data flow and user interaction efficiency by 50%.", "Designed JSON-based scheduling workflows that increased system responsiveness by 30%."], "tags": ["REST APIs", "JSON", "System Integration", "Workflow Automation"]},
        {"date": "Dec 2022 — May 2023", "role": "Research Intern", "company": "Space Applications Centre, ISRO", "summary": "Applied geospatial data and machine learning to hydrological flux estimation across Indian river basins.", "bullets": ["Analyzed MODIS, CHIRPS, ERA5/CFSR, and TRMM data using Google Earth Engine and Python.", "Compared XGBoost, LSTM, and Random Forest models for river discharge and hydraulic parameter prediction."], "tags": ["Python", "Google Earth Engine", "XGBoost", "LSTM"], "logo": "images/isro1.jpeg"},
        {"date": "Dec 2022 — Feb 2023", "role": "Machine Learning Intern", "company": "Jupiter AI Labs", "summary": "Developed practical ML case studies and AI-assisted engineering workflows for client projects.", "bullets": ["Worked across SQL, exploratory analysis, probability, and model evaluation use cases.", "Integrated AI prompt-engineering workflows into Python development and internal project delivery."], "tags": ["Python", "SQL", "Machine Learning", "Prompt Engineering"], "logo": "images/jupiter.png"},
        {"date": "Jun 2022 — Sep 2022", "role": "Data Science Intern", "company": "Zummit Infolabs", "summary": "Built facial feature, emotion classification, and object detection prototypes.", "bullets": ["Developed feature detectors with Dlib and emotion classifiers with TensorFlow.", "Experimented with YOLO-based object detection and reusable computer-vision pipelines."], "tags": ["TensorFlow", "YOLO", "Dlib", "Computer Vision"], "logo": "images/zummit.png"},
    ]
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for role in roles:
        timeline_item(role)
    st.markdown("</div>", unsafe_allow_html=True)
    st.info("Earlier experience: ML Intern at CHARUSAT, Node.js Intern at Kintu Designs, and Data Science Intern at The Sparks Foundation.")


elif page == "🧠 Skills":
    section_header("Capabilities", "Skills backed by applied work.", "Grouped by how I use the technology, not by subjective proficiency percentages.")
    groups = [
        ("Software engineering", "⚙️", "Backend logic, integrations, and dependable data flows.", ["Python", "SQL", "REST APIs", "JSON", "Java", "Node.js", "MongoDB"]),
        ("Data science & ML", "🧠", "Experimentation, evaluation, NLP, and computer vision.", ["Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "NLTK", "OpenCV"]),
        ("Product & delivery", "🚀", "Usable interfaces and clear analytics for technical stakeholders.", ["Streamlit", "Plotly", "Git", "GitHub", "Google Cloud", "MediaPipe", "HTML/CSS"]),
    ]
    cards = "".join(
        '<div class="skill-card">'
        f'<span class="skill-icon">{icon}</span>'
        f"<h3>{safe(title)}</h3>"
        f"<p>{safe(summary)}</p>"
        f'<div class="tag-row">{tag_html(skills)}</div>'
        "</div>"
        for title, icon, summary, skills in groups
    )
    st.markdown(f'<div class="skill-grid">{cards}</div>', unsafe_allow_html=True)


elif page == "🎓 Education":
    section_header("Education", "A systems foundation with a data science focus.", "The academic background behind the engineering and modeling work.")
    carleton_uri = as_data_uri(ROOT / "images" / "carleton.jpg")
    charusat_uri = as_data_uri(ROOT / "images" / "charusat.jpg")
    st.markdown(
        f"""
        <div class="edu-grid">
          <div class="edu-card">
            <img class="edu-logo" src="{carleton_uri}" alt="Carleton University" />
            <span class="date-pill">2023 — 2025 · Graduate</span>
            <h3>Master of Engineering</h3>
            <p>Electrical &amp; Computer Engineering · Data Science specialization</p>
            <strong class="edu-school">Carleton University</strong>
          </div>
          <div class="edu-card">
            <img class="edu-logo" src="{charusat_uri}" alt="CHARUSAT" />
            <span class="date-pill">2019 — 2023 · Undergraduate</span>
            <h3>Bachelor of Technology</h3>
            <p>Computer Science &amp; Engineering</p>
            <strong class="edu-school">Charotar University of Science and Technology</strong>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


elif page == "📄 Résumé":
    section_header("Résumé", "A concise view of my experience.", "Download the current PDF for education, projects, skills, and work history.")
    if resume_path.exists():
        st.download_button("⬇️ Download résumé PDF", resume_path.read_bytes(), "Dev-Kotak-Resume.pdf", "application/pdf")
        st.caption("For the most readable version, download the PDF and open it in a new tab.")
    else:
        st.error("The résumé PDF is not available.")


elif page == "✉️ Contact":
    section_header("Contact", "Have a useful problem to solve?", "Email is the best channel for roles, project discussions, and technical collaborations.")
    with st.container(border=True):
        st.subheader("Direct contact")
        st.markdown(f"### [{EMAIL}](mailto:{EMAIL})")
        st.write("Open to software engineering, data science, and applied AI opportunities.")
        email_col, linkedin_col, github_col = st.columns(3)
        with email_col:
            st.link_button("✉️ Email Dev", f"mailto:{EMAIL}", width="stretch")
        with linkedin_col:
            st.link_button("🔗 LinkedIn", LINKEDIN, width="stretch")
        with github_col:
            st.link_button("🐙 GitHub", GITHUB, width="stretch")
