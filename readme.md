# Python scripts(bots) that are hosted in the cloud to run on a scheduled basis

## How does it work?

- Make a simple flask application and place the script in a route.

- Connect the repo with Heroku or a similar platform.

- If you are a Heroku verified user, you could use [this](https://elements.heroku.com/addons/scheduler) addon. You need to add a credit card to verify your account.

- Create a new account on [WayScript](https://www.wayscript.com/)

- Create a liar that is preset with the Python Cron Job template.

- The default file will be tasks.py. Use the requests module to make a get request to the route where you have placed your script in step 1.

- Create the requirements.txt file in the root directory and add the requests module.

- Open the trigger file and add the time when you want to run the tasks.py file. Visit [CrontabGuru](https://crontab.guru/) if you do not know how to schedule a task with a cron.

- Finally, deploy the liar.

### PS. If you do not deploy your liar, the trigger file will not run
