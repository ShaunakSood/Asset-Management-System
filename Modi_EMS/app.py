from flask import Flask, render_template, request, redirect, url_for
from extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_migrate import Migrate
from forms import LoginForm, RegistrationForm
from models import Asset, User
from forms import AssetForm
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin,expose
from forms import SearchForm
import csv
from flask import make_response


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://ems_user1:modi_user123@localhost:3306/asset_management"
app.config["SECRET_KEY"] = "MIPL888"

migrate = Migrate(app, db)
db.init_app(app)


class SearchForm(FlaskForm):
    search = StringField("Search", validators=[DataRequired()])

class SearchFilter(ModelView):
    def get_query(self):
        return self.model.query.filter((self.model.name.like('%' + self.search_form.search.data + '%')) |
                                        (self.model.description.like('%' + self.search_form.search.data + '%')) |
                                        (self.model.location.like('%' + self.search_form.search.data + '%')) |
                                        (self.model.category.like('%' + self.search_form.search.data + '%')) |
                                        (self.model.status.like('%' + self.search_form.search.data + '%')))

    def is_accessible(self):
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class AssetView(SearchFilter):
    form = AssetForm
    column_searchable_list = ['name', 'description', 'location', 'category', 'status']

class UserView(ModelView):
    form_columns = ['username', 'password']

admin = Admin(app, name='Enterprise Management Software', template_mode='bootstrap3')
admin.add_view(AssetView(Asset, db.session))
admin.add_view(UserView(User, db.session))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                return redirect(url_for("assets"))
            else:
                form.password.errors.append("Incorrect password")
        else:
            form.username.errors.append("User not found")
    return render_template("login.html", form=form)

@app.route("/assets", methods=['GET', 'POST'])
def assets():
    form = AssetForm()
    search_form = SearchForm()
    assets = Asset.query.all()
    if form.validate_on_submit():
        asset = Asset(
            name=form.name.data,
            description=form.description.data,
            location=form.location.data,
            category=form.category.data,
            status=form.status.data
        )
        db.session.add(asset)
        db.session.commit()
        return redirect(url_for("assets"))
    print(assets)
   
    return render_template("assets.html", form=form, assets=assets,search_form=search_form)

@app.route('/edit_asset/<int:id>', methods=['GET', 'POST'])
def edit_asset(id):
    asset = Asset.query.get_or_404(id)
    form = AssetForm(obj=asset) 
    if request.method == 'POST':
        asset.name = request.form['name']
        asset.description = request.form['description']
        asset.location = request.form['location']
        asset.category = request.form['category']
        asset.status = request.form['status']
        db.session.commit()
        return redirect(url_for('assets'))
    return render_template('edit_asset.html', asset=asset, form=form) 

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            form.username.errors.append("Username already exists")
        else:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_term = search_form.search.data
        assets = Asset.query.filter((Asset.name.like('%' + search_term + '%')) |
                                    (Asset.description.like('%' + search_term + '%')) |
                                    (Asset.location.like('%' + search_term + '%')) |
                                    (Asset.category.like('%' + search_term + '%')) |
                                    (Asset.status.like('%' + search_term + '%'))).all()
        return render_template('search_results.html', assets=assets, form=search_form)
    return render_template('search.html', form=search_form)

@app.route('/export_csv', methods=['POST'])
def export_csv():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_term = search_form.search.data
        assets = Asset.query.filter((Asset.name.like('%' + search_term + '%')) |
                                    (Asset.description.like('%' + search_term + '%')) |
                                    (Asset.location.like('%' + search_term + '%')) |
                                    (Asset.category.like('%' + search_term + '%')) |
                                    (Asset.status.like('%' + search_term + '%'))).all()
        
     
        response = make_response()
        response.status_code = 200
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename="assets.csv"'
        
        
        writer = csv.writer(response.stream)
        writer.writerow(['Name', 'Description', 'Location', 'Category', 'Status'])  
        for asset in assets:
            writer.writerow([asset.name, asset.description, asset.location, asset.category, asset.status])
        
        return response
    
if __name__ == "__main__":
    app.run(debug=True)
