#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mercurio import mercurio

if __name__ == '__main__':

    hg = mercurio(
        host="smtp.test.com",
        port=25,
        smtp_user="myuser",
        smtp_pwd="mypwd"
    )

    # to debug purposes, you can create the message and save it on disk
    # without send it thgrougth smtp.
    message = hg.make_message(
        fromaddress="from@me.com",
        recipient="to@me.com",
        reply_to_address="reply@to.me",
        text="a long text, very long.",
        sbj="The subject, or the object?",
        attachments=[],
        cid_attachments={}
    )

    with open('test_email.eml', 'w') as o:
        o.write(message.as_string())

    # hg.send(
    #     fromaddress="from@me.com",
    #     recipients=["to@me.com"],
    #     reply_to_address="reply@to.me",
    #     text="a long text, very long.",
    #     sbj="The subject, or the object?",
    #     attachments=[],
    #     cid_attachments={"content_id_01": "mylogo.png"}
    # )
