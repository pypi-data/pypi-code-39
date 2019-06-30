import json

import GoogleApiSupport.auth as gs

class Size:
    def __init__(self, width: float = 3000000.0, height: float = 3000000.0, unit: str = 'EMU'):
        self.json = {
            "width": {
                "magnitude": width,
                "unit": unit
            },
            "height": {
                "magnitude": height,
                "unit": unit
            }
        }

    def __repr__(self):
        return json.dumps(self.json, indent=4)


class Transform:
    def __init__(self, scale_x: float = 1, scale_y: float = 1, shear_x: float = 0, shear_y: float = 0,
                 translate_x: float = 0, translate_y: float = 0, unit: str = 'EMU'):
        self.json = {
            "scaleX": scale_x,
            "scaleY": scale_y,
            "shearX": shear_x,
            "shearY": shear_y,
            "translateX": translate_x,
            "translateY": translate_y,
            "unit": unit
        }

    def __repr__(self):
        return json.dumps(self.json, indent=4)


def create_presentation(name):
    service = gs.get_service("slides")
    presentation = service.presentations().create(body={"title": name}).execute()
    return presentation['presentationId']


def get_presentation_info(presentation_id):  # Class ??
    service = gs.get_service("slides")
    presentation = service.presentations().get(
        presentationId=presentation_id).execute()
    return presentation


def get_presentation_slides(presentation_id):
    slides = presentation_info(presentation_id).get('slides')
    return slides


def get_slide_notes(slide_object: dict):
    output = []
    try:
        for element in slide_object['slideProperties']['notesPage']['pageElements']:
            if 'shapeType' in element['shape'] and element['shape']['shapeType'] == 'TEXT_BOX':
                for line in element['shape']['text']['textElements'][1::2]:
                    if 'textRun' in line:
                        output += [line['textRun']['content']]
        return ''.join(output)
    except Exception as e:
        return '# Error in slide' + str(e)


def execute_batch_update(requests, presentation_id):
    body = {
        'requests': requests
    }

    slides_service = gs.get_service("slides")
    response = slides_service.presentations().batchUpdate(presentationId=presentation_id,
                                                          body=body).execute()
    return response


def text_replace(old: str, new: str, presentation_id: str, pages: list = []):
    service = gs.get_service("slides")

    service.presentations().batchUpdate(
        body={

            "requests": [
                {
                    "replaceAllText": {
                        "containsText": {
                            "text": '{{' + old + '}}'
                        },
                        "replaceText": new,
                        "pageObjectIds": pages,
                    }
                }
            ]
        },
        presentationId=presentation_id
    ).execute()


def batch_text_replace(text_mapping: dict, presentation_id: str, pages: list = list()):
    """Given a list of tuples with replacement pairs this function replace it all"""
    requests = []
    for placeholder_text, new_value in text_mapping.items():
        if type(new_value) is str:
            requests += [
                {
                    "replaceAllText": {
                        "containsText": {
                            "text": '{{' + placeholder_text + '}}'
                        },
                        "replaceText": new_value,
                        "pageObjectIds": pages
                    }
                }
            ]
        else:
            raise Exception('The text from key {} is not a string'.format(placeholder_text))
    return execute_batch_update(requests, presentation_id)


def insert_image(url: str, page_id: str, presentation_id: str, object_id: str = None,
                 transform=None, size=None):
    requests = [
        {
            'createImage': {
                'objectId': object_id,
                'url': url,
                'elementProperties': {
                    'pageObjectId': page_id,
                    'transform': transform,
                    'size': size
                },
            }
        },
    ]

    return execute_batch_update(requests, presentation_id)


def replace_image(page_id: str, presentation_id: str, old_image_object: dict, new_image_url: str):
    insert_image(new_image_url, page_id, presentation_id,
                 transform=old_image_object['transform'],
                 size=Size())
    delete_object(presentation_id, old_image_object['objectId'])


def replace_shape_with_image(url: str, presentation_id: str, contains_text: str = None):
    requests = [
        {
            "replaceAllShapesWithImage": {
                "imageUrl": url,
                "replaceMethod": "CENTER_INSIDE",
                "containsText": {
                    "text": "{{" + contains_text + "}}",
                }
            }
        }]

    return execute_batch_update(requests, presentation_id)


def batch_replace_shape_with_image(image_mapping: dict, presentation_id: str):
    requests = []

    for contains_text, url in image_mapping.items():
        requests.append(
            {
                "replaceAllShapesWithImage": {
                    "imageUrl": url,
                    "replaceMethod": "CENTER_INSIDE",
                    "containsText": {
                        "text": "{{" + contains_text + "}}",
                    }
                }
            }
        )

    response = execute_batch_update(requests, presentation_id)
    return response


def duplicate_object(presentation_id: str, object_id: str):
    requests = [
        {
            'duplicateObject': {
                'objectId': object_id
            }
        },
    ]

    body = {
        'requests': requests
    }

    service = gs.get_service("slides")
    response = service.presentations().batchUpdate(presentationId=presentation_id,
                                                   body=body).execute()
    return response


def delete_object(presentation_id: str, object_id: str = None):
    requests = [
        {
            'deleteObject': {
                'objectId': object_id
            }
        },
    ]

    body = {
        'requests': requests
    }

    service = gs.get_service("slides")
    response = service.presentations().batchUpdate(presentationId=presentation_id,
                                                   body=body).execute()
    return response


def batch_delete_object(presentation_id: str, object_id_list: list = None):
    requests = []

    for element in object_id_list:
        requests.append(
            {
                'deleteObject': {
                    'objectId': element
                }
            }
        )

    response = execute_batch_update(requests, presentation_id)
    return response


def batch_delete_text(presentation_id: str, object_id_list: list = None):
    requests = []

    for element in object_id_list:
        requests.append(
            {
                'deleteText': {
                    'objectId': element
                }
            }
        )

    response = execute_batch_update(requests, presentation_id)
    return response


def delete_presentation_notes(presentation_id):
    slides_service = gs.get_service("slides")

    _slides = presentation_slides(presentation_id)

    elements_to_delete = []

    for _slide in _slides:
        if 'notesPage' in _slide['slideProperties']:
            for element in _slide['slideProperties']['notesPage']['pageElements']:
                if 'textRun' in str(element):
                    elements_to_delete.append(element['objectId'])

    batch_delete_text(presentation_id, elements_to_delete)


def transform_object(presentation_id: str, object_id: str, transform, apply_mode='ABSOLUTE'):
    requests = [
        {
            'updatePageElementTransform': {
                'objectId': object_id,
                'transform': transform,
                'applyMode': apply_mode
            }
        },
    ]

    body = {
        'requests': requests
    }

    service = gs.get_service("slides")
    response = service.presentations().batchUpdate(presentationId=presentation_id,
                                                   body=body).execute()
    return response
