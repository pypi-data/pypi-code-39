import json

def decodeJson(json_message):
    json_data = json.loads(json_message)
    return json_data

def parseEntities(message):
    orig_msg_text = message["text"]
    msg_text = message["text"]
    added_chars = 0
    for entity in message["entities"]:
        entity_content = orig_msg_text[entity["offset"]:][:entity["length"]]
        if entity["type"] == "mention":
            msg_text = msg_text.replace(entity_content, '<a href="https://t.me/'+entity_content.replace("@", "")+'">'+entity_content+'</a>')
        if entity["type"] == "url":
            msg_text = msg_text.replace(entity_content, '<a href="'+entity_content+'">'+entity_content+'</a>')
        if entity["type"] == "email":
            msg_text = msg_text.replace(entity_content, '<a href="mailto:'+entity_content+'">'+entity_content+'</a>')
        #if entity["type"] == "phone_number":
            #msg_text = msg_text.replace(entity_content, '<a href="tel:'+entity_content+'">'+entity_content+'</a>')
        if entity["type"] == "bold":
            msg_text = msg_text.replace(entity_content, '<b>'+entity_content+'</b>')
        if entity["type"] == "italic":
            msg_text = msg_text.replace(entity_content, '<i>'+entity_content+'</i>')
        if entity["type"] == "code":
            msg_text = msg_text.replace(entity_content, '<code>'+entity_content+'</code>')
        if entity["type"] == "pre":
            msg_text = msg_text.replace(entity_content, '<code>'+entity_content+'</code>')
        if entity["type"] == "text_link":
            msg_text = msg_text.replace(entity_content, '<a href="'+entity["url"]+'">'+entity_content+'</a>')


    return msg_text


def getHtml(json_message):
    message = decodeJson(json_message)
    htmlmessage = parseEntities(message).replace("""
""", "<br>")
    return htmlmessage
