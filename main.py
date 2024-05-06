# MAKE START.SH, REQUERENMENTS.TXT AND THAT STUFF FILES FOR GLITCH

from flask import Flask, render_template, redirect, send_from_directory
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from flask_uploads import UploadSet, configure_uploads, patch_request_class

from models import db_session
from models.users import User
from forms.loginform import LoginForm
from forms.registerform import RegisterForm

from constants.constants import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

# """ for uploading """
app.config['UPLOADED_PROJECT_DEST'] = UPLOAD_FOLDER

projectsphotos = UploadSet('project', extensions='png')
configure_uploads(app, projectsphotos)
patch_request_class(app)


projectarchives = UploadSet('project', extensions='zip')
configure_uploads(app, projectarchives)
patch_request_class(app)
# """ for uploading """


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        user = load_user(current_user.get_id())
        fl = user.role
    else:
        fl = 0
    return render_template('not_made.html', flag=fl)


@app.route('/post-project', methods=['GET', 'POST'])
@login_required
def post_project():
    from models.projects import Project
    # from models.users import User  # THAT'S ESSENTIAL
    from forms.post_proj_form import PostProjForm

    form = PostProjForm()
    if form.validate_on_submit():
        # saving in /static/...
        db_sess = db_session.create_session()
        if db_sess.query(Project).filter(Project.project_name == form.name.data).first():
            return render_template('post_project.html', title='Публикация',
                                   form=form,
                                   message="Такое имя проекта уже есть")

        filename_image = projectsphotos.save(form.image.data, name=f'{form.name.data.replace(" ", "_")}_img.')
        filename_archive = projectarchives.save(form.archive.data, name=f'{form.name.data.replace(" ", "_")}_arch.')

        proj = Project(
            project_name=form.name.data,
            project_type=PROJECTS_TYPES.index(form.proj_type.data),
            project_platform=form.platform.data,
            short_description=form.short_description.data,
            description=form.detailed_description.data,
            archive=filename_archive,
            image=filename_image
        )
        db_sess.add(proj)
        db_sess.commit()
        return redirect('/successful_download')
    return render_template('post_project.html', form=form, flag=load_user(current_user.get_id()).role)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, flag=0)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            user_name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            user_role=USERS_TYPES[form.user_role.data],
            platform=form.platform.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/index')
    return render_template('registration.html', title='Регистрация', form=form, flag=0)


@app.route('/projects')
def projects():
    from models.projects import Project

    if current_user.is_authenticated:
        user = load_user(current_user.get_id())
        fl = user.role
    else:
        fl = 0
    db_sess = db_session.create_session()
    projects_a_ds = []
    for proj in db_sess.query(Project).all():
        d = {'project_type': PROJECTS_TYPES[int(proj.project_type)], 'project_name': proj.project_name,
             'date_creation': proj.project_date.date(), 'platform': proj.project_platform,
             'project_short_description': proj.short_description,
             'archive_name': f'{UPLOAD_FOLDER}/{proj.archive}'}

        projects_a_ds.append(d)
    return render_template('projects.html', projects=projects_a_ds, flag=fl)


@app.route('/about')
def about():
    if current_user.is_authenticated:
        user = load_user(current_user.get_id())
        fl = user.role
    else:
        fl = 0
    return render_template('about.html', flag=fl)


@app.route('/profiles')
@app.route('/profile')
def profiles():
    if current_user.is_authenticated:
        user = load_user(current_user.get_id())
        fl = user.role
    else:
        fl = 0
    return render_template('not_made.html', flag=fl)


@app.route('/successful_download')
def profile():
    if current_user.is_authenticated:
        user = load_user(current_user.get_id())
        fl = user.role
    else:
        fl = 0
    return render_template('/successful_download.html', flag=fl)


@app.route('/' + UPLOAD_FOLDER + '/<file_name>')
def images(file_name):
    return send_from_directory(app.config['UPLOADED_PROJECT_DEST'], file_name, as_attachment=True)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port='8080', host='127.0.0.1')


if __name__ == '__main__':
    main()
