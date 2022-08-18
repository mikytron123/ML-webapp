<h2 align="center">ML-webapp</h2>

  <p align="center">
    Webapp for classifying whether income exceeds 50k/year based on Adult UCI dataset.
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[screen-capture.webm](https://user-images.githubusercontent.com/25290130/185510132-fcdc7035-d491-4888-a16f-583980b98f5c.webm)

This is a webapp created using C# Blazor for classifying whether income exceeds 50k/year. The backend uses a FastAPI endpoint for making predictions from a single row or batch predictions from a file. The Frontend runs client-side using Blazor WebAssembly. A SVC model is used for predictions.

### Built With

* [![Blazor][Blazor.net]][Blazor-url]
* [![Scikit-Learn][Scikit-learn.org]][Scikit-learn-url]
* [![FastAPI][FastAPI.com]][FastAPI-url]


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Install Docker for your OS

<!-- USAGE EXAMPLES -->
## Usage

1. ```docker-compose up --build api```

2. ```docker-compose up --build web```

3. Navigate to "localhost:8080" in your browser


[Blazor-url]: https://dotnet.microsoft.com/en-us/apps/aspnet/web-apps/blazor
[Blazor.net]: https://img.shields.io/badge/Blazor-0769AD?style=for-the-badge&logo=blazor&logoColor=512BD4
[Scikit-learn.org]: https://img.shields.io/badge/ScikitLearn-0769AD?style=for-the-badge&logo=scikit-learn&logoColor=F7931E
[Scikit-learn-url]: https://scikit-learn.org/stable/
[FastAPI.com]: https://img.shields.io/badge/FastAPI-0769AD?style=for-the-badge&logo=fastapi&logoColor=009688
[FastAPI-url]: https://fastapi.tiangolo.com/


