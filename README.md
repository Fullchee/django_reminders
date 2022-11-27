# Django Reminders

## Links

- Frontend React App
  - [Website](https://fullchee-reminders.netlify.app/)
  - [GitHub](https://github.com/Fullchee/values-client)
- Backend
  - [GitHub](https://github.com/Fullchee/django_reminders)
  - Postgres, Node, Express

## Setup

### Requirements
* Python 3.9+
* Postgres 13.2+

1. Create a virtual environment
   
   * `python -m venv venv`
   * `source venv/bin/activate

2. `python install -r ./requirements.txt`
3. `python manage.py migrate`
4. Add the env variables to your `~/.zshrc`
5. Copy and override the environment variables
   * `cp sample.env .env`
5. Start the Django app with the environment variables


```sh
PYTHONUNBUFFERED=1;
DJANGO_SETTINGS_MODULE=django_reminders.settings
```

### .env
In `django_reminders/.env`


## Decisions

### Moving away from GraphQL

**Previous API (GraphQL) Backend App**

* https://github.com/Fullchee/reminders-backend/blob/master/src/index.js

**Why I switched away from GraphQL**

I heard a lot about GraphQL APIs, so I decided to implement one for this project.

I decided to redo the backend with Django

* I was hired as a full stack developer at Forma.ai.
* and wanted some practice with their tech stack


### Why not pipenv`

I'm deployed on render.com's free tier and virtual environments just worked

So I didn't bother with migrating from `venv` to `pipenv`
