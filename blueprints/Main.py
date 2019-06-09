from flask import Blueprint, render_template

from model import UserRepository

main = Blueprint(
    'simple_page',
    __name__,
    template_folder='templates'
)


@main.route('/')
def show_main():
    return render_template('users.html', users=UserRepository.get_all())


@main.route('/unregister_user/<user_id>')
def unregister_user(user_id):
    UserRepository.unregister(userId)
