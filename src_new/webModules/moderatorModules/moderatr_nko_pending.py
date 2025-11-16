from databaseModules.classUsersDB import UsersDB_module
from databaseModules.classNkoDB import NkoDB_module
from databaseModules.classKnowelegesDB import KnowelegesDB_module
from webModules.hash_password_usr import hasher_pass
from flask import render_template, redirect, session, request, flash
from ..admin_checker import check_moderaotr

def before_moder_nko_pending():
    if check_moderaotr():
        return moderator_nko_pending_(mail=session['username'])



def moderator_nko_pending_(mail):
    print(request, mail)

    msg = ''
    if request.method == "POST":
        to_do_status = 1
        action = request.form.get('action')
        if "true_nko" in action:
            to_do_status = 2
        if "false_nko" in action:
            to_do_status = 3

        nko_id = int(action.split("_")[-1])
        print(to_do_status, action, nko_id)

        if NkoDB_module().update_status_nko(nko_id=nko_id, status=to_do_status):
            msg = 'Успешно'
        else:
            msg = 'Ошибка удаления'

    user_id = UsersDB_module().select_with_mail(mail=session['username'])['user_id']
    nko_list = NkoDB_module().get_all_nko(user_id=user_id, status=1)
    return render_template('moderator/moderator-nko-pending.html', nko_list=nko_list, msg=msg)


