from flask import render_template, redirect, url_for, abort, flash,current_app,request
from flask.ext.login import login_required, current_user
import requests
import json
from . import main
from .. import db
from ..models import User,Post,PostFollow,Follow,Comment,Movie,MovieTag,Tag,MovieCollect
from .forms import PostForm,SearchForm,CommentForm



@main.route('/movies/<id>',methods=['GET','POST'])
def  moviepage(id):    
    m = Movie.query.filter_by(movie_id=id).first()
    if current_user.moviecollects.filter_by(movie_id = m.id).first() is not None:
        flag = 0
    else:
        flag = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 \
        Safari/537.36'
    }
    url = 'http://api.douban.com/v2/movie/subject/'+id
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        movie = json.loads(r.text)
        year = movie['year']
        image_url = movie['images']['large']
        title = movie['title']
        tags = movie['genres']
        country = movie['countries']
        casts = movie['casts']
        avatars_list = list()
        for val in casts:
            avatars_list.append(val['name'])
        original_title = movie['original_title']
        summary = movie['summary']
        director_list = list()
        for val in movie['directors']:
            director_list.append(val['name'])
        Info = {
                    'year' :year,
                    'image_url':image_url,
                    'title':title,
                    'tags':tags,
                    'country':country,
                    'casts':avatars_list,
                    'directors':director_list,
                    'summary':summary,
                    'original_title':original_title       
        }    
        form = CommentForm()
        if form.validate_on_submit():
                comment = Comment(body=form.body.data,movies=m,author=current_user._get_current_object())
                db.session.add(comment)
                db.session.commit()
                flash('Your comment has been published.')
                return redirect(url_for('.moviepage', id=m.movie_id))
        page = request.args.get('page', 1, type=int)
        pagination = m.comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=5,error_out=False)
        comments = pagination.items
        return render_template('moviepage.html',Info=Info,form = form,movies=[m],comments=comments, id = m.id,flag = flag,pagination=pagination)
    else:
        render_template('404.html')        



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
    return render_template('post.html', posts=[post], form=form,comments=comments, id = m.id,flag = flag,pagination=pagination)
    #return render_template('post.html',posts = [post],id = id,flag = flag,form = form)


@main.route('/user/<key>')
@login_required
def user(key):
    return render_template('userpage.html')


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
    movie = Movie.query.filter_by(id = id).first()
    if movie is None:
            flash("not exist")
            return redirect(url_for('.index'))
    if current_user.moviecollects.filter_by(movie_id = id).first() is None:
            mc = MovieCollect(user_id = current_user.id,movie_id = id)
            db.session.add(mc)
            db.session.commit()
            flash('You are collect this post.')
            return redirect(url_for('.moviepage',id = movie.movie_id,flag = 0))
    else:
            flash("you have already collect this post.")
            return redirect(url_for('.moviepage',id = movie.movie_id,flag = 0))

@main.route('/uncollect/<int:id>')
@login_required
def uncollect(id):
        movie = Movie.query.filter_by(id = id).first()
        if movie is None:
            flash("Not Exist.")
            return redirect(url_for('.index'))
        if current_user.moviecollects.filter_by(movie_id = id).first() is not None:
            pf = current_user.moviecollects.filter_by(movie_id = id).first()
            db.session.delete(pf)
            db.session.commit()
            flash('You are not collect post anymore.')
            return redirect(url_for('.moviepage',id = movie.movie_id,flag = 1))
        else:
           flash("You are not collect the post.")
           return redirect(url_for('.moviepage',id = movie.movie_id,flag =1))
