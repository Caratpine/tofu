from flask import render_template, redirect, url_for, abort, flash,current_app,request
from flask.ext.login import login_required, current_user
from . import main
from .. import db
from ..models import User,Post,PostFollow,Follow,Comment,Movie,MovieTag,Tag
from .forms import PostForm,SearchForm,CommentForm


@main.route('/post/<int:id>',methods=['GET','POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,post=post,author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id))
    page = request.args.get('page', 1, type=int)
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=5,error_out=False)
    comments = pagination.items
    if current_user.postfollow.filter_by(post_id = id).first() is not None:
        flag = 0
    else:
        flag = 1
    return render_template('post.html', posts=[post], form=form,comments=comments, id = id,flag = flag,pagination=pagination)
    #return render_template('post.html',posts = [post],id = id,flag = flag,form = form)


@main.route('/user/<key>')
@login_required
def user(key):
    user = User.query.filter_by(username=key).first()
    if user is None:
    	abort(404)
    page = request.args.get('page', 1, type=int)
    pagination = user.postfollow.order_by(PostFollow.timestamp.desc()).paginate(page, per_page=5,error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, postfollows=posts,pagination=pagination,username=key)

    # posts = user.posts.order_by(Post.timestamp.desc()).all()
    # return render_template('user.html', user=user,posts = posts)


@main.route('/')
def index():
    movies = Movie.query.order_by(Movie.star.desc()).limit(4)
    mos = Movie.query.order_by(Movie.id.asc()).limit(4)
    return render_template('index.html',movies = movies,mos = mos)

@main.route('/tags/<int:id>')
def tags(id):
    tag = Tag().query.filter_by(id = id).first()
    page = request.args.get('page', 1, type=int)
    pagination = MovieTag.query.order_by(MovieTag.id.asc()).filter_by(tag_id=id).paginate(page, per_page=5,error_out=False)
    movietags = pagination.items
    return render_template('tags.html',movietags = movietags,pagination=pagination,tag = tag)        


@main.route('/search/<key>',methods=['GET','POST'])
def search(key):
    form = SearchForm()
    key = key
    if form.validate_on_submit():
        return redirect(url_for('.search',key = form.key.data))
    user = User.query.filter_by(username = key).first()
    if user is not None:
        page = request.args.get('page', 1, type=int)
        #current_app.config['FLASKY_POSTS_PER_PAGE']
        pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, per_page=5,error_out=False)
        posts = pagination.items
        return render_template('search.html', form=form, posts=posts,pagination=pagination,key=key)
    else:
        flash('your search have No Result !')
        return redirect(url_for('.index'))


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', key=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', key=username))


@main.route('/collect/<int:id>')
@login_required
def collect(id):
    post = Post.query.filter_by(id = id).first()
    if post is None:
            flash("not exist")
            return redirect(url_for('.index'))
    if current_user.postfollow.filter_by(post_id = id).first() is None:

            pf = PostFollow(user_id = current_user.id,post_id = id)
            db.session.add(pf)
            db.session.commit()
            flash('You are collect this post.')
            return redirect(url_for('.post',id = id,flag = 0))
    else:
            flash("you have already collect this post.")
            return redirect(url_for('.post',id = id,flag = 0))

@main.route('/uncollect/<int:id>')
@login_required
def uncollect(id):
        post = Post.query.filter_by(id = id).first()
        if post is None:
            flash("Not Exist.")
            return redirect(url_for('.index'))
        if current_user.postfollow.filter_by(post_id = id).first() is not None:
            pf = current_user.postfollow.filter_by(post_id = id).first()
            db.session.delete(pf)
            db.session.commit()
            flash('You are not collect post anymore.')
            return redirect(url_for('.post',id = id,flag = 1))
        else:
           flash("You are not collect the post.")
           return redirect(url_for('.post',id = id,flag =1))
