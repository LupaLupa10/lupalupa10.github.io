---
layout: post
title: Agentic AI in Data Preprocessing for PD Modeling
date: 2026-03-24 17:00:00-0600
description: notebook walkthrough for agentic preprocessing in probability of default modeling
tags: jupyter notebook ai code quantitative
categories: research-notes
giscus_comments: false
related_posts: false
published: true
---

This notebook shows an agentic approach to preprocessing a probability of default dataset. It walks through how an AI-style workflow can inspect the data, choose preprocessing actions, and apply them in a structured way instead of relying on a fixed manual pipeline.

The embedded notebook below is added using the same Jupyter blog-post pattern as the Fed dot plot post.

{::nomarkdown}
{% assign jupyter_path = "assets/jupyter/agentic_preprocessing_pd.ipynb" | relative_url %}
{% capture notebook_exists %}{% file_exists assets/jupyter/agentic_preprocessing_pd.ipynb %}{% endcapture %}
{% if notebook_exists == "true" %}
{% jupyter_notebook jupyter_path %}
{% else %}

<p>Sorry, the notebook you are looking for does not exist.</p>
{% endif %}
{:/nomarkdown}
