# TurnPCBot

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/AlexandrVino/TurnPCBot">
    <img src="https://raw.githubusercontent.com/othneildrew/Best-README-Template/master/images/logo.png" alt="Logo" width="80" height="80">
  </a>
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
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Now, in conditions of isolation, many companies are forced to transfer employees to remote work. And often computers are always on, which is bad. And so I decided to write this bot.
</br>

### Built With

* [Python](https://nextjs.org/)
* [Aiogram](https://github.com/aiogram/aiogram/)
* [Environs](https://github.com/sloria/environs/)
* [Wakeonlan](https://github.com/remcohaszing/pywakeonlan/)
* [Asyncpg](https://github.com/MagicStack/asyncpg/)
* [Requests](https://requests.readthedocs.io/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Installation
If you want to use your bot with my code:
1. Clone the repo
   ```sh
   git clone https://github.com/AlexandrVino/TurnPCBot.git
   ```
2. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```
3. Create `.env` file with db and bot data (Example: `env-example.env`)
4. Enter your Bot Name in `data/config.py`
   ```py
   #
   # You should reset bot name if your bot launch on your company server; 
   # else if you use @TurnOnPcBot should globally turn server from https://github.com/AlexandrVino/TurnOnPcBotServer.git) 
   # 
   BOT_NAME = 'TurnOnPcBot'  # Your bot name here (can be like "")
   ```
else:
1. Clone the repo
   ```sh
   git clone https://github.com/AlexandrVino/TurnOnPcBotServer.git
   ```
2. Globally turn server.
    ```pycon
   # For example download ngrok from https://ngrok.com/download
   # Turn in shell with any free port
   # Example (in ngrok shell): ./ngrok http 4567
    ```

3. Set host in bot
    ```pycon
    # Example bot command: /host http://7e9ea9dc.ngrok.io 
    ```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->




