


from flask import Blueprint,render_template,flash,redirect,url_for,request,current_app
from flask_login import login_required
from tt.forms.main import PlayerForm,AdviceForm
from tt.models import Player
from tt.extendtions import db
from flask_login import current_user
from tt.models import User,Website,Advice

main_bp=Blueprint('main',__name__)


@main_bp.route('/')
def index():
    per_page = current_app.config['TT_ARTICLE_PER_PAGE']
    user=None
    if current_user.is_authenticated:
        user=User.query.filter_by(name=current_user.name).first()

    page=request.args.get('page',1)
    pagination=Player.query.order_by(Player.timestamp.desc()).paginate(page,per_page)
    players=pagination.items
    website = Website.query.order_by(Website.timestamp.desc()).first()
    return render_template('main/index.html',pagination=pagination,players=players,user=user,website=website)


@main_bp.route('/publish_player',methods=['GET','POST'])
@login_required
def publish_player():

    form=PlayerForm()
    if form.validate_on_submit():
        name=form.name.data
        rank=form.rank.data
        backup=form.backup.data
        player=Player(name=name,rank=rank,backup=backup)
        current_user.players.append(player)
        db.session.commit()
        flash('发布成功','success')
        return redirect(url_for('main.index'))

    return render_template('main/publish_player.html',form=form)



@main_bp.route('/show/player')
@login_required
def show_player():
    page=request.args.get('page',1)
    per_page = current_app.config['TT_ARTICLE_PER_PAGE']
    paginations=Player.query.filter_by(user_id=current_user.id).order_by(Player.timestamp.desc()).paginate(page,per_page)
    players=paginations.items

    return render_template('main/show_players.html',pagination=paginations,players=players)


@main_bp.route('/delete/player/<player_id>')
@login_required
def delete_player(player_id):
    player=Player.query.filter_by(id=player_id).first_or_404()
    db.session.delete(player)
    db.session.commit()
    flash('删除成功','success')
    return redirect(url_for('.show_player'))




@main_bp.route('/search')
def search():
    user = None
    if current_user.is_authenticated:
        user = User.query.filter_by(name=current_user.name).first()
    q = request.args.get('q', '')
    page=request.args.get('page',1)
    per_page=current_app.config['TT_ARTICLE_PER_PAGE']
    if q == '':
        flash('请输入球员的名称或者等级.', 'warning')
        return  redirect(url_for('main.index'))
    elif q<'9' and q>'0':
        pagination=Player.query.filter_by(rank=int(q)).order_by(Player.timestamp.desc()).paginate(page,per_page)
    elif q=='10':
        pagination = Player.query.filter_by(rank=int(q)).order_by(Player.timestamp.desc()).paginate(page, per_page)
    else:
        pagination=Player.query.whooshee_search(q).paginate(page,per_page)
    players=pagination.items
    website = Website.query.order_by(Website.timestamp.desc()).first()
    return render_template('main/index.html',pagination=pagination,players=players,user=user,website=website)



@main_bp.route('/send_advice',methods=['GET','POST'])
@login_required
def send_advice():

    form=AdviceForm()
    if form.validate_on_submit():
        body=form.body.data
        email=form.email.data
        username=current_user.name
        advice=Advice(body=body,username=username,email=email)
        db.session.add(advice)
        db.session.commit()
        flash('您的意见我们已收到，会及时做出回复','success')
        return redirect(url_for('main.index'))


    return render_template('main/advice.html',form=form)

@main_bp.route('/user_guide')
def user_guide():

    return render_template('main/user_guide.html')
