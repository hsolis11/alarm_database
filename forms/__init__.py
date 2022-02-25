from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SelectField, StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.fields.simple import FileField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from database import EqpModels, EqpModules, Users


class SearchForm(FlaskForm):
    vendor = SelectField('Vendor:', choices=[('1', 'SEMES'), ('2', 'TEL')])
    model = SelectField('Model:', choices=[])
    module = SelectField('Module', choices=[])
    alarm_id = StringField('ALID:')
    search = SubmitField('Search')

    def fill_model(self, choice=1, all=False):
        model_choices = [(x.idmodel, x.model) for x in EqpModels().get_list(vendor=choice)]
        if all:
            model_choices.insert(0, ('all', 'ALL'))
        self.model.choices = model_choices

    def fill_module(self, choice=1, all=False, only_all=False):
        if only_all:
            module_choices = [('all', 'ALL')]
        else:
            module_choices = [(x.idmodule, x.module) for x in EqpModules().get_list(model=choice)]
            if all:
                module_choices.insert(0, ('all', 'ALL'))
        self.module.choices = module_choices


class LoginForm(FlaskForm):
    tech_id = StringField('TechID', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    tech_id = StringField('TechID', validators=[DataRequired(), Length(min=2, max=20)])
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_tech_id(self, tech_id):
        result = Users().get(tech_id=tech_id)
        if result:
            raise ValidationError('That TechID is already registered. Click forgot password')


class CreateAlarmCard(FlaskForm):
    vendor = SelectField('Vendor:', choices=[('1', 'SEMES'), ('2', 'TEL')])
    model = SelectField('Model:', choices=[])
    module = SelectField('Module', choices=[])
    alarm_id = StringField('Alarm ID:', validators=[DataRequired()])
    title = StringField('Title:', validators=[DataRequired()])
    message = TextAreaField('Message:', validators=[DataRequired()])
    cause = TextAreaField('Cause:', validators=[DataRequired()])
    response = TextAreaField('Response:', validators=[DataRequired()])
    submit = SubmitField('Create')

    def fill_model(self, choice=1):
        self.model.choices = [(x.idmodel, x.model) for x in EqpModels().get_list(vendor=choice)]

    def fill_module(self, choice=1):
        self.module.choices = [(x.idmodule, x.module) for x in EqpModules().get_list(model=choice)]


class UpdateProfileForm(FlaskForm):
    f_name = StringField('First Name', validators=[DataRequired()])
    l_name = StringField('Last Name', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class AddPostForm(FlaskForm):
    user_id = HiddenField()
    entry = TextAreaField('Add Quick Entry:')
    idalarm = HiddenField()
    submit = SubmitField('Post')


class AddPartForm(FlaskForm):
    idalarm = HiddenField()
    q_number = StringField('Q Number')
    vendor_pn = StringField('Vendor PN')
    description = StringField('Description')
    submit = SubmitField('Add Part')