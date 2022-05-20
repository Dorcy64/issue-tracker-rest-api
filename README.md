# Introduction
Part 1: Algorithm to get minimum connections needed to connect all the points: [solution](https://github.com/Dorcy64/interviews/blob/main/get-minimum-connections/solution.py).

Part 2: Coding assessment bellow.

I was tasked to build an api that has all these necessary functions and features.

- Create a bug. A bug should have a title, a body, and a status (resolved/unresolved).
- Edit a bug.
- Delete a bug.
- View all bugs.
- View a specific bug.
- Add a comment to a bug. A comment should have a title, and a body.
- Delete a comment from a bug.
- Mark a bug as "resolved".
- Mark a bug as "unresolved".
- View all bugs marked as "resolved".
- Assign the bug to a user. A user is identified by its ID.

## Method

To start the tech stack I chose for this project was Flask, due to its fast development speed. The SQL database I chose for this was sqlite, for the same reason I chose flask (fast to develop and test).

I got started by creating a `model.py` to host all the database info, then created `util_db.py` to help speed up database developments, and host all the saving, deleting, time, which all databases typically need. Then I created `util_api.py` to host render_json which is the output function I typically use everywhere in apis.

## Running

These APIs don't require any api keys since they are intended for development only and not production. If you want to skip all these steps just install [pycharm]("https://www.jetbrains.com/pycharm/") and open this directory in pycharm.

Use pip3 to install all the required dependencies on Mac or Linux.
```sh
python -m pip install --upgrade pip
pip3 install -r requirements.txt
```

Run the flask app on your machine.
```sh
export FLASK_APP=app
flask run
```

## Routes

Since there are no api keys just open a tool called postman or similar and test the APIs.

```http
POST /view-all-bugs
```

```http
POST /view-all-resolved-bugs
```
```http
POST /create-bug
```

| Parameter | Type | Description                               |
|:----------| :--- |:------------------------------------------|
| `title`   | `string` | **Required**. The new bug's title         |
| `body`    | `string` | **Required**. The new bug's body          |
| `assigned_user`    | `string` | **Optional**. The new bug's assigned user |


```http
POST  /view-bug/<bug_id>
```

Make sure you include the bug id in the route, it will return all the bug comments, and also include the bug details.

```http
POST /edit-bug/<bug_id>
```

Make sure you include the bug id in the route

| Parameter | Type | Description                                  |
|:----------| :--- |:---------------------------------------------|
| `title`   | `string` | **Required**. The edited bug's title         |
| `body`    | `string` | **Required**. The edited bug's body          |
| `assigned_user`    | `string` | **Optional**. The edited bug's assigned user |


```http
POST /delete-bug
```

| Parameter | Type  | Description                                        |
| :--- |:------|:---------------------------------------------------|
| `bug_id` | `int` | **Required**. The id of the bug you want to delete |


```http
POST  /change-bug-status/<bug_id>
```

Make sure you include the bug id in the route, calling this route will toggle resolved/unresolved, and return the serialized bug.


```http
POST  /post-comment/<bug_id>
```

Make sure you include the bug id of the bug you want to comment on in the route.

| Parameter | Type     | Description                                             |
|:----------|:---------|:--------------------------------------------------------|
| `title`   | `string` | **Required**. The title of the comment you want to add  |
| `body`    | `string` | **Required**. The comment of the comment you want to add |


```http
POST  /delete-comment/<bug_id>
```

Make sure you include the bug id of the bug you want to delete in the route.


## Responses

Many API endpoints return the JSON representation of the resources created or edited. If a valid request is submitted to retrieve all bugs, this will return a JSON response in the following format:

```javascript
[
    {
        "assigned_user": null,
        "body": "Let's see what is actually going on here",
        "id": 2,
        "status": "unresolved",
        "title": "Bug 2 UI Changes"
    },
    {
        "assigned_user": "dorcy",
        "body": "Bug 1 is a feauture",
        "id": 1,
        "status": "resolved",
        "title": "Bug 1 is a test"
    }
]
```


## Status Codes

Issue Tracker returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |
