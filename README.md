# Daily Python Tips

App built for [Code Challenge 40 - Daily Python Tip Part 1 - Make a Web App](https://pybit.es/codechallenge40.html)

I deployed it to [https://pytip.herokuapp.com](https://pytip.herokuapp.com)

Modules:
* `db.py` -> SQLAlchemy models
* `import_tweets.py` -> syncs [python_tip](https://twitter.com/python_tip)'s tweets to a Postgres DB
* `app.py` -> Bottle app

Env variables:
* Twitter API: CONSUMER_KEY / CONSUMER_SECRET / ACCESS_TOKEN / ACCESS_SECRET
* DATABASE_URL = 'postgres://user:pw@localhost:5432/pytip'
* If your run it on Heroku set APP_LOCATION to *heroku* (similar deployment instructions as [prchecker](https://github.com/pybites/prchecker))
