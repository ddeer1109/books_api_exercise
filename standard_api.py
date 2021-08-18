import db_populator
from app import app
from flask import render_template, request, redirect

from data_management.BooksApiRequest import BooksApiRequest
from data_management.BooksDataManager import BooksDataManager

from models.Constants import Status
from models.FormDataValidator import FormDataValidator
from util import util


@app.route("/")
def get_all_records():

    records = BooksDataManager.get_by_filters(
        title=request.args.get('title'),
        author=request.args.get('author'),
        language=request.args.get('language'),
        published_from=request.args.get('from'),
        published_to=request.args.get('to'),
    )
    return render_template("index.html", books=records)


@app.route("/add-entry")
def add_entry_form():
    return render_template("add-entry.html")


@app.route("/add-entry", methods=['POST'])
def add_entry():

    validator = FormDataValidator(dict(request.form))

    if validator.is_data_valid():
        BooksDataManager.add(dict(request.form))
        return redirect("/")
    else:
        return render_template("add-entry.html",
                               invalid_fields=validator.invalid_fields_info)


@app.route("/edit/<book_id>")
def view_edit_entry(book_id):
    book = BooksDataManager.get_by_id(book_id)
    return render_template("update-entry.html", book=book)


@app.route("/edit/<book_id>", methods=["POST"])
def edit_entry(book_id):

    validator = FormDataValidator(dict(request.form), update_data=True)

    if validator.is_data_valid():
        status = BooksDataManager.update(book_id, dict(request.form))

        if status == Status.OK:
            return redirect("/")

    return render_template("update-entry.html",
                           book=BooksDataManager.get_by_id(book_id),
                           invalid_fields=validator.invalid_fields_info)


@app.route("/import")
def books_api_import_view():
    return render_template("import-from-api.html")


@app.route("/import", methods=["POST"])
def books_api_import_post():
    passed_attributes = util.filter_out_empty_dict_entries((dict(request.form)))

    request_api = BooksApiRequest(params_dict=passed_attributes)
    request_api.send_request(request_options={"maxResults": 40})
    books = request_api.get_mapped_results()

    BooksDataManager.add_entries(books)
    return redirect("/")


@app.route("/books")
@util.json_response
def api_get():

    query_result = BooksDataManager.get_by_filters(
        title=request.args.get('title'),
        author=request.args.get('author'),
        language=request.args.get('language'),
        published_from=request.args.get('from'),
        published_to=request.args.get('to'),
    )

    return {"items_count": len(query_result), "results": [i.serialize for i in query_result]}


@app.route("/books/<book_id>")
@util.json_response
def api_get_by_id(book_id):

    query_result = BooksDataManager.get_by_id(id=book_id)
    return query_result.serialize


@app.route("/reset-db/<pin>")
def reset_db(pin):
    if pin == "1010":
        db_populator.populate()
    return redirect("/")

