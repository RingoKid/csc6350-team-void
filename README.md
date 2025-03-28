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

## Instructions to run application

### Build the Docker image
`docker-compose build`

### Start the Docker containers
`docker-compose up`

### Start the Docker containers in detached mode
`docker-compose up -d`

## Instructions to run tests 
`docker-compose build`
`docker-compose up`
`docker ps`  ---> this is to get the <container_id> to use in the next step
`docker exec -it <container_id> python manage.py test`

