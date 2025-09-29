Assignment 2 - Cloud Services Exercises - Response to Criteria
================================================

Instructions
------------------------------------------------
- Keep this file named A2_response_to_criteria.md, do not change the name
- Upload this file along with your code in the root directory of your project
- Upload this file in the current Markdown format (.md extension)
- Do not delete or rearrange sections.  If you did not attempt a criterion, leave it blank
- Text inside [ ] like [eg. S3 ] are examples and should be removed


Overview
------------------------------------------------

- **Name:** YourName Damon Eccles
- **Student number:** n12197718
- **Partner name (if applicable):** YourPartner NameHere
- **Application name:** Whiteboard
- **Two line description:** This app is an online ms-paint that hopefully in the future more than one person can work on at once.
- **EC2 instance name or ID:** deccl4-assignment-whiteboard

------------------------------------------------

### Core - First data persistence service

- **AWS service name:**  s3
- **What data is being stored?:** .png
- **Why is this service suited to this data?:** Large amounts of photos can be stored here relatively cheap. Also has a good file structure.
- **Why is are the other services used not suitable for this data?:** This service is cheap and used for general storage. DynamoDB would have been invalid.
- **Bucket/instance/table name:** pictures-bucket-cab432-assignment
- **Video timestamp:** 3:56
- **Relevant files:**
    - app/export.py

### Core - Second data persistence service

- **AWS service name:**  DynamoDB
- **What data is being stored?:** .json strokes. (lines drawn by user)
- **Why is this service suited to this data?:This service is great for strings and .jsons (big string)
- **Why is are the other services used not suitable for this data?: It was important for the service to be a database due to the amount of entries of strings. It was also important to connect strings to the application depending on values like roomID
- **Bucket/instance/table name:** n12197718-whiteboard-strokes
- **Video timestamp:** 3:17
- **Relevant files:**
    - app/export.py
    - app/routes.py
    - /static/canvas.js

### Third data service

- **AWS service name:**  s3
- **What data is being stored?:** storing pdfs
- **Why is this service suited to this data?:** Stores a backup of the pdf generated. Could have large quanitities.
- **Why is are the other services used not suitable for this data?:** s3 is cheap, and has a really nice filing service that can by dynamically created and explored through.
- **Bucket/instance/table name:** pictures-bucket-cab432-assignment
- **Video timestamp:** 3:56
- **Relevant files:**
    - app/export.py

### S3 Pre-signed URLs

- **S3 Bucket names:**
- **Video timestamp:**
- **Relevant files:**
    -

### In-memory cache

- **ElastiCache instance name:**
- **What data is being cached?:** [eg. Thumbnails from YouTube videos obatined from external API]
- **Why is this data likely to be accessed frequently?:** [ eg. Thumbnails from popular YouTube videos are likely to be shown to multiple users ]
- **Video timestamp:**
- **Relevant files:**
    -

### Core - Statelessness

- **What data is stored within your application that is not stored in cloud data services?:** All data is pushed to either an s3 or cognito. Data stored in memory is not used after pushed into another service.
- **Why is this data not considered persistent state?:** If there is a problem with the server, data can be fetched and the process can continue. Kinda like a backup plan.
- **How does your application ensure data consistency if the app suddenly stops?:** All data is saved in real time when the data is created. If the data is created it can be accessed.
- **Relevant files:**
    - /app/export.py
    - /app/routes.py
    - /app/static/canvas.js
- timestap: 4:54

### Graceful handling of persistent connections

- **Type of persistent connection and use:** [eg. server-side-events for progress reporting]
- **Method for handling lost connections:** [eg. client responds to lost connection by reconnecting and indicating loss of connection to user until connection is re-established ]
- **Relevant files:**
    -


### Core - Authentication with Cognito

- **User pool name:** whiteboard-user-pool
- **How are authentication tokens handled by the client?:** JWT authentication allows us to validate users by their roles and therefore their permissions.
- **Video timestamp:** 0:0, 0:27, 0:50
- **Relevant files:**
    - /app/users.py
    - /app/routes.py
    - /app/static/home.js

### Cognito multi-factor authentication

- **What factors are used for authentication:** password, email
- **Video timestamp:** 0:38, 1:48
- **Relevant files:**
    - /app/users.py

### Cognito federated identities

- **Identity providers used:**
- **Video timestamp:**
- **Relevant files:**
    -

### Cognito groups

- **How are groups used to set permissions?:** Guests are the default non signedup user. They can draw and join rooms. Users can export drawings and admin has access to the admin control panel from a1.
- **Video timestamp:** 1:09
- **Relevant files:**
    - /app/static/home.js
    - /app/users.py

### Core - DNS with Route53

- **Subdomain**:  whiteboard.cab432.com
- **Video timestamp:** 2:34

### Parameter store

- **Parameter names:** roomID, token 
- **Video timestamp:** 2:34
- **Relevant files:**
    - canvas.js

### Secrets manager

- **Secrets names:** n12197718-whiteboard-assignment
- **Video timestamp:** 3:01
- **Relevant files:**
    - app/users.py

### Infrastructure as code

- **Technology used:** terraform
- **Services deployed:** s3, cognito
- **Video timestamp:** 4:30
- **Relevant files:**
    - terraform/main.tf

### Other (with prior approval only)

- **Description:**
- **Video timestamp:**
- **Relevant files:**
    -

### Other (with prior permission only)

- **Description:**
- **Video timestamp:**
- **Relevant files:**
