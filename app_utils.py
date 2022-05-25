from flask import render_template


def turbo_change_page(app, turbo, html_page, target_name):
    with app.app_context():
        turbo.push(turbo.replace(render_template(html_page), target_name))