# Plex Recommendations AI

This project involves creating a 'Recommended' collection on your Plex server using the power of OpenAI. 
By analyzing your unique watch history, it will provide you with personalized suggestions that perfectly align with your preferred genre. 
With this feature, you'll easily discover a handful of delightful recommendations from your extensive movie list, making it a breeze to find your next enjoyable watch!

## Features

- Auto create/update a plex movie collection.
- Dynamic results based on ChatGPT results and Plex watch history.
- Creates a short description on the plex collection describing why it chose them movies.

## You'll need

- Plex server host and port
- Plex token
- Open AI account and key - Can be obtained from their website.
- Docker setup

## Setup

You'll need docker set up on your server and to best way to run this is through docker-compose.

Use this example below:

```yaml
version: "2.1"
services:
  plex-recommendations:
    image: silkychap/plex-recommendations-ai:latest
    container_name: plex-recommendations
    environment:
      - PLEX_URL=<local plex url>
      - PLEX_TOKEN=<plex token>
      - OPEN_AI_KEY=<open ai key>
      - LIBRARY_NAME=<library name>
      - COLLECTION_TITLE=<title>
      - HISTORY_AMOUNT=<amount>
      - RECOMMENDED_AMOUNT=<amount>
      - MINIMUM_AMOUNT=<amount>
      - SECONDS_TO_WAIT=<amount>
    restart: unless-stopped
```

## Stuff to do / to add
- Implement individual user collections for managed users (if possible?).
- Create more configurable options cater the movie list.
- Add TV shows functionality.
- Allow matching data past 2021?