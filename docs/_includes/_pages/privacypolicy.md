---
layout: page
title: Privacy Policy
include_in_header: false
---

**Last updated**  
May 13, 2020

# Privacy Policy
Your privacy is important to Covid Helpline so we’ve developed a Privacy Policy that covers how we collect, use, disclose, transfer, and store your personal information.


**Please** take a moment to familiarize yourself with our privacy practices and [contact us](mailto:covid.helpline@gmail.com) if you have any questions.

<br>

## Information We Collect

- User's phone number and origin based solely on the area code where the user had been registered. 
- Number of unique users' numbers
- Number of subscribers

<br>

## Information you provide to us 
- Unique user's phone number

<br>

##  How we store and secure the Personal Information we collect
Covid Helpline takes the security of your personal information very seriously. When your personal data is stored by Covid Helpline, we use computer systems with limited access housed in facilities using physical security measures. 

When you use other products, services, and applications or post on forums, chat rooms, or social networking services, the personal information and content you share that is visible to other users and can be read, collected and used by them. You are responsible for the personal information you choose to share or submit in these instances. For example, if you list your name and phone number in a forum posting, that information is public. Please take caution when using these features.

<br>

## Our Companywide Commitment to Your Privacy 
To make sure your personal information is secure, we communicate our privacy and security guidelines witht the entire team at Covid Helpline team and strictly enforce privacy safeguards within the company.

<br>

## Privacy Questions
If you have any questions or concerns about Covid Helpline’s Privacy Policy or data processing, you would like to contact our Data Protection Officer, or if you would like to make a complaint about a possible breach of local privacy laws, please [contact us](mailto:covid.helpline@gmail.com).



Covid Helpline team 



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

