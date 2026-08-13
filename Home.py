from __future__ import annotations

import base64
import html
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parent
EMAIL = "devhkotak@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/dev-kotak/"
GITHUB = "https://github.com/dev856"
NAV_ITEMS = [
    "Overview",
    "Projects",
    "Experience",
    "Skills",
    "Education",
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


st.set_page_config(
    page_title="Dev Kotak · Software & Machine Learning",
    page_icon=str(ROOT / "assets" / "phot.jpeg"),
    layout="wide",
    initial_sidebar_state="expanded",
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


def site_footer() -> None:
    st.markdown(
        f"""
        <footer class="site-footer">
          <div>
            <span>Dev Kotak</span> · <span>Software &amp; Machine Learning</span> · <span>Ottawa, Canada</span>
          </div>
          <div class="site-footer-links">
            <a href="{LINKEDIN}" target="_blank" rel="noreferrer">LinkedIn</a>
            <a href="{GITHUB}" target="_blank" rel="noreferrer">GitHub</a>
            <a href="mailto:{EMAIL}">Email</a>
          </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def timeline_item(role: dict[str, object]) -> None:
    company = str(role["company"])
    logo = role.get("logo")
    if logo:
        uri = as_data_uri(ROOT / str(logo))
        logo_html = f'<img class="timeline-logo" src="{uri}" alt="{safe(company)}" />' if uri else ""
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
        if image_path and (ROOT / image_path).exists():
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
            st.link_button("Open live application", str(project["demo"]))
        if project.get("repo"):
            st.link_button(str(project.get("repo_label", "View repository")), str(project["repo"]))


# Inject CSS
css_content = (ROOT / "styles" / "main.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


profile_path = ROOT / "assets" / "phot.jpeg"
resume_path = ROOT / "Resume-Dev.pdf"
if not resume_path.exists():
    resume_path = ROOT / "assets" / "Profile.pdf"

profile_uri = as_data_uri(profile_path)
resume_uri = as_data_uri(resume_path)

# Initialize navigation in session state
if "nav" not in st.session_state:
    st.session_state.nav = "Overview"

with st.sidebar:
    if profile_uri:
        st.markdown(
            f"""
            <div class="brand">
              <div class="portrait sm">
                <div class="portrait-frame"><img src="{profile_uri}" alt="Dev Kotak" /></div>
              </div>
              <p class="brand-kicker">Portfolio</p>
              <h2 class="brand-name">Dev Kotak</h2>
              <p class="brand-role">Software &amp; machine learning engineer</p>
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
              <p class="brand-kicker">Portfolio</p>
              <h2 class="brand-name">Dev Kotak</h2>
              <p class="brand-role">Software &amp; machine learning engineer</p>
              <div class="status-pill"><span class="status-dot"></span>Open to opportunities</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.divider()
    page = st.radio("Section", NAV_ITEMS, label_visibility="collapsed", key="nav")
    st.divider()
    st.caption("Available for software engineering, data science, and applied AI appointments.")
    st.link_button("LinkedIn", LINKEDIN, width="stretch")
    st.link_button("GitHub", GITHUB, width="stretch")


if page == "Overview":
    st.markdown(
        """
        <div class="hero">
          <p class="section-kicker">Software &amp; machine learning</p>
          <h1>I build <em class="serif-accent">useful software</em> from data and models.</h1>
          <p class="section-description">Master of Engineering graduate in Electrical &amp; Computer Engineering (Data Science). Experienced across product integrations, applied machine learning, computer vision, and interactive analytics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    hero_left, hero_right = st.columns([1.35, 0.65], vertical_alignment="center")
    with hero_left:
        st.markdown(
            """
            <div class="practice">
              <h3>A measured, product-minded practice</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write(
            "I work across the full engineering path—from raw and incomplete data to experimental models, and ultimately to dependable, production-ready interfaces that people can actually use."
        )
        resume_href = f' href="{resume_uri}" download="Dev-Kotak-Resume.pdf"' if resume_uri else ' href="#"'
        st.markdown(
            f"""
            <div class="hero-actions">
              <a class="btn btn-primary" href="#selected-work">Explore Selected Work <span aria-hidden="true">→</span></a>
              <a class="btn btn-ghost"{resume_href}>Download Résumé</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with hero_right:
        if profile_uri:
            st.markdown(
                f"""
                <figure class="portrait hero-media">
                  <div class="portrait-frame"><img src="{profile_uri}" alt="Portrait of Dev Kotak" /></div>
                  <figcaption class="portrait-caption"><strong>Dev Kotak</strong><span>Ottawa, ON</span></figcaption>
                </figure>
                """,
                unsafe_allow_html=True,
            )
    st.divider()
    st.markdown(
        """
        <div class="stat-grid">
          <div class="stat-card">
            <p class="stat-index">01</p>
            <p class="stat-value">7</p>
            <p class="stat-label">Industry &amp; Research Roles</p>
          </div>
          <div class="stat-card">
            <p class="stat-index">02</p>
            <p class="stat-value">M.Eng</p>
            <p class="stat-label">Carleton (Data Science)</p>
          </div>
          <div class="stat-card">
            <p class="stat-index">03</p>
            <p class="stat-value">5+</p>
            <p class="stat-label">Deployed ML &amp; Web Apps</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<span id="selected-work"></span>', unsafe_allow_html=True)
    st.markdown("## Selected work")
    st.write("A concise set of projects showing how I approach modeling, interfaces, and delivery.")
    st.markdown(
        """
        <div class="mini-grid">
          <div class="mini-card">
            <div>
              <p class="mini-index">01</p>
              <p class="mini-meta">Natural language processing</p>
              <h3>Tone Topic</h3>
              <p>Topic modeling and document labeling for unstructured text and CSV datasets using LDA &amp; NLTK.</p>
            </div>
          </div>
          <div class="mini-card">
            <div>
              <p class="mini-index">02</p>
              <p class="mini-meta">Computer vision</p>
              <h3>Digital Yoga Trainer</h3>
              <p>Real-time pose estimation and corrective posture feedback using MediaPipe landmark detection and OpenCV.</p>
            </div>
          </div>
          <div class="mini-card">
            <div>
              <p class="mini-index">03</p>
              <p class="mini-meta">Machine learning</p>
              <h3>Multi-label Prediction</h3>
              <p>Competition-grade model stacking combining Random Forests with a Logistic Regression meta-learner (75% accuracy).</p>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("View the full project portfolio", type="primary"):
        st.session_state.nav = "Projects"
        st.rerun()

    st.markdown(
        """
        <div class="marquee"><div class="marquee-track">
        <span>Python</span><span>SQL</span><span>REST APIs</span><span>JSON</span><span>TensorFlow</span><span>PyTorch</span>
        <span>Streamlit</span><span>Plotly</span><span>OpenCV</span><span>MediaPipe</span><span>Google Cloud</span><span>Pandas</span>
        <span>NumPy</span><span>Git</span><span>Node.js</span><span>MongoDB</span><span>Scikit-Learn</span><span>NLTK</span>
        <span>Python</span><span>SQL</span><span>REST APIs</span><span>JSON</span><span>TensorFlow</span><span>PyTorch</span>
        <span>Streamlit</span><span>Plotly</span><span>OpenCV</span><span>MediaPipe</span><span>Google Cloud</span><span>Pandas</span>
        <span>NumPy</span><span>Git</span><span>Node.js</span><span>MongoDB</span><span>Scikit-Learn</span><span>NLTK</span>
        </div></div>
        """,
        unsafe_allow_html=True,
    )


elif page == "Projects":
    st.markdown('<span id="projects"></span>', unsafe_allow_html=True)
    section_header(
        "Selected projects",
        "Work I can explain end to end.",
        "Each project is presented through the real-world problem, the implementation details, and the measurable outcome.",
    )
    with st.container(border=True):
        left, right = st.columns([1.2, 1], vertical_alignment="center")
        with left:
            st.image(str(ROOT / "images" / "screen06.jpg"), width="stretch")
        with right:
            st.markdown('<p class="project-type">Featured · Natural language processing</p>', unsafe_allow_html=True)
            st.markdown("### Tone Topic")
            st.write(
                "An interactive Streamlit application that transforms raw unstructured text or uploaded CSV documents into explorable semantic topic models using Latent Dirichlet Allocation (LDA)."
            )
            st.markdown(
                "**Outcome:** Real-time topic distribution &amp; token extraction<br>**Contribution:** End-to-end NLP pipeline and interactive UI",
                unsafe_allow_html=True,
            )
            tag_row(["Python", "Streamlit", "NLTK", "Gensim", "Pandas", "Topic Modeling"])
            st.link_button("Open live application", "https://tonetopic.streamlit.app/")

    st.write("")
    grid_left, grid_right = st.columns(2)
    with grid_left:
        project_card(
            {
                "type": "Computer vision",
                "title": "Digital Yoga Trainer",
                "description": "Real-time pose estimation and correction using MediaPipe body landmark coordinates and OpenCV angle calculations to deliver live posture feedback.",
                "outcome_label": "Outcome",
                "outcome": "Live posture tracking and corrective feedback",
                "tags": ["Python", "MediaPipe", "OpenCV", "NumPy", "Real-time Vision"],
                "repo": "https://github.com/dev856/Yoga-Pose-Estimation",
                "repo_label": "View GitHub repository",
            }
        )
        project_card(
            {
                "type": "Data Analytics & Exploration",
                "title": "InsightSync",
                "description": "Interactive data analytics workbench enabling multi-variate statistical distributions, correlation matrices, and automated data visualization for complex datasets.",
                "outcome_label": "Outcome",
                "outcome": "Instant exploratory analysis & dynamic charts",
                "tags": ["Python", "Streamlit", "Plotly", "Pandas", "Data Analytics"],
                "demo": "https://insight-sync.streamlit.app/",
            }
        )

    with grid_right:
        project_card(
            {
                "type": "Machine learning",
                "title": "Multi-label Dataset Prediction",
                "description": "A high-performing competitive modeling solution combining Random Forest base estimators with a Logistic Regression meta-classifier for complex multi-label classification.",
                "outcome_label": "Result",
                "outcome": "75% measured predictive accuracy",
                "tags": ["Python", "Scikit-Learn", "Pandas", "Meta-learning", "Ensemble Methods"],
                "repo": GITHUB,
                "repo_label": "Explore GitHub profile",
            }
        )
        project_card(
            {
                "type": "Computer Vision & Manufacturing",
                "title": "FabriSense",
                "description": "Automated textile inspection and defect detection solution utilizing computer vision preprocessing and classification algorithms.",
                "outcome_label": "Outcome",
                "outcome": "Automated anomaly identification",
                "tags": ["Python", "Streamlit", "OpenCV", "Image Processing"],
                "demo": "http://fabrisense.streamlit.app/",
            }
        )


elif page == "Experience":
    section_header(
        "Experience",
        "From research prototypes to product workflows.",
        "Current-first timeline detailing responsibilities, software architectures, and technical achievements.",
    )
    roles = [
        {
            "date": "Jul 2024 — Present",
            "role": "Computer Science Student",
            "company": "Ottawa Centre for Cognitive Therapy",
            "summary": "Building data workflows, system integrations, and automation pipelines across EHR and client scheduling platforms.",
            "bullets": [
                "Implemented REST API integrations that streamlined cross-platform data synchronization and improved interaction efficiency by 50%.",
                "Designed JSON-based scheduling workflows and automation scripts that increased system responsiveness by 30%.",
            ],
            "tags": ["REST APIs", "JSON", "System Integration", "Workflow Automation", "Python"],
        },
        {
            "date": "Dec 2022 — May 2023",
            "role": "Research Intern",
            "company": "Space Applications Centre, ISRO",
            "summary": "Applied geospatial data science and machine learning to hydrological flux estimation across Indian river basins.",
            "bullets": [
                "Processed multi-spectral MODIS, CHIRPS, ERA5/CFSR, and TRMM satellite observations using Python and Google Earth Engine.",
                "Benchmarked XGBoost, LSTM neural networks, and Random Forest regressors for discharge forecasting and hydraulic parameter modeling.",
            ],
            "tags": ["Python", "Google Earth Engine", "XGBoost", "LSTM", "Geospatial Data"],
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
            ],
            "tags": ["Python", "SQL", "Machine Learning", "Prompt Engineering", "Data Modeling"],
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
            ],
            "tags": ["TensorFlow", "YOLO", "Dlib", "OpenCV", "Computer Vision"],
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
            "tags": ["Python", "Scikit-Learn", "Pandas", "Statistical Modeling"],
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
            "tags": ["Node.js", "Express", "MongoDB", "REST APIs"],
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
            "tags": ["Python", "Data Science", "Exploratory Analysis", "Visualization"],
            "logo": "images/spark.png",
        },
    ]
    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    for role in roles:
        timeline_item(role)
    st.markdown("</div>", unsafe_allow_html=True)


elif page == "Skills":
    section_header(
        "Capabilities",
        "Skills backed by applied work.",
        "Grouped by engineering domain, showing how each tool is leveraged in real production and research projects.",
    )
    groups = [
        (
            "01",
            "Software & Systems",
            "Backend logic, API architectures, schema design, and dependable data pipelines.",
            ["Python", "SQL", "REST APIs", "JSON", "Java", "Node.js", "MongoDB", "C/C++", "Linux"],
        ),
        (
            "02",
            "Data Science & ML",
            "Statistical modeling, model evaluation, NLP pipelines, and computer vision algorithms.",
            ["Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "NLTK", "OpenCV", "MediaPipe", "Gensim"],
        ),
        (
            "03",
            "Product & Delivery",
            "Interactive dashboards, cloud environments, version control, and stakeholder interfaces.",
            ["Streamlit", "Plotly", "Git", "GitHub", "Google Cloud", "Docker Basics", "HTML5/CSS3"],
        ),
    ]
    cards = "".join(
        '<div class="skill-card">'
        f'<span class="skill-index">{index}</span>'
        f"<div>"
        f"<h3>{safe(title)}</h3>"
        f"<p>{safe(summary)}</p>"
        f"</div>"
        f'<div class="tag-row">{tag_html(skills)}</div>'
        "</div>"
        for index, title, summary, skills in groups
    )
    st.markdown(f'<div class="skill-grid">{cards}</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("### Engineering Methodologies")
    meth_left, meth_right = st.columns(2)
    with meth_left:
        with st.container(border=True):
            st.markdown("#### Applied Machine Learning & Evaluation")
            st.write(
                "Experience selecting appropriate model architectures (tree ensembles, neural networks, linear meta-models), conducting stratified cross-validation, and optimizing metrics beyond basic accuracy (precision, recall, ROC-AUC, F1)."
            )
            tag_row(["Cross-Validation", "Hyperparameter Tuning", "Ensemble Stacking", "Feature Importance"])

    with meth_right:
        with st.container(border=True):
            st.markdown("#### Systems Integration & API Design")
            st.write(
                "Experience connecting disparate software systems via structured RESTful APIs, designing deterministic JSON schema contracts, and automating repetitive data synchronization tasks."
            )
            tag_row(["REST Architecture", "JSON Schemas", "Authentication Flows", "Asynchronous Processing"])


elif page == "Education":
    section_header(
        "Education",
        "A systems foundation with a data science focus.",
        "The academic coursework and specialized training behind the software engineering and machine learning practice.",
    )
    carleton_uri = as_data_uri(ROOT / "images" / "carleton.jpg")
    charusat_uri = as_data_uri(ROOT / "images" / "charusat.jpg")
    st.markdown(
        f"""
        <div class="edu-grid">
          <div class="edu-card">
            <img class="edu-logo" src="{carleton_uri}" alt="Carleton University" />
            <span class="date-pill">2023 — 2025 · Graduate</span>
            <h3>Master of Engineering</h3>
            <p>Electrical &amp; Computer Engineering · Collaborative Specialization in Data Science</p>
            <p><strong>CGPA:</strong> 10.5 / 12.0 &nbsp;·&nbsp; <strong>Location:</strong> Ottawa, Canada</p>
            <strong class="edu-school">Carleton University</strong>
          </div>
          <div class="edu-card">
            <img class="edu-logo" src="{charusat_uri}" alt="CHARUSAT" />
            <span class="date-pill">2019 — 2023 · Undergraduate</span>
            <h3>Bachelor of Technology</h3>
            <p>Computer Science &amp; Engineering</p>
            <p><strong>CGPA:</strong> 9.25 / 10.0 (WES: 3.92 / 4.0) &nbsp;·&nbsp; <strong>Merit Scholarship</strong></p>
            <strong class="edu-school">Charotar University of Science and Technology</strong>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown("### Academic Coursework")
    st.markdown(
        """
        <div class="coursework-grid">
          <div class="coursework-card">
            <h4>Graduate Specialization</h4>
            <ul>
              <li>Applied Programming &amp; Algorithms</li>
              <li>Pattern Classification &amp; Machine Learning</li>
              <li>Advanced Data Visualization</li>
              <li>Data Science Seminar &amp; Research</li>
              <li>Cryptography &amp; Network Security</li>
            </ul>
          </div>
          <div class="coursework-card">
            <h4>Computer Science Foundation</h4>
            <ul>
              <li>Data Structures &amp; Algorithms</li>
              <li>Database Management Systems (SQL)</li>
              <li>Operating Systems &amp; System Architecture</li>
              <li>Computer Networks &amp; Protocols</li>
              <li>Object-Oriented Programming (Java)</li>
            </ul>
          </div>
          <div class="coursework-card">
            <h4>Applied Engineering</h4>
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


elif page == "Résumé":
    section_header(
        "Résumé",
        "A concise view of credentials and experience.",
        "Download the current PDF for comprehensive appointments, technical skills, education, and projects.",
    )
    st.markdown(
        """
        <div class="resume-panel">
          <p class="section-kicker">Curriculum vitae</p>
          <h3>Dev Kotak · Current Résumé</h3>
          <p>Complete record of academic credentials, software &amp; machine learning appointments, technical skills, and selected projects.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    if resume_path.exists():
        st.download_button(
            "Download Résumé PDF",
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
            st.markdown("#### Key Qualifications")
            st.write(
                "- **Graduate Degree:** M.Eng in Electrical & Computer Engineering with Data Science Specialization from Carleton University.\n"
                "- **7 Appointments:** Experience across ISRO (Space Applications Centre), Ottawa Centre for Cognitive Therapy, Jupiter AI Labs, and Zummit Infolabs.\n"
                "- **Core Stack:** Python, SQL, REST APIs, Streamlit, Pandas, Scikit-Learn, TensorFlow, OpenCV, MediaPipe."
            )
    with summary_right:
        with st.container(border=True):
            st.markdown("#### Primary Competencies")
            st.write(
                "- **Applied Machine Learning:** Classification, Regression, Ensemble Stacking, Evaluation Metrics.\n"
                "- **Computer Vision & NLP:** Pose estimation, Object Detection, Topic Modeling, Text Extraction.\n"
                "- **Product Delivery:** Rapid prototyping with Streamlit, Plotly visual analytics, RESTful backend APIs."
            )


elif page == "Contact":
    section_header(
        "Correspondence",
        "Have a problem to solve?",
        "Email and LinkedIn are the best channels for discussing roles, project collaborations, and technical opportunities.",
    )
    st.markdown(
        f"""
        <div class="letter-card">
          <p class="section-kicker">Direct Contact</p>
          <p class="letter-email"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
          <p>Open to software engineering, data science, and applied machine learning roles in Ottawa, across Canada, and remotely.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    email_col, linkedin_col, github_col = st.columns(3)
    with email_col:
        st.link_button("Write an email", f"mailto:{EMAIL}", width="stretch")
    with linkedin_col:
        st.link_button("LinkedIn Profile", LINKEDIN, width="stretch")
    with github_col:
        st.link_button("GitHub Profile", GITHUB, width="stretch")

    st.write("")
    st.markdown("### Send a direct message")
    with st.form("contact_form", clear_on_submit=True):
        f_left, f_right = st.columns(2)
        with f_left:
            name = st.text_input("Your Name *", placeholder="e.g. Alex Morgan")
        with f_right:
            sender_email = st.text_input("Your Email *", placeholder="e.g. alex@company.com")
        subject = st.text_input("Subject", placeholder="e.g. Software Engineering Role / Project Discussion")
        message = st.text_area("Message *", placeholder="Write your message here...", height=130)
        submitted = st.form_submit_button("Send Message", type="primary")

        if submitted:
            if not name.strip() or not sender_email.strip() or not message.strip():
                st.error("Please fill in all required fields (Name, Email, and Message).")
            elif "@" not in sender_email or "." not in sender_email:
                st.error("Please enter a valid email address.")
            else:
                st.success(f"Thank you, {safe(name)}! Your message has been noted. You can also reach me directly at {EMAIL}.")


site_footer()
