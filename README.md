# Space-JEDI (Junk Elimination and Debris Interception) <img src="./logo.gif" alt="Logo" width="60">

[![Demo](/space-jedi.gif)](https://www.youtube.com/watch?v=HA45-t5H0x4)

**[Click Above for Full Demo!](https://www.youtube.com/watch?v=HA45-t5H0x4)**

## Inspiration

Imagine a future where our skies are free from the peril of dangerous space debris, where accidents caused by space debris collisions are almost non-existent. Currently, there are approximately 23,000 pieces of debris larger than a softball orbiting the Earth, hurtling through space at speeds of up to 17,500 mph. Even a relatively small piece of orbital debris can pose a significant threat to satellites and spacecraft. Moreover, the number of these objects is increasing daily, highlighting the urgency of addressing this issue.

### The Space Debris Market: A $1.2 Trillion Opportunity

One of the key aspects to consider in addressing the space debris problem is the potential economic impact. The space debris market is worth over $1.2 trillion, and this figure continues to grow as the space industry expands. This market includes various sectors such as debris removal, satellite protection, and space traffic management.

As we tackle the challenge of space debris, not only are we safeguarding our space infrastructure, but we are also tapping into a massive economic opportunity that can drive innovation and growth in the space industry.

Join us in exploring the future of space debris management and the immense potential it holds for both safety and economic prosperity.

## What it does

**Junk Elimination and Debris Interception (JEDI)** is a revolutionary solution designed to predict the future positions of satellites and plot optimal flight plans for space garbage collectors. By continuously tracking and analyzing real-time data from NASA, JEDI is able to effectively monitor and manage objects in Earth's orbit.

## How we built it

Our development process involved the following key steps:

- **Data Collection**: We obtained satellite data from NASA's extensive satellite tracking database.
- **Visualization**: We created a 3D map using latitude, longitude, altitude, and object size information to visualize the positions of objects in space.
- **Predictive Modeling**: Using velocity and direction data, we developed algorithms to predict the future positions of orbital debris. This information is then used to chart efficient flight paths for garbage collectors, such as those deployed from the International Space Station (ISS).

## Challenges we ran into

Our journey was not without its share of challenges:

- **Real-Time Data Acquisition**: Accessing real-time data for tracking debris presented a significant hurdle.
- **Predictive Modeling Complexity**: Predicting the future positions of thousands of moving objects in space proved to be a computationally intensive NP-hard problem.
- **3D Path Planning**: Designing optimal flight paths in a 3D space was a complex task that required innovative solutions.

## Accomplishments that we're proud of

Our team achieved several noteworthy accomplishments:

- **Global Modeling**: We successfully built a global model and integrated it with live satellite data.
- **Complex Prediction**: Tackling the NP-hard problem of predicting and plotting flight paths for numerous moving objects was a significant achievement.
- **Endurance**: We demonstrated dedication and perseverance by working on the project for nearly 20 continuous hours.

## What we learned

Through the course of this project, we gained valuable insights:

- **Abundance of Open Data**: We discovered a wealth of open data related to space objects, ranging from debris to celestial bodies.
- **Complexity of Object Prediction**: Predicting the movements of objects in space is a challenging task that requires advanced mathematical and computational techniques.

## What's next for Junk Elimination and Debris Interception (JEDI)

Our vision for the future of JEDI includes:

- **Incorporating Additional Data**: We plan to expand our data sources by integrating data from other space observation projects.
- **Advanced Path Planning**: We aim to further refine and optimize the flight path planning algorithms.
- **Enhanced Space Cleanup**: We will continue our efforts to contribute to a cleaner and safer space environment.

## Team Info

- **[Suriya Ganesh](https://www.linkedin.com/in/suriya-ganesh/) - sayyampe**
- **[Aman Priyanshu](https://www.linkedin.com/in/aman-priyanshu/) - apriyans**
- **[Yash Maurya](https://www.linkedin.com/in/yashmaurya/) - ymaurya**

#### The application is structured as follows:
- A [program](src/app/sync_task.py) to sync [data sources](src/app/sync-settings.json)
- A Flask [web app](src/app/main.py) to serve static files and [sources](src/pub/api)
