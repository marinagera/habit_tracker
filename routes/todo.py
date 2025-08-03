from flask import Blueprint, render_template, request, redirect, url_for, current_app
import uuid

todo = Blueprint("todo", __name__,
                 template_folder="../templates", static_folder="../static")


@todo.route("/todo", methods=["GET", "POST"])
def todo_page():

    if request.method == "POST":
        task = request.form.get("task")
        context = request.form.get("context")
        if task:
            current_app.db.todos.insert_one({  # type: ignore[attr-defined]
                "_id": uuid.uuid4().hex,
                "task": task,
                "done": False,
                "context": context or "personal",
                "category": "not_urgent_not_important"
            })
        return redirect(url_for(".todo_page"))

    context = request.args.get("context")
    only_active = request.args.get("active")

    query = {}
    if context and context.lower() != "all":
        query["context"] = context
    if only_active == "true":
        query["done"] = False

    tasks = list(current_app.db.todos.find(query))  # type: ignore
    return render_template("todo.html", tasks=tasks, title="ToDo List", context=context)


@todo.route("/todo/complete/<task_id>", methods=["POST"])
def complete_task(task_id):
    task = current_app.db.todos.find_one({"_id": task_id})  # type: ignore
    if task:
        current_app.db.todos.update_one(  # type: ignore
            {"_id": task_id}, {"$set": {"done": not task["done"]}})
    return redirect(url_for(".todo_page"))


@todo.route("/todo/delete/<task_id>", methods=["POST"])
def delete_task(task_id):
    current_app.db.todos.delete_one({"_id": task_id})  # type: ignore
    return redirect(url_for(".todo_page"))
