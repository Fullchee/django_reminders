# Django Reminders

## Links

- Frontend React App
  - [🌐︎ Website](https://fullchee-reminders.netlify.app/)
  - [:octocat: GitHub](https://github.com/Fullchee/reminders-frontend)
- Backend
  - [:octocat: GitHub](https://github.com/Fullchee/django_reminders)
  - Hosted on [render.com](render.com)'s free tier
  - Django, Postgres

## Setup

1. [Install poetry](https://python-poetry.org/docs/)
   1. Install `poetry self add poetry-dotenv-plugin`
2. `cp sample.env .env`
3. Run `./setup.sh`
   1. runs `poetry install`
   2. `poetry run manage.py migrations`
4. Possibly uncomment out `~/.config/pip/pip.conf`?
   1. I think Poetry doesn't use this file

## Decisions

### Moving away from GraphQL (2021)

**Previous API (GraphQL) Backend App**

* https://github.com/Fullchee/reminders-backend/blob/master/src/index.js

**Why I switched away from GraphQL**

I heard a lot about GraphQL APIs, so I decided to implement one for this project.

I decided to redo the backend with Django

* I was hired as a full stack developer at Forma.ai.
* and wanted some practice with their tech stack


### Why poetry

At work, we use virtual environments so the first installment of `django_reminders` was the same as at work. 

I'm deployed on render.com's free tier and the existing virtual environments just worked.

Then, I moved to `pipenv`

However, I was getting some issues upgrading Django.

So, I'm trying poetry and I'm liking the DX which is similar to what I'm used to from the JavaScript ecosystem.

I've heard good things about pytest. However, we use `unittest` at work so I'm gonna stick with that.
