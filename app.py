# -*- coding: utf-8 -*-

import postgresql
import flask
import json
import psycopg2

app = flask.Flask(__name__)

# disables JSON pretty-printing in flask.jsonify
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

def db_conn():

    return psycopg2.connect('dbname=d93m8auhdgpms4 user=ybdvnnlbssjlmh password=28593faeb443003364b372b5973a0fd4f7243d54320ccd1636320ad2cf77e004 host=ec2-54-227-245-146.compute-1.amazonaws.com')



def to_json(data):
    return json.dumps(data, ensure_ascii=False) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def theme_validate():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    for field_name in ['title', 'url']:
        if type(json.get(field_name)) is not str:
            errors.append(
                "Field '{}' is missing or is not a string".format(
          field_name))

    return (json, errors)


def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code


@app.route('/')
def root():
    return flask.redirect('/api/1.0/posts')

# e.g. failed to parse json
@app.errorhandler(400)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(404)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(405)
def page_not_found(e):
    return resp(405, {})


@app.route('/api/1.0/posts', methods=['GET'])
def get_themes():
    with db_conn() as db:
        cur =db.cursor()
        cur.execute("SELECT id, post_text, community, imageurl FROM posts;")
        tuples=cur.fetchall()
        posts = []
        if tuples is None:
            return '404'
        else:
            for (id, post_text, community, imageurl) in tuples:
                posts.append({"id":id, "post_text": post_text, "community": community
                              ,"imageurl":imageurl})
            return resp(20, {"posts": posts})

"""
@app.route('/api/1.0/themes', methods=['POST'])
def post_post():
    (json, errors) = post_validate()
    if errors:  # list is not empty
        return resp(20, {"errors": errors})

    with db_conn() as db:
        insert = db.prepare(
            "INSERT INTO themes (title, url) VALUES ($1, $2) " +
            "RETURNING id")
        [(theme_id,)] = insert(json['title'], json['url'])
        return resp(200, {"theme_id": theme_id})


@app.route('/api/1.0/themes/<int:theme_id>', methods=['PUT'])
def put_theme(theme_id):
    (json, errors) = theme_validate()
    if errors:  # list is not empty
        return resp(400, {"errors": errors})

    with db_conn() as db:
        update = db.prepare(
            "UPDATE themes SET title = $2, url = $3 WHERE id = $1")
        (_, cnt) = update(theme_id, json['title'], json['url'])
        return resp(affected_num_to_code(cnt), {})


@app.route('/api/1.0/themes/<int:theme_id>', methods=['DELETE'])
def delete_theme(theme_id):
    with db_conn() as db:
        delete = db.prepare("DELETE FROM themes WHERE id = $1")
        (_, cnt) = delete(theme_id)
        return resp(affected_num_to_code(cnt), {})
"""
if __name__ == '__main__':
    app.debug = True  # enables auto reload during development
    app.run()