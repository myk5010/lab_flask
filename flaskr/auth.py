import functools

from flask import (
  Blueprint, flash, g, redirect, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 注册
@bp.route('/register', methods=['POST'])
def register():
  username = request.form['username']
  password = request.form['password']
  db = get_db()
  error = None

  if not username:
    error = 'Username is required.'
  elif not password:
    error = 'Password is required.'
  elif db.execute(
    'SELECT id FROM user WHERE username = ?', (username,)
  ).fetchone() is not None:
    error = 'User {} is already registered.'.format(username)

  if error is None:
    db.execute(
      'INSERT INTO user (username, password) VALUES (?, ?)',
      (username, generate_password_hash(password))
    )
    db.commit()
    return '注册成功'

  return error


# 登录
@bp.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']
  error = None
  db = get_db()
  user = db.execute(
    'SELECT * FROM user WHERE username = ?', (username,)
  ).fetchone()

  if user is None:
    error = 'Incorrect username.'
  elif not check_password_hash(user['password'], password):
    error = 'Incorrect password.'

  if error is None:
    session.clear()
    session['user_id'] = user['id']
    return redirect(url_for('index'))

  return error


@bp.before_app_request
def load_logged_in_user():
  user_id = session.get('user_id')

  if user_id is None:
    g.user = None
  else:
    g.user = get_db().execute(
      'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))


# 登录验证装饰器
def login_required(view):
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))

    return view(**kwargs)

  return wrapped_view