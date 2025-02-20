# CSC 6350 Software Engineering Project

## Course Info
- **Course:** CSC 6350 Software Engineering
- **Semester:** Spring 2025
- **Professor:** Dr. David James


## Group Member Names
- Kidus Tafa
- Naimul Islam
- Donggeun Yoo
- Cecilia Muniz Siqueira
- Jahin Al Hasan Joy

## Project Info
- **Title:** SPOT: Showcase, Post, Obtain Feedback, and Thrive 
- **Description:** This website is a platform designed to help students showcase their academic projects, receive ratings from peers and faculty, and gather constructive feedback to improve their work and thrive.

🚀 Features

1. Project Presentation & Management

Upload and organize academic presentations (PDF, PPT, embedded videos) for easy access.

Categorize projects based on topics, disciplines, or university courses.

2. Feedback & Rating System

Reviewers (students and professors) provide feedback through:

Comments for detailed discussions.

Emoji reactions for quick engagement.

Numerical ratings on clarity, research depth, and presentation quality.

A leaderboard highlights the top-rated projects to inspire motivation.

3. User Interaction & Collaboration

User profiles display academic backgrounds and uploaded projects.

Search and filter projects by topic, rating, or author.

Facilitates networking between students and faculty members.

🛠 Tech Stack

Backend: Django (Python)
Frontend: Vue.js
Database: MYSQL

## Use Case Diagram
![Use_Case_Diagram](Use_Case_Diagram.png)

## ER Diagram
![ERD](ERD.png)

## Functional Requirements


## Non-Functional Requirements

- **Performance:**
  - The website should load within 3 seconds for most pages to ensure smooth user experience.
  - The system should handle a large number of concurrent users without significant performance degradation, especially during peak times such as project submissions or feedback periods.
- **Security:**
  - User data, especially sensitive information such as login credentials, should be encrypted and stored securely.
  - The system should comply with privacy regulations (e.g., GDPR, FERPA) for handling personal data.
  - The platform should implement strong authentication methods, including multi-factor authentication (MFA) for sensitive user actions.
- **Scalability:**
  - The website should be designed to scale easily, handling increased traffic and a growing number of users and projects as the platform expands.
- **Reliability:**
  - The system should have a 99% uptime guarantee, ensuring that it is accessible to users at all times.
  - There should be automated backups to prevent data loss in case of failure.
- **Usability:**
  - The platform should be intuitive and user-friendly, requiring minimal training for users to upload, search for, and review projects.
  - The website should be mobile-responsive, ensuring a consistent experience on various devices (desktop, tablet, mobile).
- **Compliance:**
  - The platform should adhere to any relevant accessibility standards (e.g., WCAG) to ensure that students with disabilities can use the system effectively.
  - The platform should comply with any institutional or academic standards for academic project submissions and feedback collection.
- **Compatibility:**
  - The system should be compatible with modern web browsers (e.g., Chrome, Firefox, Safari, Edge).
  - The system should support file formats commonly used for project submission (e.g., PDFs, images, videos, .zip files for code).
- **Localization:**
  - The platform should be available in multiple languages if necessary, catering to international students or diverse user groups.
  - Date and time formats should be adaptable to different regions (e.g., time zone support).
- **Maintenance:**
  - The system should be easy to maintain and update with minimal downtime. Regular updates should be deployed for new features, bug fixes, and performance improvements.
- **Cost Efficiency:**
  - The system should be designed to minimize operational costs, particularly when scaling up to handle large numbers of users and projects.
