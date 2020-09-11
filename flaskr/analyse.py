import functools

from flask import (
  Blueprint, flash, g, redirect, request, session, url_for, json, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('analyse', __name__, url_prefix='/analyse')

# 注册
@bp.route('/insert', methods=['POST'])
def insertData():
  # json转字典
  dictionary = json.loads(request.data)
  # 原生sql写法, 后期改sqlalchemy
  sql_start = 'INSERT INTO content_data ( parent_id, time,'
  sql_end = ' VALUES (1, '+str(dictionary['params'][0])+', '
  for i in range(1,17):
    sql_start += ' data_'+str(i)+','
    sql_end += str(dictionary['params'][i])+','
  sql_start = sql_start[:-1]
  sql_end = sql_end[:-1]
  sql_start += ') '+sql_end+')'
  db = get_db()
  db.execute(sql_start)
  # TODO: 这样写入的created_at和updated_at时间不对
  db.commit()
  return {'msg': '写入成功', 'type': 'success'}
