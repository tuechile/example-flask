pirenily: A personal archive
Welcome to Pirenily! This project is a personal portfolio and image gallery website built to showcase personal, collaborative, and commissioned works of mine. Below you will find detailed instructions on how to set up, configure, and use the project.

1. Features
- Lightbox functionality for viewing images in an interactive overlay.
- A loader animation for smooth navigation between pages.
- Responsive design optimized for various devices.
- Organized sections for personal, collaborative, and commissioned works.

2. Technologies Used
- Frontend: HTML, CSS, JavaScript
- Backend: Flask (Python)
Additional Tools:
- Google Fonts
- Koyeb

3. Requirements
To run this project, you will need:
- Python 3.8 or later
- Flask (pip install flask)
- A modern web browser (e.g., Chrome, Firefox)

4. Installation
- Locate the Provided Files: Ensure all the project files are available in a single folder on your computer.
- Set Up a Virtual Environment
- Install Dependencies:
With the virtual environment activated, install Flask using "pip install flask"
- Run the Flask Application
Start the server with: "flask run"
- Access the Website

5. Continuous Integration through Koyeb
To integrate this with my own pre-purchased domain, I used Koyeb, which is a Platform-as-a-Service platform that allows me to deploy and run Flask applications. Following the guide [here](https://github.com/koyeb/example-flask?tab=readme-ov-file), I set up an account with Koyeb (using their free tier), created a new web service, linked the web service to my personal GitHub repository (which now contained not only the front-end components, but also the Procfile and other installation requirements), and pointed my domain from Google Domains (now Squarespace) to the domain that Koyeb provided for my specific account. 

This means that I can just push new commits to my personal GitHub repository for my website, and Koyeb will take care of the deployment (if it works). You can access my website at [pirenily.com](pirenily.com)!

6. Usage
Home Page: Navigate the sections for personal, collaborative, and commissioned works.
Small layout: about (neccessary information and self-photography), personal, collaborative, and commissioned works
Lightbox Functionality: Click on any image thumbnail to view it in a lightbox overlay.
Loader Animation: Notice the smooth transition when navigating between pages.

7. File Structure
pirenily-website/
│
├── app.py                  # Main Flask application
├── templates/              # HTML templates
│   ├── layout.html         # Base template
│   └── index.html          # Homepage
├── static/
│   ├── styles.css          # Custom CSS styles
│   ├── favicon.ico         # Favicon for the website
│   └── asset/              # Images and other static assets
│       ├── images/
│       │
│       └── fonts           # Loader animation
├── README.md               # Project documentation
└── DESIGN.md               # Design document

8. Video Presentation
Watch the video walkthrough here: [Pirenily Website Presentation](https://youtu.be/CZ2iPyw1jsA)
