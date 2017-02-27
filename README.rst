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


settings.py
~~~~~~~~~~~

::

    INSTALLED_APPS = (
        ...
        'markymark',  # required for markdown 
        'legaltext',
    )


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

        accepted_terms = LegalTextField('survay-participation-terms')


forms.py
~~~~~~~~

::

    from django.forms import ModelForm

    from legaltext.fields import (LegalTextCheckboxFormField,
                                  add_legaltext_checkboxes)
    from legaltext.models import LegalText

    from .models import SurveyParticipant
    

    class SurveyParticipantForm(ModelForm):

        class Meta:
            model = MockSurveyParticipant
            fields = (
                'name', ...
            )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # add single checkbox with known field name
            legaltext_version = LegalText.current_version('survay-participation-terms)
            terms_checkbox = legaltext_version.checkboxtextversion_set.first()
            self.fields['accepted_terms'] = LegalTextCheckboxFormField(terms_checkbox)

            # add all fields automatically
            add_legaltext_checkboxes(self.fields, 'survay-participation-terms)


Resources
=========

* `Code <https://github.com/moccu/django-legaltext>`_
* `Usage example <https://github.com/moccu/django-legaltext/tree/master/legaltext/tests/resources>`_
