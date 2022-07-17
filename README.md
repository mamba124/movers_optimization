To launch the project


##**via docker**

docker-compose up --build
In case you need **START**/**FINISH** time adjustment configure it in **Dockerfile** env vars


##**locally**
0. Install Geckodriver (preferable) or Chromedriver on your machine
1. Install project requirements in a separated env
2. Run the command depending on the webdriver you've installed at previous step.
   In case you need START/FINISH time adjustment indicate it
 Run ```RUNTIME=<local_firefox|remote_firefox|chrome> START=7 FININSH=19 sh restart_bot.sh```


Here are main bot's runtimes:
* local_firefox - launch on your local machine using proxy. Geckodriver must be preinstalled 
* remote_firefox - launch(preferably) on remote machine. Geckodriver must be preinstalled 
* chrome - launch(preferably) on remote machine. Chromedriver must be preinstalled
* docker - launch anywhere you want. Your docker preconfigure 

By default everywhere is configured *headless* mode as option for webdriver. 
It is done, because otherwise buttons are not interactable. 

In case new versions of the website appear, don't hesitate to update src/inbox_selectors.py 
