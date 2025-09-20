---
layout: page
title: NCUA Call Report 
description: Data exploration and analysis of U.S. credit union call reports
img: assets/img/12.jpg
importance: 1
category: work
related_publications: true
---

The **NCUA Call Report** project is a data exploration and analysis toolkit for U.S. credit union call report data published by the [National Credit Union Administration](https://ncua.gov/).

The **National Credit Union Administration (NCUA)** is an independent federal agency responsible for regulating and supervising federal credit unions across the United States. Its mission is to protect credit union members, ensure the safety and soundness of the credit union system, and maintain public confidence in these financial institutions.  

To support this mission, the NCUA requires all federally insured credit unions to submit detailed **quarterly call reports**. These reports provide a comprehensive look into the financial and operational condition of each institution. They include balance sheet data, income and expense statements, loan portfolios, membership growth, delinquency rates, and key performance ratios. By making this information publicly available, the NCUA enhances transparency, strengthens regulatory oversight, and gives researchers and practitioners the ability to analyze trends across the credit union industry.  

This project takes that open data and turns it into an opportunity for deeper analysis. My goal is to **extract and structure the quarterly datasets**, clean and organize the information, and then explore patterns across institutions and over time. I plan to build **dynamic dashboards** that make it easier to visualize how credit unions are performing, how their loan portfolios are evolving, and where risks may be emerging.  

Looking further ahead, I want to move beyond descriptive analysis into **predictive modeling**. By combining call report data with broader **macroeconomic indicators**—such as unemployment rates, interest rate trends, and GDP growth—I aim to study how external economic conditions influence credit union performance. For example, I would like to develop models that can forecast **loan delinquencies** under different economic scenarios, giving insights into how resilient the credit union system is in the face of changing conditions.  

In short, this project is about bridging regulatory reporting with modern data analysis techniques. It starts with cleaning and organizing the raw data, expands into interactive visualizations for exploration, and ultimately aspires to deliver predictive tools that can inform both researchers and practitioners in the financial sector.  

👉 Source code is available here:  
[github.com/LupaLupa10/ncua-call-report](https://github.com/LupaLupa10/ncua-call-report)


---

## Features
- Collects and processes **credit union financial data** from NCUA call reports.  
- Provides **Python scripts and utilities** for cleaning, aggregating, and analyzing the datasets.  
- Designed to support **research, compliance, and financial risk analysis**.  

---

## Example usage
```bash
git clone https://github.com/LupaLupa10/ncua-call-report.git
cd ncua-call-report
pip install -r requirements.txt
python analyze_reports.py --year 2023


    ---
    layout: page
    title: project
    description: a project with a background image
    img: /assets/img/12.jpg
    ---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/1.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/3.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Caption photos easily. On the left, a road goes through a tunnel. Middle, leaves artistically fall in a hipster photoshoot. Right, in another hipster photoshoot, a lumberjack grasps a handful of pine needles.
</div>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/5.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    This image can also have a caption. It's like magic.
</div>

You can also put regular text between your rows of images, even citations {% cite einstein1950meaning %}.
Say you wanted to write a bit about your project before you posted the rest of the images.
You describe how you toiled, sweated, _bled_ for your project, and then... you reveal its glory in the next row of images.

<div class="row justify-content-sm-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/6.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/11.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    You can also have artistically styled 2/3 + 1/3 images, like these.
</div>

The code is simple.
Just wrap your images with `<div class="col-sm">` and place them inside `<div class="row">` (read more about the <a href="https://getbootstrap.com/docs/4.4/layout/grid/">Bootstrap Grid</a> system).
To make images responsive, add `img-fluid` class to each; for rounded corners and shadows use `rounded` and `z-depth-1` classes.
Here's the code for the last row of images above:

{% raw %}

```html
<div class="row justify-content-sm-center">
  <div class="col-sm-8 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/6.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
  </div>
  <div class="col-sm-4 mt-3 mt-md-0">
    {% include figure.liquid path="assets/img/11    .jpg" title="example image" class="img-fluid rounded z-depth-1" %}
  </div>
</div>
```

{% endraw %}
