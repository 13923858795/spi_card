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
    jsonify,
    make_response, send_from_directory
)
from flask_login import login_required, login_user, logout_user, current_user

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
            redirect_url = request.args.get("next") or url_for("public.home")
            return redirect(redirect_url)
        else:
            flash_errors(form)

    # resp = render_template("public/home.html", form=form)
    # resp.set_cookie('lang', 'zh', max_age=7 * 24 * 3600)

    if current_user.is_authenticated:
        print(current_user.id)
        if current_user.office == '東南亞':
            lang = 'english'
        elif current_user.office == '台北':
            lang = 'ft'
        else:
            lang = 'zh'
    else:
        lang = 'zh'

    response = make_response(render_template("public/home.html", form=form))
    response.set_cookie('lang', lang)
    return response


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
            Cards.create(image=file_name, original_factory=form.original_factory.data,
                         remarks=form.remarks.data, own=current_user.id)
            flash("上传成功", "success")
            return render_template('public/img_update.html', form=form)
        else:
            flash_errors(form)
            return render_template('public/img_update.html', form=form)

    return render_template('public/img_update.html', form=form)


@blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = CardForm()
    if request.method == 'POST':

        if form.validate_on_submit():

            Cards.create(name=form.name.data, email=form.email.data,tel_cell=form.tel_cell.data,
                         department=form.department.data,
                         title=form.title.data, company=form.company.data, original_factory=form.original_factory.data,
                         remarks=form.remarks.data, is_analysis=True, own=current_user.id, addr=form.addr.data)

            flash("上传成功", "success")
        else:
            flash_errors(form)

        return render_template('public/add.html', form=form)
    return render_template('public/add.html', form=form)


@blueprint.route('/lists', methods=['GET', 'POST'])
@login_required
def lists():

    users = {}
    for user in User.query.filter_by().all():
        users[user.id] = user.nickname

    date = [{
        "image": model.image,
        "id": model.id,
        "name": model.name,
        "tel_cell": model.tel_cell,
        "email": model.email,
        "department": model.department,
        "title": model.title,
        "company": model.company,
        "original_factory": model.original_factory,
        "remarks": model.remarks,
        "own": users[model.own] if model.own else None,

    } for model in Cards.query.filter_by().all()]

    return render_template('public/lists.html', dates=date)


@blueprint.route('/down', methods=['GET'])
def down():
    date = [[
            "公司名称", "姓名", "电话", "邮箱", "部门", "职位", "地址", "原厂", "备注", '上传人员', "上传时间"]]

    users = {}
    for user in User.query.filter_by().all():
        users[user.id] = user.nickname

    for model in Cards.query.filter_by(is_analysis=True).all():

        """ 
            name = Column(db.String(1000))
            email = Column(db.String(500))   # 邮箱
            tel_cell = Column(db.String(500))  # 电话
            tel_work = Column(db.String(500))  # 工作电话
            department = Column(db.String(500))  # 部门
            title = Column(db.String(500))  # 头衔
            company = Column(db.String(500))  # 公司
            original_factory = Column(db.String(500))
            remarks = Column(db.String(5000))  # 备注
            image = Column(db.String(500))
        """

        _d = [model.company, model.name, model.tel_cell, model.email, model.department, model.title, model.addr,
              model.original_factory, model.remarks, users[model.own] if model.own else None, model.created_at]

        date.append([",".join(i) if isinstance(i, list) else i for i in _d])

    return excel.make_response_from_array(date, 'xlsx', file_name='cards')


@blueprint.route('/download_image/<string:filename>', methods=['GET'])
def download_image(filename):
    dirpath = os.path.join(STATIC_PATH, "photo")
    return send_from_directory(dirpath, filename, as_attachment=True)


@blueprint.route('/delete_card/<int:_id>', methods=['GET'])
def delete_card(_id):
    model = Cards.query.filter_by(id=_id).first()

    if model.own == current_user.id:
        model.delete()
        flash("delete success")
    else:
        flash("No authority")

    redirect_url = request.args.get("next") or url_for("public.lists")
    return redirect(redirect_url)

