# Pagure to Gitlab

Pagure example: https://pagure.io/pagure-to-gitlab/issues <br>
Gitlab example: https://gitlab.com/BenCapper/pagure-to-gitlab-example/-/issues

This script takes issue data from a specified Pagure.io project and uses it to replicate the issues in a Gitlab project.

The Gitlab project must be a fresh project with no prior issues created.

Just fill in the following fields and run the script:


~~~
pagure_project_name = "ENTER_PAGURE_PROJECT_NAME"  # Enter Pagure project name
~~~

~~~
header = {  # Enter Pagure personal access token
    "Authorization": "token ENTER_PAGURE_PERSONAL_ACCESS_TOKEN"
}
~~~

~~~
server = gitlab.Gitlab(  # Enter Gitlab personal access token
    "https://gitlab.com/", private_token="ENTER_GITLAB_PERSONAL_ACCESS_TOKEN", api_version=4
)
~~~

~~~
project = server.projects.get(ENTER_GITLAB_PROJECT_ID_(INT))  # Enter Gitlab project id
~~~
