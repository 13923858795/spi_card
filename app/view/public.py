# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import os, time, json
import flask_excel as excel
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify
)
from flask_login import login_required, login_user, logout_user

from app.extensions import login_manager
from app.forms.public import LoginForm, FileForm, CardForm
from app.forms.user import RegisterForm
from app.models.users import User
from app.models.cards import Cards
from app.utils import flash_errors
from app.settings import STATIC_PATH

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load view by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():

    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new view."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
'jpg'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@blueprint.route('/image', methods=['GET', 'POST'])
def image():

    form = FileForm()
    if request.method == 'POST':
        img = form.img.data
        path = STATIC_PATH + "/photo/"
        if not os.path.exists(path):
            os.makedirs(path)

        if form.validate_on_submit():
            file_name = f"{int(time.time())}.{img.filename.rsplit('.', 1)[1]}"
            file_path = path + file_name
            img.save(file_path)
            Cards.create(image=file_name, intent=form.intent.data, company_url=form.company_url.data)
            flash("上传成功", "success")
            return render_template('public/img_update.html', form=form)
        else:
            flash_errors(form)
            return render_template('public/img_update.html', form=form)

        # err = None
        # if not img or img == '':
        #     err = "文件不能为空"
        # elif not allowed_file(img.filename):
        #     err = "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"
        # if err:
        #     flash(err, 'error')
        #     return render_template('public/img_update.html', form=form)

    return render_template('public/img_update.html', form=form)


@blueprint.route('/add', methods=['GET', 'POST'])
def add():

    form = CardForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            date = json.dumps({'addr': [form.addr.data], 'company': [form.company.data],
                               'department': [form.department.data], 'email': [form.email.data],
                               'name': [form.name.data], "title": [form.title.data],
                               'tel_cell': [form.tel_cell.data]}, ensure_ascii=False)

            Cards.create(date=date, intent=form.intent.data, company_url=form.company_url.data, is_ok=True)

            flash("上传成功", "success")
        else:
            flash_errors(form)

        return render_template('public/add.html', form=form)
    return render_template('public/add.html', form=form)


@blueprint.route('/lists', methods=['GET', 'POST'])
def lists():
    models = Cards.query.filter_by().all()

    return render_template('public/lists.html', models=models)


@blueprint.route('/down', methods=['GET'])
def down():
    date = [[
            "姓名", "电话", "邮箱", "部门", "职位", "公司名称", "公司地址", "公司网址", "意向产品",
        ]]

    for model in Cards.query.filter_by(is_ok=True).all():

        info = json.loads(model.date)

        _d = [info['name'], info['tel_cell'], info['email'], info['department'], info['title'],
              info['company'], info['addr'], model.company_url, model.intent]

        date.append([",".join(i) if isinstance(i, list) else i for i in _d])

    return excel.make_response_from_array(date, 'xlsx', file_name='adj')