import os
import time
import gitlab
import datetime
import requests


tag_list = []
done_label_list = []
done_issue_list = []
issue_list = []

session = requests.Session()
pagure_project_name = "ENTER_PAGURE_PROJECT_NAME"  # Enter Pagure project name
header = {  # Enter Pagure personal access token
    "Authorization": "token ENTER_PAGURE_PERSONAL_ACCESS_TOKEN"
}
issue_url = "https://pagure.io/api/0/" + pagure_project_name + "/issues?status=all&per_page=100"
tag_url = "https://pagure.io/api/0/" + pagure_project_name + "/tags"
issue_response = requests.get(issue_url, headers=header)
tags_response = requests.get(tag_url, headers=header)
tag_list = tags_response.json()["tags"]
pages = session.get(issue_url).json()['pagination']['pages']
issue_list = issue_response.json()["issues"]
for p in range(2, pages + 1):
    page_of_issues_url = "https://pagure.io/api/0/" + pagure_project_name + "/issues?status=all&per_page=100" + "&page=" + str(p)
    page = session.get(page_of_issues_url).json()['issues']
    for i in page:
        issue_list.append(i)

server = gitlab.Gitlab(  # Enter Gitlab personal access token
    "https://gitlab.com/", private_token="ENTER_GITLAB_PERSONAL_ACCESS_TOKEN", api_version=4
)
project = server.projects.get(ENTER_GITLAB_PROJECT_ID_(INT))  # Enter Gitlab project id
project_name = project.attributes["name"]

if os.path.exists("done_labels.temp"):
    open_temp_label = open("done_labels.temp", "r")
    read_temp_label = open_temp_label.read()
    done_label_list = read_temp_label.splitlines()
else:
    os.mknod("done_labels.temp")

# Keep track of completed tags
for tag in tag_list:
    tag_dict = {}
    tag_url = "https://pagure.io/api/0/" + pagure_project_name + "/tag/" + tag
    single_tag_response = requests.get(tag_url, headers=header)
    single_tag = single_tag_response.json()
    if single_tag["tag"] in done_label_list:
        print("Label already exists, skipping...")
    else:
        tag_dict["name"] = single_tag["tag"]
        tag_dict["color"] = single_tag["tag_color"]
        tag_dict["description"] = single_tag["tag_description"]
        tag_resp = project.labels.create(
            {"name": tag_dict["name"], "color": tag_dict["color"]}
        )
        tag_resp.description = single_tag["tag_description"]
        tag_resp.save()
        done_label_list.append(single_tag["tag"])
        open_label_temp = open("done_labels.temp", "a")
        open_label_temp.write(single_tag["tag"] + "\n")

# Keep track of completed issues
if os.path.exists("done_issues.temp"):
    open_temp = open("done_issues.temp", "r")
    read_temp = open_temp.read()
    done_issue_list = read_temp.splitlines()
else:
    os.mknod("done_issues.temp")


for issue in issue_list:
    issue_data = {}
    notes = []
    issue_data["id"] = issue["id"]
    issue_data["user"] = issue["user"]["name"]
    issue_data["title"] = issue["title"]
    if str(issue_data["id"]) in done_issue_list:
        print("Issue already exists, skipping...")
    else:
        done_issue_list.append(issue_data["id"])
        open_temp = open("done_issues.temp", "a")
        description = issue["content"]
        issue_data["confidential"] = issue["private"]
        issue_data["state"] = issue["status"]
        if issue_data["state"] == "Closed":
            issue_data["state"] = "close"
        else:
            issue_data["state"] = "reopen"
        issue_data["labels"] = issue["tags"]
        issue_created_secs = issue["date_created"]
        dt = datetime.datetime.fromtimestamp(int(issue_created_secs))
        d = "{:%Y-%m-%d %H:%M:%S}".format(dt)
        issue_data["created_at"] = d
        issue_data["description"] = (
            "On "
            + str(d[:10])
            + " at "
            + str(d[11:])
            + ", **"
            + issue["user"]["name"]
            + "** said:\n\n"
            + description
        )
        create = project.issues.create(issue_data)
        open_temp.write(str(issue_data["id"]) + "\n")
        for comment in issue["comments"]:
            comment_data = {}
            comment_data["name"] = comment["user"]["name"]
            comment_data["comment"] = comment["comment"]
            date_secs = comment["date_created"]
            time = datetime.datetime.fromtimestamp(int(date_secs))
            t = "{:%Y-%m-%d %H:%M:%S}".format(time)
            comment_data["created_at"] = t
            notes.append(comment_data)
        issue_data["issue_comments"] = notes
        for note in notes:
            if "**Metadata Update" in note["comment"]:  # Delete this if conditional
                pass                                    # and move else block into the notes loop
            else:                                       # to include metadata comments            
                comment_body = (
                    "On "
                    + note["created_at"][:10]
                    + " at "
                    + note["created_at"][:11]
                    + ", **"
                    + note["name"]
                    + "**"
                    + " said:\n\n"
                    + note["comment"]
                )
                resp = create.notes.create({"body": comment_body})

        create.state_event = issue_data["state"]
        create.save()
        print(
            "ISSUE DATA: \n",
            "ID:         ",
            issue_data["id"],
            "\n",
            "USER:       ",
            issue_data["user"],
            "\n",
            "TITLE:      ",
            issue_data["title"],
            "\n",
            "CONTENT:    ",
            issue_data["description"],
            "\n",
            "PRIVATE:    ",
            issue_data["confidential"],
            "\n",
            "STATE:      ",
            issue_data["state"],
            "\n",
            "TAGS:       ",
            issue_data["labels"],
            "\n",
            "CREATED AT: ",
            issue_data["created_at"],
            "\n",
            "COMMENTS:   ",
            issue_data["issue_comments"],
            "\n\n",
        )
