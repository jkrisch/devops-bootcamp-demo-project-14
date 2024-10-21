# Automation with boto3

## Getting familiar with boto
Some Notes:

### client vs resource

Client

* provides a more low-level API
* provides a one-to-one mapping to the underlying HTTP API operations (explicitly speficy exactly which resource you want to connect to for every single function)

Resource

* provides resource objects to access attributes and performs actions
* basically a repo around client
* high-level and object oriented
    * a creation of a resource returns an object with which we can then do further modifications


## Terraform vs Python

* Terraform manages state of the infrastructure.
* So when we create a resource(e.g vpc) using Terraform, terraform will keep a state and knows what the current state in my cloud is.
* It can decide if a specific resource already exists or not.
* Terraform is also idempotent.

* Python doesn't have a state
* Python is not idempotent


### Use cases using boto3

* With boto3 we can do more things
* more complex logic possible (conditionals etc.)
* as a full-fledged programming language Python is way more powerful than terraform
* boto is an aws library (more possibilities compared to aws provider for tf)
* Monitoring/Health-Checks, Backups, Scheduled Tasks etc.
* Add Web Interface to the python projects and include the respective tasks(backups) or show monitoring etc.



## Demo Project Health Check: EC2 Status
See [python script](./main.py)
All resources were created using terraform.
[See](./terraform/main.tf)
