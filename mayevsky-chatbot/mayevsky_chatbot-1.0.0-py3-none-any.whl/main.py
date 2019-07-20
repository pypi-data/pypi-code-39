from vk_api.longpoll import VkEventType, VkLongPoll
import vk_api
import os
from bot.bd_interacting import Storage
from bot.record import UserRecord


def respond_collecting_taxa(vk, user_id, min_status, taxa):  # give user a task to send taxa data
    if min_status == 0:
        vk.messages.send(user_id=user_id,
                         message="напишите описание таксона " + taxa,
                         random_id="")
    if min_status == 1:
        vk.messages.send(user_id=user_id,
                         message="напишите дочерние таксоны " + taxa + " на латыни, каждый с новой строки и заглавной \
                         буквы (если этот таксон вид, просто напишите species)",
                         random_id="")
    if min_status == 2:
        vk.messages.send(user_id=user_id,
                         message="напишите, сколько развилок в таксоне " + taxa,
                         random_id="")


def respond_collecting_vertices(vk, user_id, taxon, num):  # give user a task to send vertex data
    vk.messages.send(user_id=user_id,
                     message="Вам нужно описать развлку %d из таксона %s для этого запишите, разделяя \
                                         переходами на новую строку\n1.текст тезы\n2.номер, развилки, к которой ведёт теза \
                                         (0 если к дочернему таксону)\n3.Таксон, к которому ведёт теза (любой набор букв, \
                                         если ведёт к развилке)\n3.\n5.\n6.\nАналогично для антитезы" % (num, taxon),
                     random_id="")


def handle_taxa(storage, taxa, taxa_id, text):  # save taxa data, which was given us by user
    if storage.min_status == 0:
        storage.update_taxa_description(taxa_id, text)

    if storage.min_status == 1:
        if text == "species":
            storage.update_taxa_species(taxa_id, True)
            storage.update_taxa_status(taxa_id, 3)
        else:
            for child_taxon in text.splitlines():
                storage.push_taxa(taxa + "/" + child_taxon)

            storage.update_taxa_species(taxa_id, False)

    if storage.min_status == 2:
        for i in range(int(text)):
            storage.push_vertex(taxa, i + 1)


def handle_vertex(storage, vertex_id, text):  # save vertex data, which was given us by user
    storage.update_vertex(vertex_id, text)


def suicide(vk, storage, user_id):  # that means, all required data is collected
    vk.messages.send(user_id=user_id,
                     message="Я видел такое, что вам, людям, и не снилось... Атакующие корабли, пылающие над Орионом;\
                      лучи Си, пронизывающие мрак близ ворот Тангейзера... Все эти мгновения затеряются во времени, как \
                      слёзы в дожде. Время... умирать (все данные собраны, бот отключается. вы единственный(ая) кто \
                      получает это сообщение)",
                     random_id="")
    storage.finnish()


def register_user(vk, cur_users, user_id):  # dynamically create a record about user
    cur_users[user_id] = UserRecord()
    vk.messages.send(user_id=user_id,
                     message="Здравствуйте, я mayevsky-chatbot, если готовы получить задание, напишите Ok",
                     random_id="")


def handle_answer(vk, storage, cur_users, user_id, text):  # save data that user had told us, using data, dynamically
    # saved while asking
    if storage.min_status < 3:
        handle_taxa(storage,
                    cur_users[user_id].pos,
                    cur_users[user_id].pos_id,
                    text)
    else:
        handle_vertex(storage,
                      cur_users[user_id].pos_id,
                      text)

    storage.save()
    vk.messages.send(user_id=user_id,
                     message="спасибо, вы нам очень помогли. Если хотите ещё помочь, начните сначала",
                     random_id="")


def ask_data(vk, storage, cur_users, user_id):  # returns True if there is no data to ask
    cur_users[user_id].status = 1
    if storage.min_status < 3:
        taxa_id, taxa = storage.shift_taxa()

        respond_collecting_taxa(vk, user_id, storage.min_status, taxa)

        cur_users[user_id].pos = taxa
        cur_users[user_id].pos_id = taxa_id
        cur_users[user_id].task = storage.min_status
    if storage.min_status == 3:
        vertex_id, taxon, num = storage.shift_vertex()
        if vertex_id is None:
            return True

        respond_collecting_vertices(vk, user_id, taxon, num)
        cur_users[user_id].pos = (taxon, num)
        cur_users[user_id].pos_id = vertex_id
        cur_users[user_id].task = "vertex"

        return False


def backup_record(vk, storage, cur_users, user_id):  # decrements status by id (shifting increments it)
    if cur_users[user_id].task == "vertex":
        storage.backup_vertex_status(cur_users[user_id].pos_id)
    else:
        storage.update_taxa_status(cur_users[user_id].pos_id, cur_users[user_id].task)

    vk.messages.send(user_id=user_id,
                     message="во время сохранения данных, которые вы дали, произошла ошибка. Чаще всего это происходит \
                     из-за того, что данные введены неверно",
                     random_id="")


storage = Storage("data.db")

storage.push_taxa(".")

vk_session = vk_api.VkApi(token=os.environ["VK_API_TOKEN"])
longpool = VkLongPoll(vk_session)
vk = vk_session.get_api()

cur_users = {}
for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.user_id in cur_users.keys():
            if event.text == "Ok" and cur_users[event.user_id].status == 0:
                if ask_data(vk, storage, cur_users, event.user_id):
                    suicide(vk, storage, event.user_id)
                    break

            elif cur_users[event.user_id].status == 1:
                try:
                    handle_answer(vk, storage, cur_users, event.user_id, event.text)
                except:
                    backup_record(vk, storage, cur_users, event.user_id)

                del cur_users[event.user_id]

        else:
            register_user(vk, cur_users, event.user_id)
