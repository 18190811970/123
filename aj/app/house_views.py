import os
from distutils.command import upload

from flask import Blueprint, render_template, jsonify, session, request
from flask_login import current_user

from app.models import User, House, Facility, HouseImage, Area
from utils.function import login_required

house_blue = Blueprint('house', __name__)


@house_blue.route('/myhouse/', methods=['GET'])
@login_required
def myhouse():
    return render_template('myhouse.html')


@house_blue.route('/myhouse_info/', methods=['GET'])
@login_required
def myhouse_info():
    user = User.query.get(session['user_id'])
    id_card = user.id_card
    # 判断是否实名认证
    if id_card:
        return jsonify({'code': 200})
    return jsonify({'code': 1001})


@house_blue.route('/newhouse/', methods=['GET'])
@login_required
def newhouse():
    return render_template('newhouse.html')


@house_blue.route('/area_facility/', methods=['GET'])
def area_facility():
    areas = Area.query.all()
    facilitys = Facility.query.all()

    areas_json = [area.to_dict() for area in areas]
    facilitys_json = [facility.to_dict() for facility in facilitys ]

    return jsonify({'code':200, 'areas':areas_json, 'facilitys':facilitys_json})


@house_blue.route('/newhouse/', methods=['POST'])
@login_required
def my_newhouse():
    # 保存房屋信息，设施信息

    house = House()
    house.user_id = session['user_id']
    house.price = request.form.get('price')
    house.title = request.form.get('title')
    house.area_id = request.form.get('area_id')
    house.address = request.form.get('address')
    house.room_count = request.form.get('room_count')
    house.acreage = request.form.get('acreage')
    house.unit = request.form.get('unit')
    house.capacity = request.form.get('capacity')
    house.beds = request.form.get('beds')
    house.deposit = request.form.get('deposit')
    house.min_days = request.form.get('min_days')
    house.max_days = request.form.get('max_days')

    facilitys = request.form.getlist('facility')
    for facility_id in facilitys:
        facility = Facility.query.get(facility_id)
        # 多对多关联
        house.facilities.append(facility)
    house.add_update()
    return jsonify({'code':200, 'data': house.id})


@house_blue.route('/house_images/', methods=['POST'])
def house_images():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 获取媒体文件路径
    MEDIA_DIR = os.path.join(BASE_DIR, '/static/media/upload')
    # 接收图片
    image = request.files['house_image']
    # 获取图片名称
    filename = image.filename
    # 保存图片
    image.save('./static/media/upload/%s' % filename)
    # 获取当前房屋对象
    house = HouseImage()
    house_id = request.form.get('house_id')
    house.house_id = house_id
    house.url = filename
    house.add_update()


    # 创建房屋首图
    house = House.query.get(house_id)
    if not house.index_image_url:
        # house.index_image_url = image_url
        house.index_image_url = filename
        house.add_update()

    # first_house = House.query.get(house_id)
    # first_house.index_image_url = filename
    # first_house.add_update()
    return jsonify({'code':200,'image_url':filename})


@house_blue.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


