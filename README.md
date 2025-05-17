# FastAPI AI Scaffolding Strategist

This project provides a simple FastAPI service used as a template for deployment on [Render](https://render.com). It now includes an example API for managing interactive question sessions.

## Features

- Create sessions with optional custom questions
- Retrieve and answer questions
- Persist session progress across restarts
- Review completed steps and get suggested next actions

## Running Locally

Install dependencies and start the development server:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Deploying to Render

1. Create a new Web Service and point it at this repository.
2. Render will install dependencies from `requirements.txt`.
3. Use the following Start Command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Or click the button below:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/render-examples/fastapi)

## Thanks

Thanks to [Harish](https://harishgarg.com) for the inspiration to create a FastAPI quickstart for Render and for some sample code!
