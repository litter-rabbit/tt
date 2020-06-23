

from flask import Blueprint,render_template,current_app,request,redirect,flash,url_for
from flask_login import login_required,current_user
from tt.decrators import admin_required
from  tt.models import User,Player,Website,Advice
from tt.extendtions import db
from tt.forms.admin import WebsiteForm

admin_bp=Blueprint('admin',__name__)


@admin_bp.route('manage/user')
@login_required
@admin_required
def manage_user():

    per_page=current_app.config['TT_ARTICLE_PER_PAGE']
    page=request.args.get('page',1)
    if  current_user.is_authenticated :
        pagination=User.query.order_by(User.timestamp.desc()).paginate(page,per_page)
    users=pagination.items


    return render_template('admin/user_manage.html',pagination=pagination,users=users,page=page)


@admin_bp.route('manage/player')
@login_required
@admin_required
def manage_player():

    per_page=current_app.config['TT_ARTICLE_PER_PAGE']
    page=request.args.get('page',1)
    if  current_user.is_authenticated :
        pagination=Player.query.order_by(Player.timestamp.desc()).paginate(page,per_page)
    players=pagination.items


    return render_template('admin/player_manage.html',pagination=pagination,players=players,page=page)



@admin_bp.route('manage/advice')
@login_required
@admin_required
def manage_advice():

    per_page=current_app.config['TT_ARTICLE_PER_PAGE']
    page=request.args.get('page',1)
    if  current_user.is_authenticated :
        pagination=Advice.query.order_by(Advice.timestamp.desc()).paginate(page,per_page)
    advices=pagination.items


    return render_template('admin/advice_manage.html',pagination=pagination,advices=advices,page=page)


@admin_bp.route('manage/website',methods=['GET','POST'])
@login_required
@admin_required
def manage_website():
    form= WebsiteForm()
    if form.validate_on_submit():
        website=Website(infomation=form.information.data)
        db.session.add(website)
        db.session.commit()
        flash('更改公告成功','success')
        return  redirect(url_for('main.index'))

    website=Website.query.order_by(Website.timestamp.desc()).first()
    form.information.data=website.infomation
    return render_template('admin/website_manage.html',form=form)






@admin_bp.route('delete/user/<user_id>',methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):

    user=User.query.filter_by(id=user_id).first_or_404()
    if user.is_admin:
        flash('管理员不可删除')
        return redirect(url_for('.manage_user'))
    db.session.delete(user)
    db.session.commit()
    flash('删除成功','success')
    return redirect(url_for('.manage_user'))




@admin_bp.route('delete/player/<player_id>',methods=['POST'])
@login_required
@admin_required
def delete_player(player_id):

    player=Player.query.filter_by(id=player_id).first_or_404()
    db.session.delete(player)
    db.session.commit()
    flash('删除成功','success')
    return redirect(url_for('.manage_player'))

@admin_bp.route('points/add/player/<user_id>',methods=['POST'])
@login_required
@admin_required
def add_points(user_id):

    user=User.query.filter_by(id=user_id).first_or_404()
    user.points+=20
    db.session.commit()
    flash('增加积分成功','success')
    return redirect(url_for('.manage_user'))


@admin_bp.route('points/cut/player/<user_id>',methods=['POST'])
@login_required
@admin_required
def cut_points(user_id):

    user=User.query.filter_by(id=user_id).first_or_404()
    user.points-=20
    db.session.commit()
    flash('减少积分成功','success')
    return redirect(url_for('.manage_user'))



@admin_bp.route('search/user')
@login_required
@admin_required
def search_user():

    q = request.args.get('q', '')
    if q=='':
        flash('请输入搜索的用户名或者微信号','waring')
        return redirect(url_for('admin.manage_user'))
    page=request.args.get('page',1)
    per_page=current_app.config['TT_ARTICLE_PER_PAGE']

    pagination=User.query.whooshee_search(q).paginate(page,per_page)
    users=pagination.items

    return render_template('admin/user_manage.html',pagination=pagination,users=users,page=page)



@admin_bp.route('/search')
@login_required
@admin_required
def search_player():

    q = request.args.get('q', '')

    page=request.args.get('page',1)
    per_page=current_app.config['TT_ARTICLE_PER_PAGE']
    if q == '':
        flash('请输入球员的名称或者等级.', 'warning')
        return redirect(url_for('admin.manage_player'))
    elif q<='9' and q>'0':
        pagination=Player.query.filter_by(rank=int(q)).order_by(Player.timestamp.desc()).paginate(page,per_page)
    elif q=='10':
        pagination = Player.query.filter_by(rank=int(q)).order_by(Player.timestamp.desc()).paginate(page, per_page)
    else:
        pagination=Player.query.whooshee_search(q).paginate(page,per_page)
    players=pagination.items

    return render_template('admin/player_manage.html',pagination=pagination,players=players,page=page)



