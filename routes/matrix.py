from flask import Blueprint, render_template, request, current_app

matrix = Blueprint("matrix", __name__,
                   template_folder="../templates", static_folder="../static")


@matrix.route("/matrix")
def matrix_page():
    context = request.args.get("context")
    active_only = request.args.get("active") == "true"

    query = {}
    if context and context.lower() != "all":
        query["context"] = context
    if active_only:
        query["done"] = False

    todos = list(current_app.db.todos.find(query))  # type: ignore
    return render_template("matrix.html", tasks=todos, context=context, active=active_only, title="Eisenhower Matrix")


@matrix.route("/matrix/move/<task_id>", methods=["POST"])
def move_task(task_id):
    data = request.get_json()
    new_category = data.get("category")
    if new_category:
        current_app.db.todos.update_one(  # type: ignore
            {"_id": task_id},
            {"$set": {"category": new_category}}
        )
    return "", 204
