from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from itertools import groupby

from .. import db
from ..models import User, Dialog, Question, Answer
from . import admin
from .forms import DialogForm


def check_admin():
    if not current_user.is_admin:
        abort(403)


# Dialog Views

@admin.route('/dialogs', methods=['GET', 'POST'])
@login_required
def list_dialogs():
    check_admin()
    
    dialogs = Dialog.query.all()
    questions = Question.query.all()
    questions = {k: list(v) for k, v in groupby(questions, lambda x: x.dialog_id)}
    answers = Answer.query.all()
    answers = {k: list(v) for k, v in groupby(answers, lambda x: x.dialog_id)}

    for dialog in dialogs:
        dialog.question = next(iter(questions.get(dialog.id, [])), None)
        dialog.answer = next(iter(answers.get(dialog.id, [])), None)

    return render_template('admin/dialogs/dialogs.html', dialogs=dialogs, title="Dialogs")


@admin.route('/dialogs/add', methods=['GET', 'POST'])
@login_required
def add_dialog():
    check_admin()

    form = DialogForm()

    # check for cancel button press
    if form.is_submitted() and not form.submit.data:
        return redirect(url_for('admin.list_dialogs'))
    
    if form.validate_on_submit():
        try:
            dialog = Dialog()
            db.session.add(dialog)
            db.session.flush()

            question = Question(dialog_id=dialog.id, text=form.question.data)
            db.session.add(question)

            answer = Answer(dialog_id=dialog.id, text=form.answer.data)
            db.session.add(answer)

            db.session.commit()
            flash('You have successfully added a new dialog.')
        except:
            db.session.rollback()
            flash('Unable to create dialog.')

        return redirect(url_for('admin.list_dialogs'))

    return render_template('admin/dialogs/dialog.html', action="Add", add_dialog=True, 
                           form=form, title="Add Dialog")


@admin.route('/dialogs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dialog(id):
    check_admin()

    dialog = Dialog.query.get_or_404(id)
    form = DialogForm(obj=dialog)

    # check for cancel button press
    if form.is_submitted() and not form.submit.data:
        return redirect(url_for('admin.list_dialogs'))

    question = Question.query.filter_by(dialog_id=dialog.id).first()
    answer = Answer.query.filter_by(dialog_id=dialog.id).first()
    
    if form.validate_on_submit():
        try: 
            if question and question.text != form.question.data:
                question.text = form.question.data
            elif not question and form.question.data:
                question = Question(dialog_id=dialog.id, text=form.question.data)
                db.session.add(question)

            if answer and answer.text != form.answer.data:
                answer.text = form.answer.data
            elif not answer and form.answer.data:
                answer = Answer(dialog_id=dialog.id, text=form.answer.data)
                db.session.add(answer)

            db.session.commit()
            flash('You have successfully edited the dialog.')
        except:
            flash('Unable to edit dialog.')
            db.session.rollback()

        return redirect(url_for('admin.list_dialogs'))

    form.question.data = question.text if question else None
    form.answer.data = answer.text if answer else None

    return render_template('admin/dialogs/dialog.html', action="Edit", add_dialog=False, 
                           form=form, dialog=dialog, title="Edit Dialog")


@admin.route('/dialogs/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_dialog(id):
    check_admin()

    try: 
        dialog = Dialog.query.get_or_404(id)
        db.session.delete(dialog)
        question = Question.query.filter_by(dialog_id=dialog.id).delete()
        answer = Answer.query.filter_by(dialog_id=dialog.id).delete()
        db.session.commit()
        flash('You have successfully deleted the dialog.')
    except:
        flash('Unable to delete dialog.')
        db.session.rollback()

    return redirect(url_for('admin.list_dialogs'))