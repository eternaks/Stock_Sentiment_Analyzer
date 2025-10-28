# Stock Sentiment Analyzer

*Aspect-Based Sentiment Analysis of Reddit Stock Discussions using DeBERTa, PyABSA, and AWS*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20RDS-orange)
![MySQL](https://img.shields.io/badge/Database-MySQL-lightgrey)
![Model](https://img.shields.io/badge/Model-DeBERTa-green)

---

## Overview

**Stock Sentiment Analyzer** is an end-to-end pipeline for performing **aspect-based sentiment analysis (ABSA)** on Reddit stock discussions.  
It fine-tunes a **DeBERTa** model using **PyABSA** to identify sentiment polarity toward specific stocks, then automatically collects and analyzes new posts daily using an AWS-hosted infrastructure.

## Objective & Results

In this project, I aimed to empirically test the idea that stock prices are directly correlated to the public's perception of said stock. This yielded limiting success, as while the stock picks that were informed by the model returned an average yield of 10% every week, I only did this for roughly two months. It should be noted that this was when the market was already on a bull run, so further testing is needed to fully deduce the performance of this model.

## Model Training Information

The model was trained on a sample size of about 3600 posts and yieled F1 scores of 0.7 for aspect-polarity classification and 0.894 for aspect-term extraction on a split of 3300 - 300 for training and test data.

## Installation & Setup

The way the project is set up will require an AWS EC2 and RDS instance.
If you want to run everything locally then you can simply just modify the code in data_pipeline/database.py to accommodate that.
Project was also built in an Ubuntu 22.04 environment.

### 1. Clone the repository
```bash
git clone git@github.com:eternaks/stock_predictor.git
cd stock_predictor
```

### 2. Create a Virtual Environment
macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows
```bash
python -m venv venv
venv/Scripts/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.text
```

### 4. Create reddit agent and aws ec2 and rds instances
Here are useful links to create a reddit agent:
https://praw.readthedocs.io/en/stable/getting_started/authentication.html

https://old.reddit.com/prefs/apps/

The ec2 instance I used was a t3 small and I used a mySQL RDS instance.

Note that the t3 small will not have enough memory to run the model, so you should create more virtual memory via swap file.

Make sure you add the AWS cert to data_pipeline/certs as well.

The MySQL structure should be as follows

database name = data

table name = predictions

table columns = int index, int amt, string ticker, float Positive, float Neutral, float Negative


### 4. Set up environment variables
Create a .env file in root with the following variables
```bash
client_id=your_client_id
client_secret=your_client_secret
user_agent=your_user_agent
db_endpoint=your_db_endpoint
db_password=your_db_password
```

### 5. Test the installation
You can run the entire pipeline by executing data_pipeline/data_collection.py

You can collect historical posts by executing data_collection/api_call.py

To view the results, execute data_pipeline/showresults.py


## Credit

This project uses yangheng95's PyABSA framework to perform sentiment analysis.

His framework can be found here: https://github.com/yangheng95/PyABSA and his paper's doi here: 10.1145/3583780.3614752
