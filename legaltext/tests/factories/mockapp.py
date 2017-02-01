import factory

from legaltext.tests.resources.mockapp.models import MockSurveyParticipant


class MockSurveyParticipantFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda i: 'Test Participant-{0}'.format(i))

    class Meta:
        model = MockSurveyParticipant
