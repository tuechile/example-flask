1. Introduction
This project is my personal portfolio website, named "Pirenily", design to showcare various works of mine in the past few years. This includes personal, collaboraive, and commissioned pieces both in Vietnam and the U.S. The website integrates features like a dynamic image gallery, interactive lightbox, responsive design, and smooth navigation facilitated by a loader. In this document, I discuss the technical implementation of the project and the rationale behind key design decisions.

2. Styling:
I used BHN Cinema and Crimson Text for the main typography, which are available on Google Fonts. BHN Cinema is a highly stylized yet readable font, which is used for an impressionist style of logo. Crimson Text is a serif font that has good font weights, not to mention that it has the word Crimson in it.

I used the CSS Grid for layout and responsiveness of the album pages.

3. Project Structure
The website follows a modular architecture using Flask's templating system. Below is the directory structure:

pirenily/
│
├── app.py                  # Main Flask application
├── templates/              # HTML templates
│   ├── layout.html         # Base layout template
│   ├── personal.html       # Personal work page with lightbox
│   └── /sections of layouts/
├── static/                 # Static assets
│   ├── styles.css          # Custom CSS for the website
│   ├── favicon.ico         # Favicon
│   └── asset/              # Images and other static files
│       ├── images/
│       │   └── /sections of photos/
│       └── loader.gif      # Loading animation
├── README.md               # User documentation
└── DESIGN.md               # Design document

3. Design Decisions
As an artist, I have long wanted to create a website from scratch to represent the archive of my interests and previous works in the artistic industry. Since this is the first time I am exposed to Computer Science in a technical way, I really want to create a portfolio website that is more interactive but should not require database or further execution of data. Before the final project, I have already thought of building a website whose main page has a big search bar to navigate through every possible pages but I would not think this would be possible. Fortunately, I got hold of Flask which makes it significantly easier to make this possible.

a. Templating System
Why Flask Templates? Flask’s Jinja2 templating system was chosen to enable dynamic content injection while maintaining a consistent layout across the website. The layout.html template defines a common structure (header, navigation, footer) for content-specific pages, such as personal.html, extend layout.html, allowing for reusable and maintainable code.

How It Works: {% block title %} and {% block content %} allow specific pages to override sections of the base layout and dynamic insertion of navigation links, gallery content, and page titles ensures scalability.

b. Loader Implementation
A loader enhances user experience by providing visual feedback during page transitions, especially for image-heavy galleries. When I was waiting for the images to finish loading, I saw that this would make users less patient with using the website, so I decided to find a funny gif to run while the page is being loaded. Luckily, I remember the gif file I used for the first project for Scratch so this is quite convenient.

How It Works: The loader is a div with a GIF inside (loader-container) styled with z-index to ensure it stays above all content. JavaScript handles its visibility by showing the loader when internal links are clicked (showLoader()). After a delay of 400ms when the page is fully loaded (hideLoader())., the loader hides to ensure that it doesn't appear as glitching.

Design Challenges: Since the loader is used accross all pages, it is easier to implement in the layout's script. However, in the pages where there are galleries, the loader from interfering with the lightbox required excluding .lightbox links in the loader script.

c. Image Gallery with Lightbox
Lightbox provides a focused view of images without redirecting the user. This enhances interactivity and aesthetics.

How It Works: The lightbox is a dynamically created overlay (lightbox-overlay) with an <img> element for the clicked image and a close button (<span> with &times;) to exit the lightbox. With CSS, we can ensures the lightbox overlay appears above other content and fits the image within the viewport. For Javascript, we use Event listeners to handle opening, closing, and clicking outside the lightbox.

Design Challenges: The Javascaript's e.preventDefault() conflicted with a Javascript outside and kept redirect to the image instead of just showing above the gallery. We need to add event delegation for .lightbox links to handle dynamically loaded content.

d. Responsive Design
CSS Grid provides a powerful and flexible layout for the gallery. It adapts seamlessly to different screen sizes, ensuring responsiveness.

How It Works: grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); allows the gallery to dynamically adjust the number of columns based on screen width.

e. Media queries
To ensure an optimal experience on smaller devices, I added customized media queries for sizes where I think this might break. This includes custom box padding, changing the div element alignment, and dynamic photo sizing.

f. Processing integration
I wanted to showcase my artistic work in other projects that are at the intersection of art and technology. This one project uses Processing, which is rather hard to integrate with HTML. Instead, I converted it to p5.js language and was able to place it onto the website, with some limitations (no external libraries and limited fonts allowed).

g. Subtle color introduction
Even though the website is mostly in black and white, I wanted to add some color when it looks aesthetically appropriate. When I hover over certain texts or photos, they will gain a color or filter gradient.

4. Summary
My Pirenily website leverages Flask's templating system, CSS Grid, and JavaScript to deliver an interactive and visually appealing portfolio. I have tried my best to carefully consider the scalability, responsiveness, and user experience. In the future, I hope to even manage growing the website content better by learning how to integrate a CMS database into my artworks, especially for those in the similar album grid.