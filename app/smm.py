from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from flask_login import current_user, login_required
from app import db
from app.models import User
from app.forms import PostGeneratorForm, SettingsForm
from config import OPENAI_API_KEY
import os
from datetime import datetime, timedelta
from social_stats.vk_stats import VKStats

smm = Blueprint('smm', __name__)

from generators.text_gen import PostGenerator as TextPostGenerator
from generators.image_gen import ImageGenerator as ImagePostGenerator
from social_publishers.vk_publisher import VKPublisher

@smm.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@smm.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.vk_api_key = form.vk_api_key.data
        current_user.vk_group_id = form.vk_group_id.data
        db.session.commit()
        flash('Your settings have been updated!', 'success')
        return redirect(url_for('smm.settings'))
    elif request.method == 'GET':
        form.vk_api_key.data = current_user.vk_api_key
        form.vk_group_id.data = current_user.vk_group_id
    return render_template('settings.html', title='Settings', form=form)

@smm.route("/post_generator", methods=['GET', 'POST'])
@login_required
def post_generator():
    form = PostGeneratorForm()
    post_text = session.get('post_text')
    image_url = session.get('image_url')
    post_posted = session.get('post_posted', False)

    if form.validate_on_submit():
        tone = form.tone.data
        topic = form.topic.data
        generate_image_flag = form.generate_image.data
        autopost = form.autopost.data

        post_generator = TextPostGenerator(openai_key=OPENAI_API_KEY, tone=tone, topic=topic)
        post_text = post_generator.generate_post()

        if generate_image_flag:
            image_generator = ImagePostGenerator(openai_key=OPENAI_API_KEY)
            image_description = post_generator.generate_post_image_description()
            image_url = image_generator.generate_image(image_description)

        session['post_text'] = post_text
        session['image_url'] = image_url
        session['autopost'] = autopost  # Store the autopost value

        if autopost:
            vk_publisher = VKPublisher(current_user.vk_api_key, current_user.vk_group_id)
            vk_publisher.publish_post(post_text, image_url)
            flash('Post generated and posted to VK successfully!', 'success')
            session['post_posted'] = True  # Mark as posted
        else:
            session['post_posted'] = False  # Mark as not posted

    return render_template('post_generator.html', title='Post Generator', form=form, post_text=post_text, image_url=image_url, post_posted=post_posted, autopost=session.get('autopost'))

@smm.route("/post_to_vk", methods=['POST'])
@login_required
def post_to_vk():
    post_text = session.get('post_text')
    image_url = session.get('image_url')

    if post_text and not session.get('post_posted', False):
        vk_publisher = VKPublisher(current_user.vk_api_key, current_user.vk_group_id)
        vk_publisher.publish_post(post_text, image_url)
        flash('Post successfully published to VK!', 'success')
        session['post_posted'] = True  # Mark as posted
    else:
        flash('No post data found or post has already been published. Please generate a new post.', 'danger')

    return redirect(url_for('smm.post_generator'))

@smm.route("/new_post", methods=['GET'])
@login_required
def new_post():
    session.pop('post_text', None)
    session.pop('image_url', None)
    session.pop('post_posted', None)
    session.pop('autopost', None)
    return redirect(url_for('smm.post_generator'))

@smm.route("/vk_stats")
@login_required
def vk_stats():
    vk_stats = VKStats(current_user.vk_api_key, current_user.vk_group_id)

    # Define the date range (last 7 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Format dates as strings
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    stats = vk_stats.get_stats(start_date_str, end_date_str)

    # Convert stats to list of dictionaries
    data = vk_stats.convert_stats_to_list(stats)

    return render_template('vk_stats.html', title='VK Stats', data=data)


