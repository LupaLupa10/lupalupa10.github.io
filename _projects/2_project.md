---
layout: page
title: Freddie Mac
description: A Python toolchain to download, clean, and analyze Freddie Mac Single-Family Loan-Level data, with an auto-generated HTML report and (WIP) Bayesian modeling.
img: assets/img/3.jpg
importance: 2
category: work
related_publications: true
---

Working with Freddie Mac’s Single-Family Loan-Level {% cite freddiemac_dataset %} dataset started as an experiment to make a dense, institutional resource more accessible to independent researchers and hobbyists. The data, which spans millions of mortgages over decades, is publicly available but fragmented across quarterly ZIP archives that are tedious to manage.

I built a Python pipeline that automates downloading, cleaning, and merging the origination and performance files, then generates a lightweight HTML report with trends like FICO distributions, delinquency rates, and prepayment behavior. Along the way I leaned heavily on reproducibility — Poetry for environments, YAML configs for runs, and Jinja2 for templating — so anyone can replicate or extend the workflow. For me, this project is as much about **democratizing access to housing finance data** as it is about coding, and it’s already opened the door to deeper analysis like Bayesian modeling of loan defaults, which I’ll continue to explore.
