---
layout: post
title: Fed Inflation CPI and Core CPI
date: 2026-06-16 10:00:00-0600
description: notebook for CPI and core CPI inflation from FRED
tags: jupyter notebook fed quantitative
categories: research-notes
giscus_comments: false
related_posts: false
published: true
---

This notebook pulls CPI and core CPI from FRED, calculates year-over-year inflation, and compares the headline index with core CPI excluding food and energy.

{::nomarkdown}
{% assign jupyter_path = "assets/jupyter/fed_inflation_cpi.ipynb" | relative_url %}
{% capture notebook_exists %}{% file_exists assets/jupyter/fed_inflation_cpi.ipynb %}{% endcapture %}
{% if notebook_exists == "true" %}
{% jupyter_notebook jupyter_path %}
{% else %}

<p>Sorry, the notebook you are looking for does not exist.</p>
{% endif %}
{:/nomarkdown}
