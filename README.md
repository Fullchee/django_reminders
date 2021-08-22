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
* virtual-env
* Postgres 13.2+

1. Setup your virtual environment and enter it
2. `python install -r ./requirements.txt`
3. `python manage.py migrate`
4. Start the Django app with the environment variables

```
PYTHONUNBUFFERED=1;
DJANGO_SETTINGS_MODULE=django_reminders.settings
```

### .env
In `django_reminders/.env` (not the root)

copy from Heroku? (or BitWarden)


## Asana
https://app.asana.com/0/1200788876937280/1200788876937280


**Previous API (GraphQL)**

* https://github.com/Fullchee/reminders-backend/blob/master/src/index.js

**Why I switched**

I heard a lot about GraphQL APIs so I decided to implement one for this project.

I decided to redo the backend with Django because I was hired as a full stack developer at Forma
and wanted some practice with their tech stack.