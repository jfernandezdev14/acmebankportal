# AcmeBankPortal
Service containing all functionalities of ACME bank

## DOCKER - PYTHON/FLASK/MONGODB API
Dev Environment - Python Flask App API with MongoDB using Docker.


## Required Software
Docker Engine is available on a variety of Linux platforms, macOS and Windows 10 through Docker Desktop, and as a static binary installation. Find your preferred operating system below.
https://docs.docker.com/engine/install/

## Dependencies
This repository depends on the following one:
- https://github.com/juanse-14/financialservice
- https://github.com/juanse-14/userservice


## How to install
   
   ## 1 - Create a project directory:
     mkdir playvox_test
     cd playvox_test

   ## 2 - Clone repo:
     git clone https://github.com/juanse-14/acmebankportal.git
     git clone https://github.com/juanse-14/financialservice.git
     git clone https://github.com/juanse-14/userservice.git

   ## 3 - Start and debug:
   In different terminals execute inside each repo (acmebankportal, financialservice, userservice) the following commands:

     docker-compose up -d

   ## 4 - Test endpoints via postman (Optional):
   If you want to test the endpoints of financialservice or userservice repos you can load the following postman collection links
   
   - FinancialService postman collection: https://www.getpostman.com/collections/fa7bb4dbe2d2c61961d7
   - UserService postman collection: https://www.getpostman.com/collections/2f7339a01e1f4bb62cb4

   In case you don't have postman here is the link to download and install its client: https://www.postman.com/downloads/ 

## Test the application
After deploy, you can use the following url to test the app - http://localhost:8000/
