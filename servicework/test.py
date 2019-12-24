    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = LoginForm()
    print(f"Form: {form}")
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        password_match_check = bcrypt.check_password_hash(user.password, form.password.data)
        print(f"User: {user}")
        if user and password_match_check:
            print(f"Entered password matches user password? {password_match_check}")
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            print(f"Entered password matches user password? {password_match_check}")
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = LoginForm()
    print(f"Form: {form}")
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)