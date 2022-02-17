from app import app
from flask import request, render_template



@app.route('/', methods=['POST', 'GET'])
def home():
    ALARM_LIST_PAGE = "./home/alarmlist.html"
    HOME_PAGE = "./home/search.html"
    TITLE = "Alarm Search"
    form = SearchForm()
    form.fill_model(all=True)
    form.fill_module(only_all=True)

    if request.method == 'POST':
        vendor = int(form.vendor.data)
        model = form.model.data
        module = form.module.data
        alarm_id = clean_text(form.alarm_id.data)

        if model == 'all' or module == 'all' or alarm_id == '':
            alarm = Alarms()
            alarm.fill(vendor=vendor, model=model, module=module, alarm_id=alarm_id)

            return render_template(ALARM_LIST_PAGE, form=form, alarms=alarm)

        posts = Posts(manager)
        data = clean_form(form)
        posts.process_dict(data)
        posts.fill()

        if not current_user.is_anonymous:
            add_post_form = AddPostForm()
            add_part_form = AddPartForm()
            add_post_form.idalarm.data = posts.idalarm
            add_post_form.user_id.data = current_user.id
            add_part_form.idalarm.data = posts.idalarm
            return render_template(HOME_PAGE, form=form, title=TITLE, posts=posts, addPostForm=add_post_form, addPartForm=add_part_form)

        return render_template(HOME_PAGE, form=form, title=TITLE, posts=posts)

    return render_template(HOME_PAGE, form=form, title="Alarm Search")
