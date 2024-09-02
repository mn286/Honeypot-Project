# Honeypot-Project

This repository contains a Proof of Concept (PoC) for deploying a versatile web application honeypot using Docker. The honeypot is capable of emulating different web applications, such as Drupal and WordPress, to attract and analyze attacks from malicious actors.

## Table of Contents

- [Introduction](#introduction)
- [Honeypot Environment](#honeypot-environment)
  - [Docker Environment](#docker-environment)
  - [Honeypot Architecture](#honeypot-architecture)
    - [Scalability](#scalability)
    - [Ease of Deployment](#ease-of-deployment)
    - [Effectiveness in Luring Attackers](#effectiveness-in-luring-attackers)
  - [OWASP Honeypot](#owasp-honeypot)
    - [Honeytraps](#honeytraps)
  - [ModSecurity (ModSec)](#modsecurity-modsec)
- [Usage](#usage)
  - [Setting Up the Environment](#setting-up-the-environment)
  - [Switching Profiles](#switching-profiles)
  - [Accessing the Honeypot](#accessing-the-honeypot)
  
## Introduction

This project is designed to deploy and manage a web application honeypot that can switch between emulating Drupal and WordPress environments. The primary goal is to lure attackers and analyze their behaviors in a controlled environment.

## Honeypot Environment

### Docker Environment

The honeypot environment is containerized using Docker, allowing for easy deployment and management. Docker ensures that the environment is isolated and can be easily replicated across different systems.

### Honeypot Architecture

The honeypot architecture is designed to be scalable, easy to deploy, and effective in attracting attackers.

#### Scalability

The use of Docker allows for easy scaling of the honeypot environment. Multiple instances can be deployed across different systems or cloud environments to cover a broader range of attack surfaces.

#### Ease of Deployment

With Docker, the honeypot can be deployed with a single command, making it easy to set up and manage.

#### Effectiveness in Luring Attackers

The honeypot is designed to mimic real-world web applications closely, using various honeytraps and ModSecurity rules to detect and log malicious activities.

### OWASP Honeypot

This project leverages the OWASP Honeypot framework, which provides a robust foundation for setting up web application honeypots.

#### Honeytraps

The honeypot includes several custom honeytraps designed to attract attackers. These traps emulate typical vulnerabilities found in Drupal and WordPress, such as fake admin login pages, misconfigured files, and more.

### ModSecurity (ModSec)

ModSecurity is used to monitor and log all incoming requests. Custom ModSecurity rules are applied based on the selected profile (Drupal or WordPress) to simulate specific vulnerabilities.

## Usage

### Setting Up the Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/mn286/Honeypot-Project.git
   cd Honeypot-Project
2. Build the Docker Image
   ```bash
   docker-compose build
3. Start the Honeypot
    ```bash
   docker-compose up

### Switching Profiles

To switch between Drupal and WordPress profiles:

1. Run the profile switch script inside the container:
   ```bash
   docker exec -it <container_name> /usr/local/bin/switch_profile.sh <profile_name>
Replace <profile_name> with drupal or wordpress.

### Accessing the Honeypot

The honeypot can be accessed locally at http://localhost:8080. The environment will present the selected web application (Drupal or WordPress) to any incoming traffic.






