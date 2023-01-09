# -*- coding: utf-8 -*-
#
from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import FormField, StringField
from wtforms import PasswordField, BooleanField, validators, SelectMultipleField, EmailField, widgets, SelectField
from wtforms.widgets import html_params
from wtforms.widgets import html_params

# -*- coding: utf-8 -*-
#
from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import FormField, StringField
from wtforms import PasswordField, BooleanField, validators, SelectMultipleField, EmailField, widgets, SelectField
from wtforms.widgets import html_params


class ButtonWidget(object):
    """
    Renders a multi-line text area.
    `rows` and `cols` ought to be passed as keyword args when rendering.
    """
    input_type = 'button'
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)

        if 'value' not in kwargs:
            kwargs['value'] = field._value()

        return Markup('<button {params}>{label}</button>'.format(
            params=self.html_params(name=field.name, **kwargs),
            label=field.label.text))


class ButtonCloseWidget(ButtonWidget):
    """
    Renders a multi-line text area.
    `rows` and `cols` ought to be passed as keyword args when rendering.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)

        if 'value' not in kwargs:
            kwargs['value'] = field._value()

        return Markup('<button {params}>{label}</button>'.format(
            params=self.html_params(name=field.name, **kwargs),
            label=""))


class SubmitFieldWidget(ButtonWidget):
    """
    Renders a multi-line text area.
    `rows` and `cols` ought to be passed as keyword args when rendering.
    """
    input_type = 'submit'


class ButtonField(StringField):
    widget = ButtonWidget()


class SubmitField(StringField):
    widget = SubmitFieldWidget()


class ButtonCloseField(StringField):
    widget = ButtonCloseWidget()


class WTFPassworder(FlaskForm):
    password = PasswordField('Nouveau mot de passe', [validators.DataRequired(), validators.EqualTo('confirm',                                                                                                    message='La saisie ne coincide pas')])
    confirm = PasswordField('Répéter saisie mot de passe', [validators.DataRequired()])


class NoChoiceSelectField(SelectField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """

    def pre_validate(self, form):
        pass


class NopSelectMultipleField(SelectMultipleField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """

    def pre_validate(self, form):
        pass


class CellWidget:
    """
    Renders a list of fields as a set of table rows with th/td pairs.

    If `with_table_tag` is True, then an enclosing <table> is placed around the
    rows.

    Hidden fields will not be displayed with a row, instead the field will be
    pushed into a subsequent table row to ensure XHTML validity. Hidden fields
    at the end of the field list will appear outside the table.
    """

    def __init__(self, with_table_tag=True):
        self.with_table_tag = with_table_tag

    def __call__(self, field, **kwargs):
        html = []
        if self.with_table_tag:
            kwargs.setdefault("id", field.id)
            html.append("<fieldset %s>" % html_params(**kwargs))
        hidden = ""
        for subfield in field:
            if subfield.type in ("HiddenField", "CSRFTokenField"):
                hidden += str(subfield)
            else:
                html.append(
                    "<div class='cell margin-bottom-2'>%s%s%s</div>"
                    % (str(subfield.label), hidden, str(subfield))
                )
                hidden = ""
        if self.with_table_tag:
            print(kwargs)
            html.append("</div>")
        if hidden:
            html.append(hidden)
        return Markup("".join(html))


class CustomFormField(FormField):
    widget = CellWidget()


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MFlaskForm(FlaskForm):
    @property
    def data(self):
        dt = super(MFlaskForm, self).data

        if 'csrf_token' in dt:
            del dt['csrf_token']
        return dt

