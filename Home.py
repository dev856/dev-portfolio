import streamlit as st
import base64
from streamlit_option_menu import option_menu
from streamlit.components.v1 import html
from st_on_hover_tabs import on_hover_tabs
import requests
from streamlit_lottie import st_lottie
from PIL import Image
import streamlit_analytics
import base64
from streamlit_extras.mention import mention
from streamlit_extras.app_logo import add_logo
import sqlite3
from bs4 import BeautifulSoup
from streamlit_extras.echo_expander import echo_expander
from custom import GITHUB_PROFILE,LINKEDIN_PROFILE
import streamlit.components.v1 as components
from streamlit_pdf_viewer import pdf_viewer
def home():
    # Page configs (tab title, favicon)
   
    st.set_page_config(
        page_title="Dev Kotak", 
        page_icon="👨‍💻",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.sidebar.success("Select a page below.")

    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    def render_lottie(url, width, height):
        lottie_html = f"""
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.7.14/lottie.min.js"></script>
        </head>
        <body>
            <div id="lottie-container" style="width: {width}; height: {height};"></div>
            <script>
                var animation = lottie.loadAnimation({{
                    container: document.getElementById('container'),
                    renderer: 'svg',
                    loop: true,
                    autoplay: true,
                    path: '{url}'
                }});
                animation.setRendererSettings({{
                    preserveAspectRatio: 'xMidYMid slice',
                    clearCanvas: true,
                    progressiveLoad: false,
                    hideOnTransparent: false
                }});
            </script>
        </body>
        </html>
        """
        return lottie_html
    def load_lottieurl(url):
    # use the request method to send a get to request URL
        r = requests.get(url)
    # if status is successful it will return 
        if r.status_code != 200: 
            return None
    # return the json data of the lottie animation
        return r.json()
    lottie_coding= load_lottieurl("https://lottie.host/68d3c014-d4f6-4c56-91e4-9bf2097244d3/0sOZZzTYjD.json")
    lottie_python = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_2znxgjyt.json")
    lottie_media = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_osdxlbqq.json")
    lottie_github = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_6HFXXE.json")
    lottie_internet = load_lottieurl("https://lottie.host/6f966033-0640-4492-aba8-e069b551b6f4/LtF2FH3ttk.json")

    # Use local CSS
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("styles/main.css")


    # CSS styles file
    with open("styles/main.css") as f:
        st.write(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Profile image file
    with open("assets/phot.jpeg", "rb") as img_file:
        img = "data:image/png;base64," + base64.b64encode(img_file.read()).decode()

    # PDF CV file
    with open("assets/Profile.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    
    # Top title
    st.write(f"""<div class="title"><strong>Hi! My name is</strong> Dev Kotak👋</div>""", unsafe_allow_html=True)

    # Profile image
    st.write(f"""
    <div class="container">
        <div class="box">
            <div class="spin-container">
                <div class="shape">
                    <div class="bd">
                        <img src="{img}" alt="Dev Kotak">
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, 
    unsafe_allow_html=True)

    
       # Custom function for printing text
    def show_pdf(file_path):
        with open(file_path,"rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="400" height="600" type="application/pdf">'
        st.markdown(pdf_display, unsafe_allow_html=True)

    def pdf_link(pdf_url, link_text="Click here to view PDF"):
        href = f'<a href="{pdf_url}" target="_blank">{link_text}</a>'
        return href
    
    custom_css1 = f"""
    <style>
    .stApp {{
            background-image: url("https://cdn.svgator.com/images/2022/06/use-svg-as-background-image-particle-strokes.svg");
            background-size: cover;
        }}
    </style>
    """

    # Display the custom CSS with the SVG background
    st.markdown(custom_css1, unsafe_allow_html=True)
    img_utown = Image.open("images/lh.jpeg")
    img_lh = Image.open("images/lh.jpeg")
    img_ifg = Image.open("images/lh.jpeg")
    sidebar_logo = Image.open("images/logog.png")
    #Assets for internship
    img_bitmetrix = Image.open("images/isro1.jpeg")
    img_scor = Image.open("images/jupiter.png")
    img_zummit = Image.open("images/zummit1.png")
    img_dep = Image.open("images/depstar.png")
    img_kintu = Image.open("images/kintu.jpeg")
    img_spark = Image.open("images/spark.png")
    # Assets for education

    img_carleton = Image.open("images/clogo.png")
    img_nus = Image.open("images/images (1).png")
    img_poc = Image.open("images/hira.jpg")
    img_tpjc = Image.open("images/ultra.jpeg")
    # Assets for projects
    
    image_names_projects = ["Tadasana","screen06"]

    images_projects = [Image.open(f"images/{name}.{'jpg' if name not in ('','') else 'jpg'}") for name in image_names_projects]
    # Assets for volunteering
    image_names_vol = ["crowd2", "csi", "cn","code"]
    images_vol = [Image.open(f"images/{name}.{'jpg' if name not in ('crowd2', 'csi','cn','code') else 'png'}") for name in image_names_vol]
    #img_lottie_animation = Image.open("images/lottie_animation.gif")
    # Assets for contact
    #lottie_coding = load_lottieurl("python_lottie = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_2znxgjyt.json")")

    img_linkedin = Image.open("images/linkedin.png")
    img_github = Image.open("images/github.png")
    img_email = Image.open("images/email.png")
    img_codechef = Image.open("images/codechef.png")

    def social_icons(width=24, height=24, **kwargs):
            icon_template = '''
            <a href="{url}" target="_blank" style="margin-right: 20px;">
                <img src="{icon_src}" alt="{alt_text}" width="{width}" height="{height}">
            </a>
            '''

            icons_html = ""
            for name, url in kwargs.items():
                icon_src = {
                   
                    "linkedin": "https://img.icons8.com/ios-filled/100/ff8c00/linkedin.png",
                    "github": "https://img.icons8.com/ios-filled/100/ff8c00/github--v2.png",
                    "email": "https://img.icons8.com/ios-filled/100/ff8c00/filled-message.png",
                    "codechef": "https://img.icons8.com/?size=100&id=LnZMjt9rZC3d&format=png&color=000000"
                }.get(name.lower())

                if icon_src:
                    icons_html += icon_template.format(url=url, icon_src=icon_src, alt_text=name.capitalize(), width=width, height=height)

            return icons_html
    #####################
    # Custom function for printing text
    def txt(a, b):
        col1, col2 = st.columns([4,1])
        with col1:
            st.markdown(a)
        with col2:
            st.markdown(b)

    def txt2(a, b):
        col1, col2 = st.columns([1,4])
        with col1:
            st.markdown(f'`{a}`')
        with col2:
            st.markdown(b)

    #def txt3(a, b):
    #col1, col2 = st.columns([1,2])
    #with col1:
        #st.markdown(f'<p style="font-size: 20px;">{a}</p>', unsafe_allow_html=True)
    #with col2:
        # Split the text at the comma and wrap each part in backticks separately
        #b_parts = b.split(',')
        #b_formatted = '`' + ''.join(b_parts) + '`'
        #st.markdown(f'<p style="font-size: 20px; font-family: monospace;">{b_formatted}</p>', unsafe_allow_html=True)
        #st.markdown(f'<p style="font-size: 20px; color: red;"></code>{b}</code></p>', unsafe_allow_html=True)

    def txt3(a, b):
        col1, col2 = st.columns([1,4])
        with col1:
            st.markdown(f'<p style="font-size: 18px;">{a}</p>', unsafe_allow_html=True)
        with col2:
            b_no_commas = b.replace(',', '')
            st.markdown(b_no_commas)

    def txt4(a, b):
        col1, col2 = st.columns([1.5,2])
        with col1:
            st.markdown(f'<p style="font-size: 25px; color: white;">{a}</p>', unsafe_allow_html=True)
        with col2: #can't seem to change color besides green
            st.markdown(f'<p style="font-size: 25px; color: red;"><code>{b}</code></p>', unsafe_allow_html=True)
    
    st.logo(sidebar_logo, icon_image=sidebar_logo)
    #####################
# Sidebar: If using streamlit_option_menu
    with st.sidebar:
        with st.container():
            l, m, r = st.columns((1,3,1))
            with l:
                st.empty()
            with m:
                st.image(img_lh, width=175)
            with r:
                st.empty()
        
        choose = option_menu(
                            "Dev Kotak", 
                            ["About Me", "Site Overview", "Experience", "Skills", "Education", "Projects", "Volunteering", "Resume", "Contact"],
                            icons=['person fill','globe','clock history', 'tools', 'book half', 'clipboard', 'heart', 'paperclip', 'envelope'],
                            menu_icon="mortarboard", 
                            default_index=0,
                            styles={
            "container": {"padding": "0!important", "background-color": "#181818"},
            "icon": {"color": "white", "font-size": "16px"}, 
            "nav-link": {"font-size": "17px", "text-align": "left", "margin":"0px", "--hover-color": "#192538"},
            "nav-link-selected": {"background-color": "#192538"},
        }
        )
        components.html(LINKEDIN_PROFILE,height=400,width=900)
        components.html(GITHUB_PROFILE)
        
        linkedin_url = "https://www.linkedin.com/in/dev-kotak/"
        github_url = "https://github.com/dev856"
        email_url = "mailto:devhkotak@gmail.com"
        codechef_url = "https://www.codechef.com/users/god_001"
        with st.container():
            l, m, r = st.columns((0.11,2,0.1))
            with l:
                st.empty()
            with m:
                st.markdown(
                    social_icons(30, 30, LinkedIn=linkedin_url, GitHub=github_url, Email=email_url, Codechef=codechef_url)
                    ,unsafe_allow_html=True)
            with r:
                st.empty()

    st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
    st.title("Dev Kotak")
    # Create header
    if choose == "About Me":
        #aboutme.createPage()
        with st.container():
            left_column, middle_column, right_column = st.columns((2,0.1,1))
            with left_column:
                st.header("🙋 :blue[About Me]",divider='rainbow')
                st.subheader("Aspiring Software Engineer")
                st.info("👋🏻 Hi, I'm Dev! I'm a student of Master of Engineering: Electrical and Computer Engineering with a collaborative specialization in Data Science at Carleton University. Having prior relevant experiences in tech, I am constantly seeking unique internships to broaden my horizons before embarking on my career upon graduation.")
                st.info("💼 With the COVID-19 pandemic behind us, I believe there is potential for data science to be applied in the retail industry. In response to the increasing demand for data analytics from online, I am thus aiming to enter this industry for my first full-time job.")
                st.info("🏋🏻 In addition, I like to run, write, watch movies and... enjoy eating good food in my free time!")
                st.info("👨🏼‍💻 Academic interests: Data Visualization, Deep Learning, Recommendation Systems, Natural Language Processing")
                st.info("💭 Ideal Career Prospects: Data Analyst, Data Scientist, Data Engineer , Machine Learning Engineer, Software Engineer")
            with right_column:
                #st_lottie(lottie_coding, height=500, key="coding")
                components.html(
                """
                <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
                <dotlottie-player src="https://assets6.lottiefiles.com/packages/lf20_w51pcehl.json" background="transparent" speed="1" style="width: 350px; height: 500px" direction="1" mode="normal" loop autoplay></dotlottie-player>
                """,
                height=500,
                ) 
            
    elif choose == "Site Overview":   
        #overview.createPage()
        st.header("🌐 Site Overview",divider='rainbow')
        
        with st.container():
                left_column, middle_column, right_column = st.columns((2,0.1,1))
                with left_column:
                    st.markdown("""
                                - Originally, I started working this website as a portfolio, essentially an extended resume. The distinctive qualities of Streamlit compared to traditional front-end frameworks is that it it primarily used for creating web application dashboards, its extensive features make it more visually appealing to explore than alternatives such as Plotly and Shiny.
                                """)
                with right_column:
                    components.html(
                    """
                    <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
                    <dotlottie-player src="https://lottie.host/6f966033-0640-4492-aba8-e069b551b6f4/LtF2FH3ttk.json" background="transparent" speed="1" style="width: 350px; height: 500px" direction="1" mode="normal" loop autoplay></dotlottie-player>
                    """,
                    height=500,
                    )
# Create section for Work Experience
    elif choose == "Experience":
        #st.write("---")
        st.header("🔰 Experience",divider='rainbow')
        with st.container():
            image_column, text_column = st.columns((1,5))
            with image_column:
                st.image(img_bitmetrix,output_format="auto",width=250)
            with text_column:
                st.subheader("Research Intern, [Space Application Center, ISRO](https://www.isro.gov.in/)")
                st.write("*December 2022 to May 2023*")
                st.markdown("""
                - Worked on Machine learning techniques to estimate hydrological flues over different river basins of India.
                - Performed Analysis on Indian river basins dataset.
                - Analysis of Rainfall, Evapotranspiration, Groundwater Recharge helped to manage water resources across rivers.
                - Technical Skills: `Python` `Google Earth Engine` `JavaScript` `Google Colab, Git`.
                - Soft Skills: `Presentation` `problem solving` `Time management` `Communication skills`.
                
                """)
        st.divider()        
        with st.container():
            image_column, text_column = st.columns((1,5))
            with image_column:
                st.image(img_scor, output_format="auto",width=250)
            with text_column:
                st.subheader("Machine Learning Intern, [Jupiter AI Labs Pvt. Ltd.](https://juppiterailabs.com/)")
                st.write("*Dec 2022 to Feb 2023* | [*Certificate*](https://drive.google.com/file/d/1VYHlbY-K7cDr96Mv-6pRR6ev3idHyPeA/view?usp=sharing)")
                st.markdown("""
                - Created End to End Machine Learning solutions for Knowledge hut Client.
                - Worked on integration of ChatGpt and Chrome extensions.
                - Worked on AI Prompt Engineering project.
                - Technical Skills: `Python` `OpenAI` `TensorFlow` `Scikit-learn` `Git`
                - Soft Skills: `Innovation` `Detail oriented` `Decision-making` `Prioritization`

                """)
        st.divider()
        with st.container():
            image_column, text_column = st.columns((1,5))
            with image_column:
                st.image(img_zummit, output_format="auto",width=250)
            with text_column:
                st.subheader("Data Science Intern, [Zummit Infolabs Pvt. Ltd.](https://zummitlabs.com/)")
                st.write("*June 2022 to Sept 2022*")
                st.markdown("""
                - Completed learning path containing python programming concepts.
                - Facial Features Detection using Dlib.
                - Worked on Emotion detection classifier model for Kaggle FER Dataset.
                - Performed Object Detection using YOLO.
                - Technical Skills: `Python` `NumPy` `Matplotlib` `Pandas` `TensorFlow` `Scikit-learn` `Git`
                - Soft Skills: `Teamwork` `Presentation skills` `Decision-making` `Dedication`
                """)
        st.divider()
        with st.container():
            image_column, text_column = st.columns((1,5))
            with image_column:
                st.image(img_dep, output_format="auto",width=250)
            with text_column:
                st.subheader("Machine Learning Intern, [Devang Patel Institute of Advance Technology and Research(CHARUSAT)](https://charusat.ac.in/)")
                st.write("*May 2022 to June 2022* | [*Certificate*]()")
                st.markdown("""
                - Produced a lightweight solution for Yoga Pose estimation which predicts the yoga asanas using MediaPipe.
                - Classified Yoga poses using angle heuristic approach by detecting human poses and also worked on Research paper.
                - Worked on Deep Learning based solution for classification of Yoga asanas for the best results.
                - Technical Skills: `Python` `NumPy` `MediaPipe` `Pose Detection` `Pose Estimation` `OpenCV` `Git`
                - Soft Skills: `Research skills` `Time Management` `Writing Skills` `punctuality`
                """)
        st.divider()
        with st.container():
            image_column, text_column = st.columns((1,5))
            with image_column:
                st.image(img_kintu, output_format="auto",width=250)
            with text_column:
                st.subheader("NodeJS and Botpress.io Intern, [Kintu Designs Pvt. Ltd.](https://kintudesigns.com/public/)")
                st.write("*June 2021 to September 2021*")
                st.markdown("""
                - Completed Node.JS course as a learning path for internship.
                - Worked on ChatBot using Botpress for Zipply - delivery Application.
                - Configured google maps API and other live tasks during the internship.
                - Technical Skills: `Botpress.io` `Node.js` `Express.Js` `MySql`
                - Soft Skills: `Cooperation` `Communication` `Problem Solving` `Logical Thinking`
                
                """)
        st.divider()
        with st.container():
            image_column, text_column = st.columns((1,5))
            with image_column:
                st.image(img_spark, output_format="auto",width=250)
            with text_column:
                st.subheader("Data Science and Business Analytics Intern, [The Sparks Foundation](https://www.thesparksfoundationsingapore.org/)")
                st.write("*Jan 2021 to Feb 2021* | [*Testimonial*](https://drive.google.com/file/d/1O6Yu0P65dU8LCSDuXkf9BvlQJoz_5mRW/view?usp=sharing)")
                st.markdown("""
                - Predicted the study hours of students using Supervised Machine Learning algorithms.
                - Worked on Iris dataset and predicted the optimum number of clusters and represented it visually.
                - Used supervised and Unsupervised Machine learning algorithms for prediction tasks
                - Technical Skills: `Python` `Machine Learning`
                - Soft Skills: `Adaptability` `Work ethic` `Honesty`
                
                """)
        st.markdown('''
        <style>
        [data-testid="stMarkdownContainer"] ul{
            padding-left:0px;
        }
        </style>
        ''', unsafe_allow_html=True)
    # Subtitle

    elif choose == "Skills":
    #st.write("---")
        st.header(" ⚒️ Skills",divider='rainbow')
        with st.container():
                left_column, middle_column, right_column = st.columns((2,0.1,1))
                with left_column:
                    txt3("Programming Languages","`C/C++`, `Python`, `SQL`, `Java`, `MATLAB`")
                    txt3("Academic Interests","`Data Visualization`, `Recommendation Systems`, `Natural Language Processing`")
                    txt3("Data Visualization", "`matplotlib`, `seaborn`, `Plotly`, `Folium`, `GIS`, `Google Data Studio`")
                    txt3("Database Systems", "`MySQL`, `SQLite`, `NoSQL`")
                    txt3("Cloud Platforms", "`Google Cloud Platform`, `Streamlit Cloud`, `Hugging Face`")
                    txt3("Natural Language Processing", "`NLTK`, `Word2Vec`, `TF-IDF`, `TextStat`")
                    txt3("Version Control", "`Git`")
                    txt3("Design and Front-end Development", "`Canva`, `HTML`, `CSS`, `Streamlit`, `Wordpress`")
                    txt3("Data Science Techniques", "`Regression`, `Clustering`, `Random Forest`, `Decison Trees`, `Text Classification`, `Sentiment Analysis`, `Matrix Factorisation`")
                    txt3("Machine Learning Frameworks", "`Numpy`, `Pandas`, `Scikit-Learn`, `TensorFlow`, `Keras`")
                    txt3("Task Management Tools", "`Notion`, `ClickUp`, `Slack`, `Jira`")
                    txt3("Miscellaneous", "`Microsoft Office`, `Libre Officce`")
                with right_column:
                    components.html(
                    """
                    <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
                    <dotlottie-player src="https://assets6.lottiefiles.com/packages/lf20_2znxgjyt.json" background="transparent" speed="1" style="width: 350px; height: 500px" direction="1" mode="normal" loop autoplay></dotlottie-player>
                    """,
                    height=500,
                    )
       

# Create section for Education
#st.write("---")
    elif choose == "Education":
        st.header("🏛 Education",divider='rainbow')
        selected_options = ["Summary", "Modules"]
        selected = st.selectbox("Which section would you like to read?", options = selected_options)
        st.write("Current selection:", selected)
        if selected == "Summary":
            st.subheader("Summary")
            st.write("*Summary of education from primary school till university*")
            with st.container():
                image_column, text_column = st.columns((1,2.5))
                with image_column:
                    st.image(img_carleton,output_format="auto",width=200)
                with text_column:
                    st.subheader("Master of Engineering - [Electrical and Computer Engineering with collaborative specialization in Data Science], [Carleton University](https://carleton.ca/discover/) (2023-2025)")
                    st.write("Relevant Coursework: Pattern Classification and Experiment design , Applied Programming , Design Secure Network and Computer System, Interactive networked system and Telemedicine, Data Science Seminar, Cryptographic Implementations, Advanced Data Visualization")
                    st.markdown("""
                    - CGPA - 10.5/12.0
                    """)
            with st.container():
                image_column, text_column = st.columns((1,2.5))
                with image_column:
                    st.image(img_nus, output_format="auto",width=200)
                with text_column:
                    st.subheader("Bachelor of Technology - [Computer Science and Engineering], [Charotar University of Science and Technology ](https://www.charusat.ac.in/) (2019-2023)")
                    st.write("Relevant Coursework: Java Programming, Object-oriented Programming with C++, Programming in Python, Data Structure & Algorithms, Design & Analysis of algorithms, Machine learning, Artificial Intelligence, Software Engineering, Theory of Computation, Data Communication & Networking, Computer Networks, Modern Networks")
                    st.markdown("""
                    - CGPA - 9.25/10.00 | WES-ICAP-Eveluation- 3.92/4.00
                    - Recipient of Mukhyamantri Yuva Swavalamban Yojana Scholarship.- 2019-23
                    
                    """)
            with st.container():
                image_column, text_column = st.columns((1,2.5))
                with image_column:
                    st.image(img_poc, output_format="auto",width=200)
                with text_column:
                    st.subheader("Higher Secondary Education (Class- XI,XII) [Hiramohan Vidhyalaya](https://schools.org.in/surendranagar/24080503891/hira-mohan-vidhyalaya.html) (2017-2019)")
                    st.write("Coursework: Physics, Chemistry, Mathematics")
                    st.markdown("""
                    - Percentage - 82% Grade - A2
                    """)
            with st.container():
                image_column, text_column = st.columns((1,2.5))
                with image_column:
                    st.image(img_tpjc, output_format="auto", width=200)
                with text_column:
                    st.subheader("Secondary Education (Class- X) [Ultravision Academy](http://www.ultravisionschool.com/) (2016 - 2017)")
                    st.write("Coursework: ")
                    st.markdown(""" 
                    - 2
                    """)
            
        elif selected == "Modules":
            st.subheader("Modules")
            st.write("*List of courses taken at Carleton University*")
            with st.container():
                sem1, mid, sem2 = st.columns((1,0.1,1))
                with sem1:
                    st.write("**Academic Year 2023-2024**")
                    st.markdown("""
                    |Code|Module Title                       |Credit|
                    |--------|--------------------------------------|---------|
                    |ITEC 5010| Applied Programming|0.5|
                    |SYSC 5405| Pattern Classification and Experiment Design|0.5|
                    |SYSC 5500| Designing Secure Networking and Computer System|0.5|
                    |DATA 5000| Data Science Seminar|0.5|
                    |SYSC 5303| Interactive Networked Systems and Telemedicines|0.5|
                    |SYSC 5807| Cryptography Implementation|0.5|
                    """)
                    st.write("")
                    st.markdown("""
                    Total Workload : **6 Credits (Credit)**
                    """)
            st.write("*List of courses taken at Charotar University of Science and Technology*")
            with st.container():
                sem1, mid, sem2 = st.columns((1,0.1,1))
                with sem1:
                    st.write("**Academic Year 2019/20 Semester 1**")
                    st.markdown("""
                    |Code|Module Title                       |Credit|
                    |--------|--------------------------------------|---------|
                    |CE143| Computer Concepts and Programming       |5|
                    |CL142.01| Environmental Sciences              |2|
                    |EE145| Basics of Electronics and Electrical Engineering  |4|
                    |HS105.01 A| Liberal Arts - Media and Graphic Design          |2|
                    |IT144| ICT workshop         |1|
                    |MA143| Engineering Mathematics- I |4|
                    """)
                    st.write("")
                    st.markdown("""
                    Total Workload for Semester: **18 Modular Credits (Credit)**
                    """)
                with mid:
                    st.empty()
                with sem2:
                    st.write("**Academic Year 2020/21 Semester 2**")
                    st.markdown("""
                    |Code|Module Title                       |Credits|
                    |--------|--------------------------------------|---------|
                    |CE144|Object Oriented Programming with C++|5|
                    |HS126.01A|Communication Skills - I|2|
                    |MA144|Engineering Mathematics - II|4|
                    |ME145|Elements of Engineering |4|
                    |PY141.01|Engineering Physics|4|
                    """)
                    st.write("")
                    st.markdown("""
                    Total Workload for Semester: **19 Modular Credits (MCs)**
                    """)
            with st.container():
                sem1, mid, sem2 = st.columns((1,0.1,1))
                with sem1:
                    st.write("**Academic Year 2020/21 Semester 3**")
                    st.markdown("""
                    |Code|Module Title                       |Workload|
                    |--------|--------------------------------------|---------|
                    |CE244|Software Group Project - I|2|
                    |CE251|Java Programming|5|
                    |CE252|Digital Electronics|4|
                    |CE257|Data Communications and Networking|5|
                    |EC281.01|Introduction to Matlab Programming|2|
                    |HS121.02A|Creativity, Problem Solving and Innovation|2|
                    |MA253|Discrete Mathematics and Algebra|4|
                    """)
                    st.write("")
                    st.markdown("""
                    Total Workload for Semester: **24 Modular Credits (MCs)**
                    """)
                with mid:
                    st.empty()
                with sem2:
                    st.write("**Academic Year 2020/21 Semester4**")
                    st.markdown("""
                    |Code|Module Title                       |Workload|
                    |--------|--------------------------------------|---------|
                    |CS245|Data Structures and Algorithms|4|
                    |CE246|DataBase Management System|6|
                    |CE255|Software Group Project- II|2|
                    |CE258|Microprocessor and Computer Organization|5|
                    |CE259|Programming in Python|1|
                    |EC282.01|Prototyping Electronics with Arduino|2|
                    |HS111.02A|Human Values and Professional Ethics|2|
                    """)
                    st.write("")
                    st.markdown("""
                    Total Workload for Semester: **4 Modular Credits (MCs)**
                    """)
            with st.container():
                sem1, mid, sem2 = st.columns((1,0.1,1))
                with sem1:
                    st.write("**Academic Year 2021/22 Semester5**")
                    st.markdown("""
                    |Code|Module Title                       |Workload|
                    |--------|--------------------------------------|---------|
                    |CS341|Artificial Intelligence|4|
                    |CS343|Summer Internship I|3|
                    |CS348|Software Group Project - III|1|
                    |CS350|Operating System|4|
                    |CS351|Design and analysis of Algorithm|4|
                    |CS352|Computer Networks|4|
                    |CS377|Mobile Application Development|4|
                    |HS131.02A|Communication and Soft Skills|2|
                    """)
                    st.write("")
                    st.markdown("""
                    Total Workload for Semester: **23 Modular Credits (MCs)**
                    """)
                with mid:
                    st.empty()
                with sem2:
                    st.write("**Academic Year 2021/22 Semester 6**")
                    st.markdown("""
                    |Code|Module Title                       |Workload|
                    |--------|--------------------------------------|---------|
                    |CS344|Machine Learning|4|
                    |CS345|Cryptography and Network Security|5|
                    |CS346|Software Engineering|4|
                    |CS353|Theory of Computation|3|
                    |CS357|Software Group Project-IV|1|
                    |CS374|Modern Networks|4|
                    |HS132.02A|Contributing Personality Development|2|
                    """)
                    st.write("")
                    st.markdown("""
                    Total Workload for Semester: **23 Modular Credits (MCs)**
                    """)
            with st.container():
                sem1, mid, sem2 = st.columns((1,0.1,1))
                with sem1:
                    st.write("**Academic Year 2022/23 Semester 7**")
                    st.markdown("""
                    |Code|Module Title                       |Workload|
                    |--------|--------------------------------------|---------|
                    |CS442|Data Science and Analytics|5|
                    |CS446|Summer Internship-II|3|
                    |CS449|Internet of Things|4|
                    |CS450|Design of Langugage Processor|4|
                    |CS451|Advanced Computing|4|
                    |CS452|Software Group Project-V|1|
                    |CS474|Image Processing and Computer Vision|5|
                    """)
                    st.write("")
                    st.markdown("""
                    Total Workload for Semester: **22 Modular Credits (MCs)**
                    """)
                with mid:
                    st.empty()
                with sem2:
                    st.write("**Academic Year 2022/23 Semester 8**")
                    st.markdown("""
                    |Code|Module Title                       |Workload|
                    |--------|--------------------------------------|---------|
                    |CS453|Software Project Major|18|
                    """)
                    st.write("")
                    st.markdown("""
                    Total Workload for Semester: **18 Modular Credits (MCs)**
                    """)
    elif choose == "Projects":
        # Create section for Projects
        #st.write("---")
        st.header("📁 Projects",divider='rainbow')
        with st.container():
            text_column, image_column = st.columns((3,1))
            with text_column:
                st.subheader("Digital Trainer for Yoga Pose Estimation")
                st.write("*Python, NumPy, MediaPipe, Matplotlib, Pandas, OpenCV, VS Code*")
                st.markdown("""
                - Developed a solution for detecting and predicting yoga asana by analysing various methodologies for pose detection and estimation. 
                - Studied different topologies for better results.
                - Used MediaPipe lightweight library for landmark detection which accurately identifies more keypoints as compared to existing solutions.
                """)
                mention(label="Github Repo", icon="github", url="https://github.com/dev856",)
            # with image_column:
            #     st.image(images_projects[0])
        with st.container():
            text_column, image_column = st.columns((3,1))
            with text_column:
                st.subheader("Multi-label Dataset Prediction")
                st.write("*Carleton University SYSC 5405*")
                st.markdown("""
                - Processed 6 feature files with 25k rows and 786-1024 columns each, addressing randomness at the start of the competition. Implemented Randomforest for feature selection and ensured data quality by checking standards like null values and outliers.
                - Employed Logistic Regression using Multioutput classifier techniques. Incorporated meta-learning by leveraging these three base models and applied  bagging and boosting as the meta-learning algorithm.
                - Achieved a remarkable 75% accuracy on a blind dataset, securing position under top 5 team in the competition. The strategic combination of preprocessing, diverse models, and meta-learning contributed to the winning solution.
                
                """)
                # st.write("[Github Repo](https://github.com/harrychangjr/sales-prediction)")
                #mention(label="Streamlit App", icon="streamlit", url="https://huggingface.co/spaces/harrychangjr/tiktok_analytics",)
                mention(label="Github Repo", icon="github", url="https://github.com/dev856",)
            # with image_column:
            #     st.image(images_projects[1])
        with st.container():
            text_column, image_column = st.columns((3,1))
            with text_column:
                st.subheader("Tone Topic: Topic Modeling and Labeling in the Streamlit Sea ")
                st.write("* Carleton University - Applied Programming ITEC5010*")
                st.markdown("""
                - This project represents the merging of artificial intelligence and user-centric design to ease the gathering of insights from diverse data sources. 
                - This project presents a tool that uses the LDA(Latent Dirichlet Allocation) algorithm for effective topic modeling and tagging, applied to textual data and CSV files received. 
                - Along with Streamlit's engaging interface and the Heapq algorithm for detailed topic categorization, this app stands as an important tool for market research and data analysis. 
                - It is aimed at inspiring analysts and researchers to help users build a flexible and insightful data analysis tool.
                """)
                # st.write("[Github Repo](https://github.com/harrychangjr/sales-prediction)")
                mention(label="Github Repo", icon="github", url="https://github.com/dev856",)
            # with image_column:
            #     st.image(images_projects[1])
    elif choose == "Volunteering":
        st.header("🫴 Volunteering",divider='rainbow')
        with st.container():
            text_column, mid, image_column = st.columns((3,0.4,1))
            with text_column:
                st.subheader("Google Crowdsource")
                st.write("*Jan 2020 to Present*")
                st.markdown("""
            
                - Level 13 Contributor
                """)
            with mid:
                st.empty()
            with image_column:
                st.image(images_vol[0], output_format="auto", width=200)
        with st.container():
            text_column, mid, image_column = st.columns((3,0.4,1))
            with text_column:
                st.subheader("Computer Society of India")
                st.write("*Jan 2020 to Feb 2020*")
                st.markdown("""
                - Event Coordinator 
                - Contributed as Event Volunteer in CSI Regional Student Convention (RSC 2020) organized by CSI Student Branch of CSPIT and DEPSTAR in association with Computer Society of India (CSI).2
                """)
            with mid:
                st.empty()
            with image_column:
                st.image(images_vol[1], output_format="auto", width=200)
        with st.container():
            text_column, mid, image_column = st.columns((3,0.4,1))
            with text_column:
                st.subheader("Coding Ninjas")
                st.write("*Nov 2019 to Apr 2020*")
                st.markdown("""
                Campus Ambassador
                - My responsibility was to spread awarness about various services provided by Coding Ninjas to the student community . Developed campus-specific outreach programs and campaigns.
                """)
            with mid:
                st.empty()
            with image_column:
                st.image(images_vol[2], output_format="auto", width=200)
        with st.container():
            text_column, mid, image_column = st.columns((3,0.4,1))
            with text_column:
                st.subheader("Codechef CHARUSAT Chapter")
                st.write("*September 2022 to October 2022*")
                st.markdown("""
                Event Coordinator 

                - Served as a member of the organizing committee in codepie 2.0 competitive programming contest organized by faculty of technology & engineering in association with codechef.
                """)
            with mid:
                st.empty()
            with image_column:
                st.image(images_vol[3], output_format="auto", width=200)
    elif choose == "Resume":   
        resume_url = "https://drive.google.com/file/d/1UnSVLegQIbSE_GQ-K-DzA1JQQtHb4aNx/view?usp=sharing"
        st.header("📄 Resume",divider='rainbow')
        st.write("*In case your current browser cannot display the PDF documents, do refer to the hyperlink below!*")
        #google_viewer_url = f"https://drive.google.com/file/d/1UnSVLegQIbSE_GQ-K-DzA1JQQtHb4aNx/view?usp=sharing"

        #st.markdown(f'<iframe src="{google_viewer_url}" width="100%" height="800px"></iframe>', unsafe_allow_html=True)
        #st.markdown(f"[Open Resume in Google Drive Viewer]({resume_url})", unsafe_allow_html=True)
        st.markdown(pdf_link(resume_url, "**Resume**"), unsafe_allow_html=True)
        show_pdf("Resume-Dev.pdf")
        with open("Resume-Dev.pdf", "rb") as file:
            PDFbyte = file.read()
        st.download_button(
            label="Download Resume (1 page)",
            data=PDFbyte,
            file_name="Resume-Dev.pdf",
            mime="application/pdf"
        )
    elif choose == "Contact":
    # Create section for Contact
        #st.write("---")
        st.header("Contact",divider='rainbow')
        def social_icons(width=24, height=24, **kwargs):
            icon_template = '''
            <a href="{url}" target="_blank" style="margin-right: 10px;">
                <img src="{icon_src}" alt="{alt_text}" width="{width}" height="{height}">
            </a>
            '''

            icons_html = ""
            for name, url in kwargs.items():
                icon_src = {
                    "linkedin": "https://cdn-icons-png.flaticon.com/512/174/174857.png",
                    "github": "https://cdn-icons-png.flaticon.com/512/25/25231.png",
                    "email": "https://cdn-icons-png.flaticon.com/512/561/561127.png"
                }.get(name.lower())

                if icon_src:
                    icons_html += icon_template.format(url=url, icon_src=icon_src, alt_text=name.capitalize(), width=width, height=height)

            return icons_html
        with st.container():
            text_column, mid, image_column = st.columns((1,0.2,0.5))
            with text_column:
                st.write("Let's connect! You may either reach out to me at devhkotak@gmail.com or use the form below!")
                # with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
                #     st.write('Please help us improve!')
                #     Name=st.text_input(label='Your Name',
                #                         max_chars=100, type="default") #Collect user feedback
                #     Email=st.text_input(label='Your Email', 
                #                         max_chars=100,type="default") #Collect user feedback
                #     Message=st.text_input(label='Your Message',
                #                             max_chars=500, type="default") #Collect user feedback
                #     submitted = st.form_submit_button('Submit')
                #     if submitted:
                #         st.write('Thanks for your contacting us. We will respond to your questions or inquiries as soon as possible!')
                def create_database_and_table():
                    conn = sqlite3.connect('contact_form.db')
                    c = conn.cursor()
                    c.execute('''CREATE TABLE IF NOT EXISTS contacts
                                (name TEXT, email TEXT, message TEXT)''')
                    conn.commit()
                    conn.close()
                create_database_and_table()

                st.subheader("Contact Form")
                if "name" not in st.session_state:
                    st.session_state["name"] = ""
                if "email" not in st.session_state:
                    st.session_state["email"] = ""
                if "message" not in st.session_state:
                    st.session_state["message"] = ""
                st.session_state["name"] = st.text_input("Name", st.session_state["name"])
                st.session_state["email"] = st.text_input("Email", st.session_state["email"])
                st.session_state["message"] = st.text_area("Message", st.session_state["message"])


                column1, column2= st.columns([1,5])
                if column1.button("Submit"):
                    conn = sqlite3.connect('contact_form.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)",
                            (st.session_state["name"], st.session_state["email"], st.session_state["message"]))
                    conn.commit()
                    conn.close()
                    st.success("Your message has been sent!")
                    # Clear the input fields
                    st.session_state["name"] = ""
                    st.session_state["email"] = ""
                    st.session_state["message"] = ""
                def fetch_all_contacts():
                    conn = sqlite3.connect('contact_form.db')
                    c = conn.cursor()
                    c.execute("SELECT * FROM contacts")
                    rows = c.fetchall()
                    conn.close()
                    return rows
                
                if "show_contacts" not in st.session_state:
                    st.session_state["show_contacts"] = False
                if column2.button("View Submitted Forms"):
                    st.session_state["show_contacts"] = not st.session_state["show_contacts"]
                
                if st.session_state["show_contacts"]:
                    all_contacts = fetch_all_contacts()
                    if len(all_contacts) > 0:
                        table_header = "| Name | Email | Message |\n| --- | --- | --- |\n"
                        table_rows = "".join([f"| {contact[0]} | {contact[1]} | {contact[2]} |\n" for contact in all_contacts])
                        markdown_table = f"**All Contact Form Details:**\n\n{table_header}{table_rows}"
                        st.markdown(markdown_table)
                    else:
                        st.write("No contacts found.")


                st.write("Alternatively, feel free to check out my social accounts below!")
                linkedin_url = "https://www.linkedin.com/in/dev-kotak/"
                github_url = "https://github.com/dev856"
                email_url = "mailto:devhkotak@gmail.com"
                st.markdown(
                    social_icons(32, 32, LinkedIn=linkedin_url, GitHub=github_url, Email=email_url),
                    unsafe_allow_html=True)
                st.markdown("")
                
            with mid: 
                st.empty()
            with image_column:
                components.html(
                """
                <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
                <dotlottie-player src="https://assets9.lottiefiles.com/packages/lf20_osdxlbqq.json" background="transparent" speed="1" style="width: 350px; height: 500px" direction="1" mode="normal" loop autoplay></dotlottie-player>
                """,
                height=500,
                )
                
    
    st.divider()

    st.write("##")
    
    st.write(f"""<div class="subtitle" style="text-align: center;">⬅️ Check out my other details in the  n menu!</div>""", unsafe_allow_html=True)


if __name__=="__main__":
    home()


