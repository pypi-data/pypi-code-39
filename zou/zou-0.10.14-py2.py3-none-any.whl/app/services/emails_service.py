from zou.app import config
from zou.app.utils import emails

from zou.app.services import (
    entities_service,
    persons_service,
    projects_service,
    tasks_service
)
from zou.app.stores import queue_store


def send_notification(person_id, subject, message):

    person = persons_service.get_person_raw(person_id)
    if person.notifications_enabled:
        if config.ENABLE_JOB_QUEUE:
            queue_store.job_queue.enqueue(
                emails.send_email,
                args=(subject, message, person.email)
            )
        else:
            emails.send_email(subject, message, person.email)
    return True


def send_comment_notification(person_id, comment, task):
    organisation = persons_service.get_organisation()
    author = persons_service.get_person(person_id)
    project = projects_service.get_project(task["project_id"])
    task_type = tasks_service.get_task_type(task["task_type_id"])
    task_status = tasks_service.get_task_status(task["task_status_id"])
    entity = entities_service.get_entity(task["entity_id"])

    episode_segment = ""
    entity_type = "shots"
    if project["production_type"] == "tvshow":

        if task_type.for_assets:
            episode_segment = "/episodes/%s" % entity["source_id"]
            entity_type = "assets"
        else:
            sequence = entities_service.get_entity(entity["parent_id"])
            episode_segment = "/episodes/%s" % sequence["parent_id"]

    task_url = "%s://%s/productions/%s%s/%s/tasks/%s" % (
        task["project_id"],
        episode_segment,
        entity_type,
        task["id"],
        config.DOMAIN_PROTOCOL,
        config.DOMAIN_NAME,
    )
    subject = "[Kitsu] %s - %s commented on %s" (
        task_status["short_name"],
        author["first_name"],
        task_name
    )
    message = """
%s

To reply connect to this URL:
%s

Best,

%s Team
""" % (
        task_status["short_name"],
        author["first_name"],
        comment["text"],
        task_url,
        organisation["name"]
    )
    return send_notification(person_id, subject, message)


def send_mention_notification(person_id, comment):
    organisation = persons_service.get_organisation()
    subject = "[Kitsu] Someone mentioned you in a comment"
    message = """

Best,

%s Team
""" % (
        config.DOMAIN_PROTOCOL,
        config.DOMAIN_NAME,
        organisation["name"]
    )
    return send_notification(person_id, subject, message)


def send_assignation_notification(person_id, task_id):
    organisation = persons_service.get_organisation()
    subject = "[Kitsu] You were assigned to a task"
    message = """

Best,

%s Team
""" % (
        config.DOMAIN_PROTOCOL,
        config.DOMAIN_NAME,
        organisation["name"]
    )
    return send_notification(person_id, subject, message)
