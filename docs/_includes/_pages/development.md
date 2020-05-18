---
layout: page
title: Development
include_in_header: true
---

# Development

## Getting started
This project uses Python and Twilio. To get started make sure you have [Python 3.7+](https://www.python.org/downloads/) and [Twilio CLI](https://www.twilio.com/docs/twilio-cli/quickstart) installed. You can install Twilio CLI with Homebrew using this commad:

<dl>brew tap twilio/brew && brew install twilio</dl>

You will need to login to Twilio CLI:

`twilio login`

In order to run the project you need the following credentials:


- `keys.json` that you can get by generating an IAM role in [GCP](https://cloud.google.com/storage/docs/access-control/iam-roles) with the Storage Object Access Role.
- `keys.py` where you will need to add your Twilio credentials from the [Twillio console](https://www.twilio.com/login?g=%2Fconsole%3F&t=2b1c98334b25c1a785ef15b6556396290e3c704a9b57fc40687cbccd79c46a8c) and your News API token that you can genenrate [here](https://newsapi.org/).

Use virtualenv to create an environment and install app dependencies:

```virtualenv venv```<br>
```source venv/bin/activate```<br>
```pip3 install -r requirements.txt ```

To start your own localhost flask server:

`python3 main.py`

Twilio partners with [Ngrok](https://ngrok.com/) which allows you to share your localhost via network. This makes the next command possible and lets you link your python script to Twilio. After logging in to the Twilio CLI, set your Twilio URL webhook to be the one from your localhost:

+19142684397 is our development number. When using your own Twilio account, make sure you replace the below number with your own.

`twilio phone-numbers:update "+19142684397" --sms-url="http://localhost:8080/sms"`


Now you should be able to text your number and use the app.

## Testing

There is currently no testing for the code. Due to the importance of speed of delivery in this situation, we decided to focus on user/load testing and make sure we can scale the functionality to those who need it the most.

## Deployment

We containerize our python app using docker and then deploy it to GCP Cloud Run using the `deploy.sh` script. Feel free to take a look at the [Deploy Script](https://github.com/Marwan01/covid-helpline/blob/master/src/deploy.sh) & the [Dockerfile](https://github.com/Marwan01/covid-helpline/blob/master/src/Dockerfile).

## Built With

- [Twilio](https://www.twilio.com/) - Programmatically send and receive SMS
- [Python](https://www.python.org/) - Scripting Language

## Contributing

We are currently seeking developers who are willing to give us a hand completing the work listed in the [issues section](https://github.com/Marwan01/covid-helpline/issues) following our [contribution guidelines](https://github.com/Marwan01/covid-helpline/blob/master/.github/CONTRIBUTING.md).

To be added as a contributor, please contact us via [email](mailto:covid.helpline@gmail.com).

## Versioning

We use [SemVer](https://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Marwan01/covid-helpline/tags).

See also the [list of contributors](https://github.com/Marwan01/covid-helpline/graphs/contributors) who participated in this project.


## Copyright & License

Copyright (c) 2020 Covid Helpline - Released under the [MIT license](https://github.com/Marwan01/covid-helpline/blob/master/LICENSE). Covid Helpline and the Covid Helpline logo are trademarks of Covid Helpline official contributors. 


## Support

This project is in serious need of contributions and funding. If you are interested in saving the world, getting your questions answered, or reaching out to the developers, contact us at via [email](mailto:covid.helpline@gmail.com). We are currently asking for donations via this [GoFundMe](https://www.gofundme.com/f/help-spread-information-about-covid19-via-text) page and would really appreciate any donation amount. The goal is to keep Covid Helpline running for FREE for all of its users. Help us with our mission by helping us spread the word on social media: [Facebook](https://www.facebook.com/covidhelpline) & [Instagram](https://www.instagram.com/covid_helpline/).

<br><br>

<footer>
	<!--
	{% if site.your_name %}
	<p class="footerText">Made by {% if site.your_link %}<a href="{{ site.your_link }}">{% endif %}{{ site.your_name }}{% if site.your_link %}</a>{% endif %}{% if site.your_city %} in {{ site.your_city }}{% endif %}</p>
	{% endif %}
	-->
	<div class="footerIcons">
		{% if site.facebook_username %}
			<a href="https://facebook.com/{{ site.facebook_username }}">
				<span class="fa-stack fa-1x">
					<i class="socialIconBack fas fa-circle fa-stack-2x"></i>
					<i class="socialIconTop fab fa-facebook fa-stack-1x"></i>
				</span>
			</a>
		{% endif %}
		{% if site.twitter_username %}
			<a href="https://twitter.com/{{ site.twitter_username }}">
				<span class="fa-stack fa-1x">
					<i class="socialIconBack fas fa-circle fa-stack-2x"></i>
					<i class="socialIconTop fab fa-twitter fa-stack-1x"></i>
				</span>
			</a>
		{% endif %}
		{% if site.github_username %}
			<a href="https://github.com/{{ site.github_username }}">
				<span class="fa-stack fa-1x">
					<i class="socialIconBack fas fa-circle fa-stack-2x"></i>
					<i class="socialIconTop fab fa-github fa-stack-1x"></i>
				</span>
			</a>
		{% endif %}
		{% if site.email_address %}
			<a href="mailto:{{ site.email_address }}">
				<span class="fa-stack fa-1x">
					<i class="socialIconBack fas fa-circle fa-stack-2x"></i>
					<i class="socialIconTop fas fa-envelope fa-stack-1x"></i>
				</span>
			</a>
		{% endif %}
	</div>
	<div class="footerLinks">
		{% for page in site.pages %}
			<a href="{{ page.url | relative_url }}" target="_self">{{ page.title }}</a>
		{% endfor %}
		{% if site.presskit_download_link %}
			<a href="{{ site.presskit_download_link }}">Press Kit</a>
		{% endif %}
	</div>
</footer>

















