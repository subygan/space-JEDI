# JEDI (Junk Elimination and Debris Interception)

![Demo](/space-jedi.gif)

Open source web application for real-time visualization of space debris. 
And plotting an optimal path to collect all debris
Ability to synchronize local data sources through TLE files.

#### The application is structured as follows:
- A [program](src/app/sync_task.py) to sync [data sources](src/app/sync-settings.json)
- A Flask [web app](src/app/main.py) to serve static files and [sources](src/pub/api)
