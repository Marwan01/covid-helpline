---
layout: page
title: About
include_in_header: true
---

# About

Covid Helpline is a non-profit, open source, community driven initiative created to raise awareness and facilitate accurate information and communication regarding current Coronavirus outbreak. We make the latest updated data obtained from [John Hopkins University’ Covid-19 data repository](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports) available via SMS, along with important tips and news about Covid-19.
<br>

<iframe width="560" height="315" src="https://www.youtube.com/embed/axAEKzDHBm4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
<br>

# Why is this important?

Some of the biggest challenges we are facing during this pandemic are a lack of communication and misinformation of the general public, especially the elderly which are most vulnerable. Currently, around 10% of the U.S population does not use the internet. Around 42% of older adults are part of that group. The good news is that the vast majority of Americans – 96% – now own a cellphone of some kind. However, of that 96% of Americans with access to a cell phone only 81% have owned a smartphone. Moreover when looking at the aging population, around 91% of Americans age 65+, own some type cellphone, however, 39% of that group do not own a smartphone. 

These statistics are extremely important due to the fact that the people with the highest risk of contracting COVID-19 are older adults and individuals who have severe chronic medical conditions such as heart, lung or kidney disease. According to early CDC data, it is suggested that the older population is twice as susceptible to contract a serious case of the COVID-19 virus.

Making this vital information accessible via text, along with the latest Coronavirus news, and the CDC’s advice about how to stay safe in this time would greatly aid in the quest to control this fatal virus. Covid Helpline offers a reasonably easy and cost effective solution to this issue.

[Learn more about our mission in this Youtube video from our team](https://www.youtube.com/watch?v=axAEKzDHBm4&feature=youtu.be)

# Our team

    Alexandru Andrei - Initial work 
	Marouen Helali - Initial work 
	Vanessa Trujillo - Initial work 
    Anna Tyan - Web & Digital Design 
    Glenn Parham - Feature Development 
    Sumiya Choudhry - Scrum Coordinator 
    Vlad Khudik - Initial work 
	
    Cleopatra Nestor - Public Relations
    Karla Bravo - Video Editor
    Kassidy Tharp - Marketing 
    Cristiana Faur - Marketing
	Andrea Hoppert - Marketing 
	Vince McDonnell - Marketing/Video Content
	Davina Agasaro - Marketing 


# Contribution

We are currently seeking to work with other likeminded developers who are willing to give us a hand in completing the work listed in the [issues section](https://github.com/Marwan01/covid-helpline/issues) following our [contribution guidelines](https://github.com/Marwan01/covid-helpline/blob/master/.github/CONTRIBUTING.md).


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
		{% if site.instagram_username %}
			<a href="https://instagram.com/{{ site.instagram_username }}">
				<span class="fa-stack fa-1x">
					<i class="socialIconBack fas fa-circle fa-stack-2x"></i>
					<i class="socialIconTop fab fa-instagram fa-stack-1x"></i>
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
		{% if site.youtube_username %}
			<a href="https://youtube.com/{{ site.youtube_username }}">
				<span class="fa-stack fa-1x">
					<i class="socialIconBack fas fa-circle fa-stack-2x"></i>
					<i class="socialIconTop fab fa-youtube fa-stack-1x"></i>
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

