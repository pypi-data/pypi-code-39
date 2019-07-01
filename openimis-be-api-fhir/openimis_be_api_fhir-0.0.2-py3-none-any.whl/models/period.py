from api_fhir.models import Element, Property


class Period(Element):

    end = Property('end', 'FHIRDate')
    start = Property('start', 'FHIRDate')

    class Meta:
        app_label = 'api_fhir'
