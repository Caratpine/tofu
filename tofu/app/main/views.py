from flask import render_template, redirect, url_for, abort, flash,current_app,request
from flask.ext.login import login_required, current_user
import requests
import json
from . import main
from .. import db
from ..models import User,Comment,Movie,MovieTag,Tag,MovieCollect
from .forms import PostForm,SearchForm,CommentForm



@main.route('/movies/<id>',methods=['GET','POST'])
def  moviepage(id):    
    m = Movie.query.filter_by(movie_id=id).first()
    flag = 3
    if current_user.is_authenticated:
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
                if current_user.is_authenticated:
                    comment = Comment(body=form.body.data,movies=m,author=current_user._get_current_object())
                    db.session.add(comment)
                    db.session.commit()
                    flash('Your comment has been published.')
                    return redirect(url_for('.moviepage', id=m.movie_id))
                else:
                    flash('you must login first.')
                    return redirect(url_for('auth.login'))     
        page = request.args.get('page', 1, type=int)
        pagination = m.comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=5,error_out=False)
        comments = pagination.items
        return render_template('moviepage.html',Info=Info,form = form,movies=[m],comments=comments, id = m.id,flag = flag,pagination=pagination)
    else:
        render_template('404.html')        



@main.route('/user/<key>')
@login_required
def user(key):
    user = User.query.filter_by(username=key).first()
    if user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    pagination = user.moviecollects.order_by(MovieCollect.id.desc()).paginate(page, per_page=5,error_out=False)
    moviecollects = pagination.items
    return render_template('userpage.html', user=user, moviecollects=moviecollects,pagination=pagination,username=key)


@main.route('/')
def index():
    movies = Movie.query.order_by(Movie.star.desc()).limit(30)
    movie = []
    mos = []
    for i in range(4):
        movie.append(movies[30-i])
    for i in range(4,8):
        mos.append(movies[30-i])    
    return render_template('index.html',movies = movie,mos = mos)

@main.route('/tags/<int:id>')
def tags(id):
    tag = Tag().query.filter_by(id = id).first()
    page = request.args.get('page', 1, type=int)
    pagination = MovieTag.query.order_by(MovieTag.id.asc()).filter_by(tag_id=id).paginate(page, per_page=5,error_out=False)
    movietags = pagination.items
    return render_template('tags.html',movietags = movietags,pagination=pagination,tag = tag)

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
            flash('You are collect this movie.')
            return redirect(url_for('.moviepage',id = movie.movie_id,flag = 0))
    else:
            flash("you have already collect this movie.")
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
            flash('You are not collect movie anymore.')
            return redirect(url_for('.moviepage',id = movie.movie_id,flag = 1))
        else:
           flash("You are not collect the movie.")
           return redirect(url_for('.moviepage',id = movie.movie_id,flag =1))
