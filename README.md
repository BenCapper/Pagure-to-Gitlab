# Pagure to Gitlab

Pagure example: https://pagure.io/pagure-to-gitlab/issues <br>
Gitlab example: https://gitlab.com/BenCapper/pagure-to-gitlab/-/issues

This script takes issue data from a specified Pagure.io project and uses it to replicate the issues in a Gitlab project.

The Gitlab project must be a fresh project with no prior issues created.

Just fill in the following fields and run the script:

~~~
pagure_project_name = "<ENTER PAGURE PROJECT NAME HERE>"  # Enter Pagure project name
~~~

~~~
header = {  # Enter Pagure personal access token
    "Authorization": "token <ENTER TOKEN HERE>"
}
~~~

~~~
server = gitlab.Gitlab(  # Enter Gitlab personal access token
    "https://gitlab.com/", private_token="<ENTER TOKEN HERE>", api_version=4
)
~~~

~~~
project = server.projects.get("<ENTER GITLAB PROJECT ID HERE>")  # Enter Gitlab project id
~~~
