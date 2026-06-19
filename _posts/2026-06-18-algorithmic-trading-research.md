---
layout: post
title: Polymarket Simple Tutorial
date: 2026-06-18 10:00:00-0600
description: notebook for market discovery, order book analysis, and trading research APIs
tags: jupyter notebook code quantitative
categories: research-notes
giscus_comments: false
related_posts: false
published: true
---

This notebook is a simple research starter for market discovery, token-level price analysis, order-book inspection, and user activity analysis using the Gamma, CLOB, and Data APIs.

{::nomarkdown}
{% assign jupyter_path = "assets/jupyter/polymarket_simple_tutorial.ipynb" | relative_url %}
{% capture notebook_exists %}{% file_exists assets/jupyter/polymarket_simple_tutorial.ipynb %}{% endcapture %}
{% if notebook_exists == "true" %}
{% jupyter_notebook jupyter_path %}
{% else %}

<p>Sorry, the notebook you are looking for does not exist.</p>
{% endif %}
{:/nomarkdown}
