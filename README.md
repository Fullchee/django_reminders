# Django Reminders

## Links

- Frontend React App
  - [🌐︎ Website](https://fullchee-reminders.netlify.app/)
  - [:octocat: GitHub](https://github.com/Fullchee/reminders-frontend)
- Backend
  - [:octocat: GitHub](https://github.com/Fullchee/django_reminders)
  - Django, Postgres

## Setup

* Python 3.9+
* Postgres 13.2+


1. Run `./build.sh`
   1. Old way: Create a virtual environment
   
      * `python -m venv venv`
      * `source venv/bin/activate
      2. `python install -r ./requirements.txt`
2. `pipenv shell`
3. `python manage.py migrate`
4. Copy and override the environment variables
   * `cp sample.env .env`
5. Add the env variables to your `~/.zshrc`
6. Uncomment out `~/.config/pip/pip.conf`

```sh
PYTHONUNBUFFERED=1;
DJANGO_SETTINGS_MODULE=django_reminders.settings
```


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
