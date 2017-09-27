================
django-legaltext
================

.. image:: https://badge.fury.io/py/django-legaltext.svg
    :target: https://pypi.python.org/pypi/django-legaltext
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/moccu/django-legaltext.svg?branch=master
    :target: https://travis-ci.org/moccu/django-legaltext
    :alt: Latest Travis CI build status


Legaltext is a Django application to help managing legal text versioning (e.g.
terms of condition, pr privacy policy). It also supports versioning of the
corresponding checkbox labels.


Features
========

The application consists of multiple parts and helpers:

* Models to maintain legal texts, their versions and checkboxes
* Model field to store the accepted version of a legal text (with support to
  auto-fetched default of current version)
* Form field to render the widget which outputs the configured checkboxes just
  using the legal text slug
* Admin interface to maintain the legal texts, adding new version with prefilling, and export
* Templatetag legaltext_url


Installation
============

requirements.txt
~~~~~~~~~~~~~~~~

Just add the following PyPI package to your requirements.txt
::

    django-legaltext


settings.py
~~~~~~~~~~~

To activate the application, add the following two packages to your `INSTALLED_APPS`
::

    INSTALLED_APPS = (
        ...
        'floppyforms',  # needed for widget rendering
        'markymark',  # required for markdown rendering
        'legaltext',
    )


urls.py
~~~~~~~

To register the url to output the legal texts, add the following to your `urls.py`.
::

    urlpatterns = [
        ...
        url(r'^legaltext/', include('legaltext.urls')),
    ]


Usage
=====

Please refer to the examples to learn how to use the application.

You just need to add a new model field to your models and set the correct formfield
in the corresponding forms.


::

    class YourModel(models.Model):
        ...

        accepted_legaltext = LegalTextField('some-unique-slug')


::

    class YourForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['accepted_legaltext'] = LegalTextFormField('some-unique-slug')


Make sure that you use the same slug on both (model and form) field.


Customization
=============

There are some more settings you can set to change the applcation

* `LEGALTEXT_ANCHOR_CLASS`
  Add an additional css class the the rendered anchor-span when using [anchor:foo]
* `LEGALTEXT_VIEW_TEMPLATE`
  Change the template which is used to in the view to output the legal text
* `LEGALTEXT_VIEW_TEMPLATE_OVERRIDES`
  Choose a different template to use in views for specific slugs
* `LEGALTEXT_WIDGET_TEMPLATE`
  Change the template which is used to in the widget to output the checkboxes
* `LEGALTEXT_WIDGET_TEMPLATE_OVERRIDES`
  Choose a different template to use in widget for specific slugs
* `LEGALTEXT_WIDGET_ATTRS`
  Add extra attributes to checkbox input elements
* `LEGALTEXT_SILENCE_TEMPLATE_ERRORS`
  Silence errors for legaltext_url templatetag if legaltext does not exist


Resources
=========

* `Code <https://github.com/moccu/django-legaltext>`_
* `Usage example <https://github.com/moccu/django-legaltext/tree/master/examples>`_
