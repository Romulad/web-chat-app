# Web Chat App : Open real time chat without authentication


## You can:
- Create a chat and get a link
- Share chat link with friends to invite them to join, as many as you want
- Approve join request, to allow others to be added to the chat
- Chat and have fun
- As the chat owner, you can delete the chat and all related data with just a click once you're done


**Live version:** [click here(over http, avoid entering sensitive informationa)](http://ec2-35-180-138-45.eu-west-3.compute.amazonaws.com)

[![Watch the video](https://img.youtube.com/vi/jxiMnjLykxo/hqdefault.jpg)](https://www.youtube.com/watch?v=jxiMnjLykxo)


## Technologies
- **Frontend**: TypeScript, React, Tailwind CSS
- **Backend**: Python, FastAPI, WebSocket, Redis


## Run locally


#### Clone the repo
First of all you need [Git](https://git-scm.com/downloads) on your system\
to be able to clone the repository.

The following instructions assume that [Git](https://git-scm.com/downloads)\
is installed:

- Open your terminal
- navigate to the folder where you want to clone the repository
- clone the repository to your local machine by running:
```bash
git clone https://github.com/Romulad/web-chat-app.git
```
- then navigate to the newly created directory to follow the next instructions:
```bash
  cd web-chat-app
```

***important***: You need to provide redis connection details in a `.env` file within the `api` directory. 
Use the `.env.template` file under the `api` directory as an example. The next instructions assume you did this!

[Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/)


### Using Docker compose
The app includes Docker compose file for production like environment without ssl, over http only

You need to have :

1. [Docker](https://www.docker.com/products/docker-desktop/)
2. [Docker compose](https://docs.docker.com/compose/install/)

installed before following these instructions.

Make sure [Docker](https://www.docker.com/products/docker-desktop/) engine is running\
on your system and Docker client is accessible from your command line

#### Run with compose
To run in a production like environment: 
- at the root of the project run:
```bash
docker compose up -d
```
Visit `localhost` to view the app.


### By setting up the dev environment
To run this app locally make sure you have the following prerequisites on your system:
- [Node.js](https://nodejs.org/en/download/current), this include `npm` (Node Package Manager) will be used to 
run the [React app](https://react.dev) (Front-end). 
- [Python intepreter](https://www.python.org/downloads/), will be used to run the [FastApi app](https://fastapi.tiangolo.com/) (API). 


#### Install dependencies and run the FastApi app
In a terminal :
- Navigate to the `api` subdirectory under the project root directory:
```bash
  cd api
```
- Create a virtual environment:
```bash
  python -m venv venv
```
- Activate the virtual environment:
  1. On windows
```bash
  .\venv\Scripts\activate
```
  2. On macOS/Linux:
```bash
  source venv/bin/activate/
```
- Install the required packages:
```bash
  pip install -r requirements.txt
```
- once the installation is completed start the app with:
```bash
  fastapi dev
```
  
Visit `localhost:8000/docs` to view the api doc, next step to see the full app.


#### Install dependencies and run the front-end :
In a new terminal :
- Navigate to the `web` directory by running:
```bash
  cd web
```
- install the necessary packages by running this command:
```bash
  npm install
```
- once the installation is completed start the app with:
```bash
  npm run dev
```
  
And you're done! visit `localhost:3000` to view the app.
