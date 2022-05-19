from util_api import render_json
from models import Bug, BugComment
from app import db
from flask import Blueprint, request

api = Blueprint('api', __name__)


@api.route('/view-all-bugs', methods=["POST"])
def view_all_bugs():
    """
    :returns: status code and all the serialized bugs in a list.
    """
    bugs = db.session.query(Bug).order_by(Bug.created_on.desc()).all()
    return render_json(200, [b.serialize for b in bugs])


@api.route('/view-all-resolved-bugs', methods=["POST"])
def view_all_resolved():
    """
    :returns: status code and all the serialized bugs which are marked as resolved in chronological order.
    """
    bugs = db.session.query(Bug).filter(Bug.status == "resolved").order_by(Bug.created_on.desc()).all()
    return render_json(200, [b.serialize for b in bugs])


@api.route("/create-bug", methods=["POST"])
def create_bug():
    """
    This route takes title, body, assigned_user(optional) parameters and by default status is unresolved
    :returns: status code and message when the bug is successfully created.
    """

    title = request.args.get('title', type=str)
    body = request.args.get('body', type=str)
    assigned_user = request.args.get("assigned_user", type=str)
    if title is None or title == "" or body is None or body == "":
        return render_json(400, "Bug body or title cannot be empty")

    new_bug = Bug(title=title, body=body, assigned_user=assigned_user)
    new_bug.save()

    return render_json(201, new_bug.serialize)


@api.route("/view-bug/<int:bug_id>", methods=["POST"])
def view_bug(bug_id):
    """
    :param bug_id: the bug id of the bug you want to view.
    :returns: status code, serialized bug info (details), and serialized comments (comments).
    """
    bug = Bug.query.get(bug_id)
    if bug is None:
        return render_json(400, "The bug you want to view is missing or doesn't exist")

    return render_json(200, {
        "details": bug.serialize,
        "comments": [c.serialize for c in bug.bug_comments]
    })


@api.route('/edit-bug/<int:bug_id>', methods=["POST"])
def edit_bug(bug_id):
    """
    This route takes bug_id, title, body, assigned_user parameter.
    :returns: status code and message when the bug is successfully edited.
    """

    bug = Bug.query.get(bug_id)
    if bug is None:
        return render_json(400, "The bug you want to edit is missing or doesn't exist")

    title = request.args.get('title', type=str)
    body = request.args.get('body', type=str)
    if title is None or title == "" or body is None or body == "":
        return render_json(400, "Bug body or title cannot be empty")

    bug.title = title
    bug.body = body
    bug.assigned_user = request.args.get('assigned_user', type=str)
    bug.save()

    return render_json(200, "The bug was successfully edited")


@api.route("/delete-bug", methods=["POST"])
def delete_bug():
    """
    This route takes bug_id parameter.
    :returns: status code, and message when the bug is successfully edited.
    """

    try:
        bug_id = request.args.get('bug_id', type=int)
    except ValueError or TypeError:
        return render_json(400, "Invalid bug id format or is missing")

    bug = Bug.query.get(bug_id)
    if bug is None:
        return render_json(400, "The bug you want to delete is missing or doesn't exist")

    bug.delete()
    return render_json(200, "Successfully deleted the bug")


@api.route("/change-bug-status/<int:bug_id>", methods=["POST"])
def change_bug_status(bug_id):
    """
    :param bug_id: the bug id of the bug you want to view.
    :returns: status code and serialized bug info if changing status was successful.
    """
    bug = Bug.query.get(bug_id)
    if bug is None:
        return render_json(400, "The bug you want to change status is missing or doesn't exist")

    bug.change_status()
    return render_json(200, bug.serialize)


@api.route("/post-comment/<int:bug_id>", methods=["POST"])
def post_comment(bug_id):
    """
    This route takes bug_id, title, and body parameters.
    :returns: status code and serialized comment info if comment was successful.
    """

    bug_object = Bug.query.get(bug_id)
    if bug_object is None:
        return render_json(400, "The bug you want to comment on is missing or doesn't exist")

    title = request.args.get('title', type=str)
    body = request.args.get('body', type=str)
    if title is None or title == "" or body is None or body == "":
        return render_json(400, "Comment body or title cannot be empty")

    new_comment = BugComment(title=title, body=body, bug_id=bug_id)
    new_comment.save()

    return render_json(201, new_comment.serialize)


@api.route("/delete-comment/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    """
    This route takes comment_id parameter.
    :returns: 200 status code when the deletion was successful.
    """
    comment = BugComment.query.get(comment_id)
    if comment is None:
        return render_json(400, "The comment you requested to delete wasn't found or is missing")

    comment.delete()

    return render_json(200, "Successfully deleted the comment")
