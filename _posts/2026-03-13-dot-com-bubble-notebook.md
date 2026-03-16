---
layout: post
title: Fed Dot Plot (Federal Reserve Interest Rate Projections)
date: 2026-03-12 16:30:00-0600
description: explainer for the Fed dot plot
tags: jupyter notebook markets fed
categories: research-notes
giscus_comments: false
related_posts: false
published: true
---

The Fed dot plot is the market's shorthand for the Federal Open Market Committee's chart of where individual participants think the federal funds rate should be at the end of future years.

Each dot represents one participant's rate projection. Readers usually look for three things first:

1. The cluster of dots for the next year
2. The median path across future years
3. Whether the distribution is spreading out or converging

The notebook below recreates a recent Fed-style dot plot using the latest available official Summary of Economic Projections release from December 10, 2025.

{::nomarkdown}
{% assign jupyter_path = "assets/jupyter/dot_com_bubble.ipynb" | relative_url %}
{% capture notebook_exists %}{% file_exists assets/jupyter/dot_com_bubble.ipynb %}{% endcapture %}
{% if notebook_exists == "true" %}
{% jupyter_notebook jupyter_path %}
{% else %}

<p>Sorry, the notebook you are looking for does not exist.</p>
{% endif %}
{:/nomarkdown}
