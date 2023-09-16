# [spacetrash.live](https://spacetrash.live)
Open source web application for real-time visualization of space debris. 
Ability to synchronize local data sources through TLE files.

#### The application is structured as follows:
- A [program](src/app/sync_task.py) to sync [data sources](src/app/sync-settings.json)
- A Flask [web app](src/app/main.py) to serve static files and [sources](src/pub/api)
