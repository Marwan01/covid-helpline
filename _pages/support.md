---
layout: page
title: Support
include_in_header: true
---

# Support

This project is in serious need of contributions and funding. If you are interested in saving the world, getting your questions answered, or reaching out to the developers, contact us at via [email](mailto:covid.helpline@gmail.com). 
<br>
We are currently asking for donations via this [GoFundMe](https://www.gofundme.com/f/help-spread-information-about-covid19-via-text) page and would really appreciate any donation amount. The goal is to keep Covid Helpline running for FREE for all of its users. 

## Sharing = Caring

Stay on top of the latest updates and help us with our mission by spreading the word on social media.

Follow us on [Facebook](https://www.facebook.com/covidhelpline), [Instagram](https://www.instagram.com/covid_helpline/) and [Youtube](https://www.youtube.com/channel/UC1XCOJ4hYywwJnBfrkbtvfA)

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

