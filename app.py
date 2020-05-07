from flask import Flask , render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, Form, FormField, FieldList
from wtforms.validators import InputRequired,  Length, AnyOf, Email
from collections import namedtuple
# from flask_bootstrap import bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Mysecret'
app.config['WTF_CSRF_ENABLED']=True
app.config['WTF_CSRF_SECRET_KEY']='AnotherKey'  #this is just to use a different key, not sure when it would be used
app.config['WFT_CSRF_TIME_LIMIT']=3600

# bootstrap = Bootstrap(app)
class TelephoneNumbers(Form):
    country_code = IntegerField('country code')
    area_code = IntegerField('area code')
    number = IntegerField('number')

class YearsForm(Form):
    year = IntegerField('year')
    total = IntegerField('total')


class LoginForm(FlaskForm):
    # username = StringField('username', validators=[InputRequired('required!')])
    username = StringField('username', validators=[InputRequired('A username is required!'), Length(min=4, max=8, message='Must be between 4 and 8 characters')])

    password = PasswordField('password', validators=[InputRequired('A password it required'), AnyOf(values=['secret', 'password'], message='non valid list')])

    age = IntegerField('Age', default=34)

    true = BooleanField('True')

    email = StringField('email', validators=[Email( message='Not a valid Email format')])

    home_phone = FormField(TelephoneNumbers)

    years = FieldList(FormField(YearsForm))

    # now to show the power of enclosers, what if you needed mnobile phone as weill,  well godod thing we alarday made a the class
    #so no we can just add it again but this time call it mobile_phone
    mobile_phone = FormField(TelephoneNumbers)

class NameForm(LoginForm):
    first_name= StringField("First name")
    last_name = StringField("Last name")




#this funtion is to pre-populate the form
class User:
    def __init__(self, username, age, email):
        self.username = username
        self.age=age
        self.email=email

@app.route('/', methods=['GET','POST'])
def index():
    myUser = User('philip22', 34, 'ptman@gmail.com')
    group = namedtuple('Group', ['year', 'total'])
    g1 = group(2002, 1000)
    g2 = group(2006, 1500)
    g3 = group(2007, 1700)

    years = {'years' : [g1,g2,g3]}

    # form = LoginForm()
    form = NameForm(obj=myUser, data=years)
#Disable CSRF security
   # form = LoginForm(obj=myUser, csrf_enabled=False)
    if form.validate_on_submit():
        # return '<h1>Username: {} Password: {} Age:{} Email:{}</h1>'.format(form.username.data, form.password.data, form.age.data, form.email.data)
        return '<h1>Country Code: {} Area code: {} Number : {}'.format(form.home_phone.country_code, form.home_phone.area_code, form.home_phone.number)
    return render_template('index.html', form=form)

@app.route('/dynamic', methods=['GET', 'POST'])
def dynamic():
    class DynamicForm(FlaskForm):
        pass

    DynamicForm.name = StringField('name')

    names = ['middle_name', 'last_name', 'nickname']
    for name in names:
        setattr(DynamicForm, name, StringField(name))
    form = DynamicForm()
    if form.validate_on_submit():
        return '<h1>Form has been validated.  Name : {}</h1>'.format(form.name.data)
    return render_template('dynamic.html', form = form, names = names)
if __name__ == '__main__':
    app.run(debug=True)
