# Web Chat App : Open real time chat without authentication


## You can:
- Create a chat and get a link
- Share chat link with friends to invite them to join, as many as you want
- Approve join request, to allow other to be added to the chat
- Chat and have fun
- Once done, as chat owner, with just a click, delete the chat and all related data.


Live version : [click here(over http, don't enter sensitive data)](http://ec2-35-180-138-45.eu-west-3.compute.amazonaws.com)


## Technologies
1. **TypeScript**/**React**
2. **Tailwind CSS**
3. **Python**/**FastApi**
4. **Websocket**
5. **Redis**


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

***important***: You need to provide redis connection details in a `.env` file within the `api` directory. Take `.env.template` file under the `api` directory as an example.

[Redis](https://redis.io)


### Using Docker compose
The app includes Docker compose files for production like environment without ssl, thus over http only

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
- [Node.js](https://nodejs.org/en/download/current), this include `npm` (Node Package Manager) will be use to run the app. 
- [Python](https://nodejs.org/en/download/current), this include `npm` (Node Package Manager) will be use to run the app. 
- [Redis](https://nodejs.org/en/download/current), this include `npm` (Node Package Manager) will be use to run the app. 


#### Install dependencies and run the app
In your terminal :
- Navigate to the new directory created by running:
```bash
  cd figma-to-code-ed2-week3
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
