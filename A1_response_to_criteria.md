Assignment 1 - REST API Project - Response to Criteria
================================================

Overview
------------------------------------------------

- **Name:** Damon Eccles    
- **Student number:** n12197718
- **Application name:** Whiteboard
- **Two line description:** This project is about an online paint tool that allows you to download your pages into a pdf. It was important that the user can have multiple pages they can switch between them.

I apologise for the video, OBS default settings (fresh download) had these as default and the microphone turned off. 


Core criteria
------------------------------------------------

### Containerise the app

- **ECR Repository name:** n12197718/whiteboard
- **Video timestamp:** 0:03 
- **Relevant files:**
    - Dockerfile
    - docker-compose.yml
    - requirements.txt

### Deploy the container

- **EC2 instance ID:** 901444280953
- **Video timestamp:** 0:16

### User login

- **One line description:** Admin and user can log in, each have different accessbilities. Admin has control on the stress button.
- **Video timestamp:** 0:33, 2:36
- **Relevant files:**
    - app/user.py
    - app/routes.py

### REST API

- **One line description: REST api was used for mainly switching between pages but also for exporting and error handling.
- **Video timestamp:** 3:03
- **Relevant files:**
    - routes.py

### Data types

- **One line description:** The data kept was used for drawing onto the screen and making the pages downloadable.
- **Video timestamp:** 
- **Relevant files:**
    - 

#### First kind

- **One line description:**  I had a json for each stroke a user commited, used to redraw and draw for export.
- **Type:** .json
- **Rationale:** Used to store important information such as colour size and the pen coordinates. This information is client side until exported.
- **Video timestamp:** 4:08
- **Relevant files:**
    - app/export.py
    - app/static/canvas.js

#### Second kind

- **One line description:** Pdf used to download to the user    
- **Type:** .pdf    
- **Rationale:** Compact way to give multiple pages to the user.
- **Video timestamp:** 4:08
- **Relevant files:**
  - app/export.py

### CPU intensive task

 **One line description:** Upscale points from the .json to 4k and save them to a .png  
- **Video timestamp:** 4:08
- **Relevant files:**
    - app/export.py

### CPU load testing

 **One line description:** Load 1000 pages that have the same .json (1000 might be unrealistic but 100 is definetly possible, therefore i think is a valid test)
- **Video timestamp:** 3:37 
- **Relevant files:**
    - 

Additional criteria
------------------------------------------------

### Extensive REST API features

- **One line description:** Not attempted
- **Video timestamp:**
- **Relevant files:**
    - 

### External API(s)

- **One line description:** Not attempted
- **Video timestamp:**
- **Relevant files:**
    - 

### Additional types of data

- **One line description:** Compile .pngs stored in an array to create .pdf 
- **Video timestamp:** 4:08
- **Relevant files:** 
    - app/export.py

### Custom processing

- **One line description:** redrawing to screen when switching between pages, and storing page data. 
- **Video timestamp:** 1:00 
- **Relevant files:**
    - app/static/canvas.js  

### Infrastructure as code

- **One line description:** docker-compose used to compile project. 
- **Video timestamp:** 0.03
- **Relevant files:**
    - docker-compose.yml

### Web client

- **One line description:** Not attempted
- **Video timestamp:**
- **Relevant files:**
    -   

### Upon request

- **One line description:** Front end features
- **Video timestamp:** 4:35
- **Relevant files:** 
    - adminLog.js   
    - userLog.js   
    - home.js
    - canvas.js 

