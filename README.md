<a name="readme-top"></a>



[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<br />
<div align="center">
  <img alt="Logo" width="170" height="70" src="./assets/logo.png"/>
  <h3 align="center">Fjob backend</h3>

  <p align="center">
    Fjob is a portal that will make your job search easier, it allows you to scrape job offers from various job portals (currently only in Poland) to easily have everything in one place. It also allows companies to post their own ads.
    <br />
    <br />
    <a href="https://github.com/DEENUU1/fjob_backend/issues">Report Bug</a>
    ·
    <a href="https://github.com/DEENUU1/fjob_backend/issues">Request Feature</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

Fjob is a constantly developing project, every day I try to expand the application with new functionalities and enable the collection of data from as many websites as possible so that you don't miss any offer.

### Backend - https://kwlodarczyk.pro/admin
### Frontend - https://main.d3cjvuwb5x6i3c.amplifyapp.com/

## Key Features
- Advanced user system - JWT Authentication and functions to confirm operations with email
- The main endpoint, which returns a list of job offers, uses pagination, advanced searches and filtering
- Possibility to buy ads thanks to the integration of the application with the stripe platform
- Possibility to add advertisements to favorites and report irregularities
- Advanced administrator panel that allows you to track annual, monthly and daily statistics for all models
- Possibility to create a company account to post your own job offers - in the future, the option will be extended to add moderators to a given company profile
- Using Django signals and creating your own permissions to ensure that the application works efficiently and safely


### Built With

- Python
  - Django 
  - Django Rest Framework
  - Pytest
  - Celery
- Redis
- Docker
- Docker-compose
- AWS EC2
- AWS S3
- AWS Route 53
- Google Cloud SQL (postgre)
- Certbot
- NGINX
- CI/CD 

<!-- GETTING STARTED -->
## Getting Started


### Installation (dev mode)

1. Clone git repository
```bash
git clone https://github.com/DEENUU1/fjob_backend.git
```

2. Create dotenv file and add required data
```bash
cp .env_example .env
```

3. Install all requirements
```bash
pip install -r requirements.txt
```

4. Change directory to metaspy to run commands
```bash
python manage.py runserver
```

### Tests

To run pytests use this command
```bash
pytest
```



<!-- LICENSE -->
## License

See `LICENSE.txt` for more information.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/DEENUU1/fjob_backend.svg?style=for-the-badge
[contributors-url]: https://github.com/DEENUU1/fjob_backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/DEENUU1/fjob_backend.svg?style=for-the-badge
[forks-url]: https://github.com/DEENUU1/fjob_backend/network/members
[stars-shield]: https://img.shields.io/github/stars/DEENUU1/fjob_backend.svg?style=for-the-badge
[stars-url]: https://github.com/DEENUU1/fjob_backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/DEENUU1/fjob_backend.svg?style=for-the-badge
[issues-url]: https://github.com/DEENUU1/fjob_backend/issues
[license-shield]: https://img.shields.io/github/license/DEENUU1/fjob_backend.svg?style=for-the-badge
[license-url]: https://github.com/DEENUU1/fjob_backend/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/kacper-wlodarczyk
[basic]: https://github.com/DEENUU1/fjob_backend/blob/main/assets/v1_2/basic.gif?raw=true
[full]: https://github.com/DEENUU1/fjob_backend/blob/main/assets/v1_2/full.gif?raw=true
[search]: https://github.com/DEENUU1/fjob_backend/blob/main/assets/v1_2/search.gif?raw=true
