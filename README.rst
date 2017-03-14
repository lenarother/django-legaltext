=========
legaltext
=========

Legaltext is a Django application supporting versioning of legal texts (e.g. participation terms
or privacy terms). It also supports versioning of checkbox labels.


Features
========

* LegalTextField model field
* LegalTextCheckboxFormField form field
* add_legaltext_checkboxes form helper
* managing legaltext and checkbox labels through admin interface


Usage
=====

requirements.txt
~~~~~~~~~~~~~~~~

::

    git+https://PRIVATE_TOKEN@github.com/moccu/django-legaltext.git#egg=django-legaltext


settings.py
~~~~~~~~~~~

::

    INSTALLED_APPS = (
        ...
        'markymark',  # required for markdown
        'legaltext',
    )


urls.py
~~~~~~~

::

    urlpatterns = [
        ...
        url(r'^legaltext/', include('legaltext.urls')),
    ]


templates
~~~~~~~~~

To overwrite basic legaltext template which displas legaltext content place
legaltext/content.html in your templates directory


constants.py
~~~~~~~~~

Having legaltext slug as constant is not neccessary, however this approach is less error-prone than repeating slug as string in duifferent parts of the code.

::

    MOCKAPP_TERMS_SLUG = 'mockapp-terms'


models.py
~~~~~~~~~

::

    from django.db import models
    from django.utils import timezone
    from django.utils.translation import ugettext_lazy as _

    from legaltext.fields import LegalTextField


    class SurveyParticipant(models.Model):
        name = models.CharField(_('Name'), max_length=255)
        date_submit = models.DateTimeField(_('Survey submited date'), default=timezone.now)
        ...

        accepted_terms = LegalTextField(MOCKAPP_TERMS_SLUG)


forms.py
~~~~~~~~

::

    from django.forms import ModelForm

    from legaltext.widgets import CheckboxWidget

    from .constants import MOCKAPP_PRIVACY_SLUG, MOCKAPP_TERMS_SLUG
    from .models import MockSurveyParticipant


    class MockappParticipationForm(ModelForm):

        class Meta:
            model = MockSurveyParticipant
            fields = ('name', 'accepted_terms')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['accepted_terms'].widget = CheckboxWidget(MOCKAPP_TERMS_SLUG)
            self.fields['accepted_terms'].required = True


Resources
=========

* `Code <https://github.com/moccu/django-legaltext>`_
* `Usage example <https://github.com/moccu/django-legaltext/tree/master/legaltext/tests/resources>`_
