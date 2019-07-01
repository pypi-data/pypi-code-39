from api_fhir.models import Element, Property


class CodeableConcept(Element):

    coding = Property('coding', 'Coding', count_max='*')
    text = Property('text', str)

    class Meta:
        app_label = 'api_fhir'
