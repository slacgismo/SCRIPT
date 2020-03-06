# SCRIPT-frontend

## Standalone Deployment

### Prerequisites

1. Install `docker`. For more details, please refer to [Install Docker](https://docs.docker.com/v17.09/engine/installation/).
2. Please launch [webserver](/webserver/README.md) first before running this frontend.

### Run

1. Build the image:

```bash
docker build -t script/frontend .
```

2. Run in docker container:

```bash
docker run -it --name script_frontend -p 3000:3000 --entrypoint bash script/frontend
```

In the prompted shell, start the frontend:

```bash
npm start
```

Then, you can visit the `localhost:3000` to see the web page.

## Development

### Prerequisites

1. You should have [Node.js](https://nodejs.org/en/download/) installed.
2. Please launch [webserver](/webserver/README.md) first before running this frontend.

### Run

1. Install all modules using:

```bash
npm install
```

2. Start React App:

```bash
npm start
```

Then, you can visit the `localhost:3000` to see the web page.
