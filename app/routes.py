from app import app, bcrypt, login_manager
from flask import request, render_template
from flask_login import login_user, current_user, logout_user, login_required

from forms import SearchForm
import services
import database

def clean_text(data: str):
    if isinstance(data, str) and data != "":
        data = data.strip()
        data = data.lower()
        count = 0
        while data[count] == '0':
            count += 1
        data = data[count:]
    return data


@app.route('/', methods=['POST', 'GET'])
def home():
    ALARM_LIST_PAGE = "./home/alarmlist.html"
    HOME_PAGE = "./home/search.html"
    TITLE = "Alarm Search"
    form = SearchForm()
    form.fill_model(all=True)
    form.fill_module(only_all=True)

    if request.method == 'POST':
        data = {'vendor': int(form.vendor.data),
                'model': clean_text(form.model.data),
                'module': clean_text(form.module.data),
                'alarm_id': clean_text(form.alarm_id.data)}  # Need to clean the data

        if data['model'] == 'all' or data['module'] == 'all' or data['alarm_id'] == '':
            alarms = services.alarm_list_controller(database.Alarms(), data)
            return render_template(ALARM_LIST_PAGE, form=form, alarms=alarms)

        # posts = Posts(manager)
        # data = clean_form(form)
        # posts.process_dict(data)
        # posts.fill()
        #
        # if not current_user.is_anonymous:
        #     add_post_form = AddPostForm()
        #     add_part_form = AddPartForm()
        #     add_post_form.idalarm.data = posts.idalarm
        #     add_post_form.user_id.data = current_user.id
        #     add_part_form.idalarm.data = posts.idalarm
        #     return render_template(HOME_PAGE, form=form, title=TITLE, posts=posts, addPostForm=add_post_form, addPartForm=add_part_form)
        #
        # return render_template(HOME_PAGE, form=form, title=TITLE, posts=posts)

    return render_template(HOME_PAGE, form=form, title="Alarm Search")
