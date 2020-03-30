# ![Cover](assets/cover.png)

# Covid Helpline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Marwan01/corona-sms/blob/master/LICENSE)

## Helping spread communication about novel virus Covid-19 via FREE text messages for everyone.

Covid Helpline is a **open source tool** created to raise awareness and boost communication about the current coronavirus outbreak. This is done by making the latest updated data obtained from [John Hopkins' *Covid-19* data repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports)   available to everyone online and offline.

![Demo Gif](assets/covid-helpline-demo.gif)

## Getting Started

to get started, text the below number following the below instructions:

![number](assets/COVID-19TEXTWHITE.png)

* Text **"Advice"** to get CDC's best advice about how to stay safe during the Covid-19 pandemic.
* Text **"News"** to get the latest news articles about Coronavirus from a truthful source:  [News API](https://newsapi.org/).
* Text the desired **country name** *or* **state/province name** to the designated twilio phone number to receive the latest updated data from [John Hopkins' open source repo](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports) about the number of *confirmed cases*, *deaths*, and *recoveries* in that location.
* Text **"Subscribe"** followed by **country/state** name (Example: 'Subscribe Italy') to receieve the most up to date Covid-19 count report from John Hopkins as soon as it is released.
* Text **anything else** to receive the generic helper SMS with all of the above options.
* Text **"Stop"** to opt out.


# Why is this important?

**The biggest issue about pandemics is communication.** As of today, 10% of the U.S population does not use the internet. 42% of older adults are part of that group. The vast majority of Americans – 96% – now own a cellphone of some kind. Of that 96% of Americans only 81% owned a smartphone. We also have 91% of Americans age 65+, who own some type cellphone, of that share 39% of the group do not own a smartphone. Still, these numbers are more extremes in developing countries.

These stats are extremely important; People at higher risk of contracting COVID-19 are older adults and people who have severe chronic medical conditions like heart, lung or kidney disease. According to early CDC data, it is suggested that older people are twice as likely to have serious COVID-19 illness.

Making this information accessible via text, along with the latest Coronavirus news, and the CDC advice about how to stay safe would greatly aid mankind in it's quest to control this fatal virus. Covid Helpline is a *reasonably easy and cheap solution* to this issue.


### Getting Started

This project uses Python and Twilio. To get started make sure you have [Python 3.7+](https://www.python.org/downloads/) and [Twilio CLI](https://www.twilio.com/docs/twilio-cli/quickstart) installed. You can install Twilio CLI with Homebrew using this commad:
`brew tap twilio/brew && brew install twilio`

You will need to login to Twilio CLI:
`twilio login`

In order to run the project you need the following credentials:
* `keys.json` that you can get by generating an IAM role in [GCP](https://cloud.google.com/storage/docs/access-control/iam-roles) with the Storage Object Access Role.
* `keys.py` where you will need to add your Twilio credentials from the [Twillio console](https://www.twilio.com/console) and your News API token that you can genenrate [here](https://newsapi.org/).

Use virtualenv to create an environment and install app dependencies:
```sh
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

To start your own localhost flask server:
`python3 main.py`

Twilio partners with [Ngrok](https://ngrok.com/) which allows you to share your localhost via network. This makes the next command possible and lets you link your python script to Twilio. After logging in to the Twilio CLI, set your Twilio URL webhook to be the one from your localhost:

+19142684397 is our development number. When using your own Twilio account, make sure you replace the below number with your own.

`twilio phone-numbers:update "+19142684397" --sms-url="http://localhost:8080/sms"`

Now you should be able to text your number and use the app.

## Testing
There is currently no testing for the code. Due to the importance of speed of delivery in this situation, we decided to focus on user/load testing and make sure we can scale the functionality to those who need it the most.

## Deployment

We containerize our python app using docker and then deploy it to GCP Cloud Run using the ```deploy.sh``` script. Feel free to take a look at the [Deploy Script](https://github.com/Marwan01/covid-helpline/src/deploy.sh) & the [Dockerfile](https://github.com/Marwan01/covid-helpline/src/Dockerfile)

## Built With

* [Twilio](https://www.twilio.com/) - Programmatically send and receive SMS
* [Python](https://www.python.org/) - Scripting Language

## Contributing

We are currently seeking developers who are willing to give us a hand completing the work listed in the [issues section](https://github.com/Marwan01/covid-helpline/issues) following our [contribution guidelines](https://github.com/Marwan01/covid-helpline/blob/master/.github/CONTRIBUTING.md).

- To be added as a contributor, please contact us via covid.helpline@gmail.com.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Marwan01/covid-helpline/tags).

## Authors

* **Alexandru Andrei** - *Initial work* - [AlexAndrei98](https://github.com/AlexAndrei98)
* **Ajay Raj** - *Feature Development* - [ajayraj](https://github.com/ajayraj)
* **Anna Tyan** - *Design work/Public Relations/Marketing* - [annajt178](https://github.com/annajt178)
* **Glenn Parham** - *Feature Development* - [glennparham](https://github.com/glennparham)
* **Marouen Helali** - *Initial work* - [Marwan01](https://github.com/Marwan01)
* **Sumiya Choudhry** - *Scrum Coordinator/Public Relations/Marketing* - [SumiyaChoudhry](https://github.com/SumiyaChoudhry)
* **Vanessa Trujillo** - *Initial work* - [trujivan](https://github.com/trujivan)
* **Vlad Khudik** - *Initial work* - [VoltK](https://github.com/VoltK)
* **Cleopatra Nestor** - *Public Relations/Marketing*
* **Karla Bravo** - *Lead Video Editor* 
* **Kassidy Tharp** - *Public Relations/Marketing* 


See also the list of [contributors](https://github.com/Marwan01/covid-helpline/contributors) who participated in this project.

# Copyright & License

Copyright (c) 2020 Covid Helpline - Released under the [MIT license](https://github.com/Marwan01/covid-helpline/blob/master/LICENSE). Covid Helpline and the Covid Helpline logo are trademarks of Covid Helpline official contributors. [Code of Conduct](https://github.com/Marwan01/covid-helpline/blob/master/CODE_OF_CONDUCT.md)

# Support

 *This project is in serious need of contributions and funding.* If you are interested in saving the world, getting your questions answered, or reaching out to the developers, contact us at via covid.helpline@gmail.com. We are currently asking for donations via this [GoFundMe page](https://www.gofundme.com/f/help-spread-information-about-covid19-via-text) and would really appreciate any donation amount. The goal is to keep Covid Helpline running for FREE for all of its users. Help us with our mission by helping us spread the word on social media: [Facebook](https://www.facebook.com/covidhelpline) & [Instagram](https://www.instagram.com/covid19helpline/).
