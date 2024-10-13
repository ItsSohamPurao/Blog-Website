from app import app,db
from flask import render_template ,redirect , url_for, flash , request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User,Post,Comment, Like
from app.forms import RegisForms ,LoginForm


@app.route('/')
@app.route('/home')
def home_page():
    # Fetch all posts from the database
    posts = Post.query.all()
    user = User.query.all()
    # Pass the posts to a template to display them
    return render_template('home.html', title='Home', posts=posts , user=user)

@app.route('/register',methods = ["GET",'POST'])
def register_page():
    form = RegisForms()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')  # Captures the 'title' input
        text = request.form.get('text')    # Captures the 'text' textarea
        
        # Check if the title or text are empty
        if not title or not text:
            flash('Post and title cannot be empty', category='error')
        else:
            # Create a new Post object
            post = Post(content=text, title=title, user_id=current_user.id)
            
            # Add and commit the post to the database
            db.session.add(post)
            db.session.commit()
            
            flash('Post created!', category='success')
            return redirect(url_for('home_page'))  # Redirect after creation
    
    return render_template('post.html', user=current_user)

