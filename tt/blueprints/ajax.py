
from flask import Blueprint,jsonify,render_template
from flask_login import login_required
from tt.decrators import admin_required
from tt.models import Advice
from tt.extendtions import db

ajax_bp=Blueprint('ajax',__name__)


@ajax_bp.route('advice/show/<advice_id>',methods=['POST'])
@login_required
@admin_required
def show_advice(advice_id):

    advice=Advice.query.filter_by(id=advice_id).first()
    advice.is_read=True
    db.session.commit()
    return jsonify(message='阅读')

@ajax_bp.route('advice/get/<advice_id>')
@login_required
@admin_required
def get_advice(advice_id):

    advice=Advice.query.filter_by(id=advice_id).first()
    advice.is_read=True
    db.session.commit()
    return render_template('admin/advice_popup.html',advice=advice)

@ajax_bp.route('weixin/get')
def get_weixin():

    return render_template('main/weixin_popup.html')