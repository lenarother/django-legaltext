=========
Legaltext
=========

Legaltext is a Django app to save versions of legaltexts e.g. when creating a survey participation form.


Authors
-------

Ute Bracklow, Stephan Jäkel


Quick start
-----------

1. Add "legaltext" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'markymark'
        'legaltext',
    ]

2. Run `python manage.py migrate` to create the legaltext models. 

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a legaltext (you'll need the Admin app enabled).

4. Use legaltext in your Participant model::
	
	from legaltext.models import LegalText, LegalTextVersion


	CONSTANT_PRIVACY =  LegalText.current('mysurvey10-privacy-terms')

	class Participant(models.Model):
		...    
		privacy_terms_text_version = models.ForeignKey(
			LegalTextVersion, blank=True, null=True)

		def save(self, *args, **kwargs):
			...
        	if self.privacy_terms_text_version is None:
            	self.privacy_terms_text_version = CONSTANT_PRIVACY
        	super(Participant, self).save(*args, **kwargs)
