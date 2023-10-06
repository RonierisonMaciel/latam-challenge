# Machine Learning & Large Language Models Engineering Challenge: A Solution

## Introduction

This solution for the engineering challenge is available on a public GitHub repository and is hosted using Google Cloud's Cloud Run service. You can access the repository by clicking [here](https://github.com/RonierisonMaciel/latam-challenge).

### Understanding the Solution

- We opted for the Logistic Regression model for several reasons:
  - To conclude, although XGBoost may have shown slightly better metrics in its specific comparison, it is not just numerical performance that determines the choice of model. 
  - Often the decision is influenced by practical considerations, business requirements, ease of interpretation, and maintainability. In the scenario we presented, logistic regression may be “better” if we consider all these factors together, even if XGBoost has a slightly higher AUC.
  - In production environments, simplicity and maintainability can be crucial. If logistic regression meets the needs of the problem with adequate performance, it may be easier to implement, monitor, and readjust as needed.

## How to Utilize

If you're looking to leverage this solution, you have a couple of options:
- Set it up on your local machine:
  - Execute a git clone of the main branch of the repository.
  - Install necessary dependencies using:
  ```bash
    pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt
    ```
  - Launch the \_\_init__.py file present in the challenge directory.
- Alternatively, access the solution directly through the hosted service [here](https://latam-challenge-ljbxkwvxmq-uc.a.run.app/).

## Guide to API
If you're interested in understanding the API further:
- On a local setup: After running the application as mentioned previously, navigate to http://0.0.00:8080/docs.
- On the hosted platform, Simply head to https://latam-challenge-ljbxkwvxmq-uc.a.run.app//docs.
