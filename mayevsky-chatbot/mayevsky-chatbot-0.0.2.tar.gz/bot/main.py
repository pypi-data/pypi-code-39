from vk_api.longpoll import VkEventType, VkLongPoll
import vk_api
import os
from bd_interacting import Storage

storage = Storage("data.db")

storage.push_taxa("./")

vk_session = vk_api.VkApi(token=os.environ["VK_API_TOKEN"])
longpool = VkLongPoll(vk_session)
vk = vk_session.get_api()
current_volunteers_status = {}
current_volunteers_taxa = {}
current_volunteers_taxa_id = {}

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.user_id in current_volunteers_status.keys():
            if event.text == "ready" and current_volunteers_status[event.user_id] == 0:
                current_volunteers_status[event.user_id] = 1
                taxa_id, taxa = storage.shift_taxa()

                if storage.min_status == 0:
                    vk.messages.send(user_id=event.user_id,
                                     message="напишите описание таксона " + taxa,
                                     random_id="")
                if storage.min_status == 1:
                    vk.messages.send(user_id=event.user_id,
                                     message="напишите дочерние таксоны " + taxa + " на латыни, каждый с новой строки и\
                                      заглавной буквы (если этот таксон вид, просто напишите species)",
                                     random_id="")
                if storage.min_status == 2:
                    vk.messages.send(user_id=event.user_id,
                                     message="напишите, сколько развилок в таксоне " + taxa,
                                     random_id="")

                if storage.min_status == 3:
                    vk.messages.send(user_id=event.user_id,
                                     message="Хотя нет. Кажется, цель моей жизни достигнута. Теперь я могу спокойно \
                                     отключиться. Кстати, вы единственный, кто увидит это сообщение, гордитесь",
                                     random_id="")
                    break

                current_volunteers_taxa[event.user_id] = taxa
                current_volunteers_taxa_id[event.user_id] = taxa_id
            elif current_volunteers_status[event.user_id] == 1:
                if storage.min_status == 0:
                    storage.update_taxa_description(current_volunteers_taxa_id[event.user_id], event.text)

                if storage.min_status == 1:
                    if event.text == "species":
                        storage.update_taxa_species(current_volunteers_taxa_id[event.user_id], True)
                        storage.update_taxa_status(current_volunteers_taxa_id[event.user_id], 3)
                    else:
                        for child_taxon in event.text.splitlines():
                            storage.push_taxa(current_volunteers_taxa[event.user_id] + "/" + child_taxon)

                        storage.update_taxa_species(current_volunteers_taxa_id[event.user_id], False)

                if storage.min_status == 2:
                    for i in range(int(event.text)):
                        storage.push_vertex(current_volunteers_taxa[event.user_id], i+1)

                vk.messages.send(user_id=event.user_id,
                                 message="спасибо, вы нам очень помогли. Если хотите ещё помочь, начните сначала",
                                 random_id="")

                del current_volunteers_status[event.user_id]
                del current_volunteers_taxa[event.user_id]
                del current_volunteers_taxa_id[event.user_id]

        else:
            current_volunteers_status[event.user_id] = 0
            vk.messages.send(user_id=event.user_id,
                             message="Здравствуйте, я mayevsky-chatbot, если готовы получить задание, напишите ready",
                             random_id="")


