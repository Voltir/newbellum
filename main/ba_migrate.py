#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

import MySQLdb
import HTMLParser
import time
from datetime import datetime

from django.utils.timezone import utc
from django.db import transaction

from django.conf import settings
from django.contrib.auth.models import User,Group
from django.core.management.base import BaseCommand, CommandError
from django.db.models.signals import post_save
from djangobb_forum import settings as forum_settings
from djangobb_forum.models import Category, Forum, Profile, TZ_CHOICES, Post, Topic, Attachment
from djangobb_forum import signals as djangobb_signals

from guardian.shortcuts import assign

############ TODO: Migrate Attachments!
############ TODO: Poster IP for posts!

con = MySQLdb.connect("localhost","root","root","testba",use_unicode=True)
con.query("SET character_set_client = utf8")
con.store_result()
h = HTMLParser.HTMLParser()

#Timestamps from nuke_* tables are *not* utc...
#They are "gmtime" which kind of misses the whole point
#of how to properly store time in a timezone agnostic way
def defoobar(timestamp):
    #for now, do the easy thing and just subtract out
    #the added offset (the server was on eastern time so it added
    #4*3600 seconds to the actual unix utc timestamp)
    #I should probably figure out if DST plays a role
    #and fix the time accordingly..
    # (Does php Date('Z') take DST into account?)
    return timestamp - 3600*4 #actual utc timestamp, ignoring DST..

#A lot of this script was stolen from phpbb2djangobb.py (Volt)
def disable_auto_fields(model_class):
    """
    Hack: It's needed to disable "auto_now_add" to set a old datetime
    
    see also: http://stackoverflow.com/questions/7499767/temporarily-disable-auto-now-auto-now-add
    """
    ATTR_NAMES = ("auto_now", "auto_now_add")
    for field in model_class._meta.local_fields:
        for attr_name in ATTR_NAMES:
            if getattr(field, attr_name, False) == True:
                print "Disable '%s' on field %s.%s" % (attr_name, model_class.__name__, field.name)
                setattr(field, attr_name, False)

def migrate(con):

    #check_attachment_path()

    # disable DjangoBB signals for speedup
    post_save.disconnect(djangobb_signals.post_saved, sender=Post, dispatch_uid='djangobb_post_save')
    post_save.disconnect(djangobb_signals.topic_saved, sender=Topic, dispatch_uid='djangobb_topic_save')

    #disable_auto_fields(Forum)
    disable_auto_fields(Topic)
    disable_auto_fields(Post)

    groups = migrate_groups(con)
    users, moderators = migrate_users(con)
    
    migrate_user_groups(con,users,groups)
    categories = migrate_categories(con)
    forums = migrate_forums(con,categories)
    migrate_auth(con,forums,groups)

    topics = migrate_topics(con,users,forums)
    migrate_posts(con,users,topics,forums)
    
    # needed if signals disabled, see above
    update_topic_stats()
    update_forum_stats()

def migrate_groups(con):
    groups = {}
    con.query("select * from nuke_bbgroups")
    result = con.store_result()
    with transaction.commit_on_success():
        for r in result.fetch_row(0,1):
            group, created = Group.objects.get_or_create(name=r["group_name"])
            if created:
                group.save()
            groups[r["group_id"]] = group
    return groups

def migrate_users(con):
    moderators = []
    user_dict = {}
    
    con.query("select * from nuke_users;")
    result = con.store_result()
    with transaction.commit_on_success():
        for r in result.fetch_row(0,1):
            name = r["name"].split()
            first = r["name"]
            last = ''
            if len(name) == 2:
                first = name[0]
                last = name[1]
		
            unix_timestamp = defoobar(int(r["user_regdate"]))
            reg_date = datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=utc)

            django_user, created = User.objects.get_or_create(
			    username=h.unescape(r["username"]),
				password=r["user_password"],
                defaults={
                    "email":h.unescape(r["user_email"]),
                    "first_name":first,
                    "last_name":last,
                    "is_staff": False,
                    "is_active": True,
                    "is_superuser": False,
                    "date_joined": reg_date,
                }
            )
            if created:
                django_user.save()
            else:
                #print("\tUser '%s' exists." % django_user)
                pass
            #if phpbb_user.group in moderator_groups:
            #    self.stdout.write("\t *** Mark user '%s' as global forum moderator\n" % phpbb_user)
            #    moderators.append(django_user)

            user_dict[r["user_id"]] = django_user

            profile_data = {}
            if r["user_website"] != None:
                profile_data["site"] = r["user_website"]
            if r["user_posts"] != None:
                 profile_data["post_count"] = int(r["user_posts"])
            #if r["user_timezone"] != None:
            #    profile_data["time_zone"] = int(r["user_timezone"]),
                 
            user_profile, created = Profile.objects.get_or_create(
                user=django_user,
                defaults=profile_data
            )
            if created:
                user_profile.save()
            else:
                pass

    return user_dict,moderators

def migrate_user_groups(con,users,groups):
    con.query("select * from nuke_bbuser_group")
    result = con.store_result()
    with transaction.commit_on_success():
        for r in result.fetch_row(0,1):
            if r["user_id"] not in users or r["group_id"] not in groups:
                continue
            user = users[r["user_id"]]
            user.groups.add(groups[r["group_id"]])
            user.save()

def migrate_categories(con):
    categories = {}
    con.query("select * from nuke_bbcategories")
    result = con.store_result()
    with transaction.commit_on_success():
        for r in result.fetch_row(0,1):
            cat, created = Category.objects.get_or_create(
                name=h.unescape(r["cat_title"]),
                position=int(r["cat_order"])
            )
            if created:
                cat.save()
            categories[r["cat_id"]] = cat
    return categories

def migrate_forums(con,categories):
    forums = {}
    con.query("select * from nuke_bbforums")
    result = con.store_result()
    with transaction.commit_on_success():
        for r in result.fetch_row(0,1):
            cat = categories[r["cat_id"]]
            forum, created = Forum.objects.get_or_create(
                name=h.unescape(r["forum_name"]),
                description=h.unescape(r["forum_desc"]),
                category=cat)
            if created:
                forum.save()
            forums[r["forum_id"]] = forum
    return forums

def migrate_topics(con,users,forums):
    topics = {}
    con.query("select * from nuke_bbtopics") #where forum_id=27")
    result = con.store_result()
    with transaction.commit_on_success():
        for r in result.fetch_row(0,1):
            if r["forum_id"] not in forums or r["topic_poster"] not in users:
                print "Unknown forum_id or topic_poster!"
                continue
            unix_timestamp = defoobar(int(r["topic_time"]))
            topic_time = datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=utc)
            topic, created = Topic.objects.get_or_create(
                forum=forums[r["forum_id"]],
			    name=h.unescape(r["topic_title"]),
                user=users[r["topic_poster"]],
                created=topic_time,
                views=r["topic_views"],
            )
            if created:
                topic.save()
            topics[r["topic_id"]] = topic
    return topics
            
def migrate_posts(con,users,topics,forums):
    con.query("select * from nuke_bbposts as a, nuke_bbposts_text as b where a.post_id = b.post_id") #and a.forum_id=27")
    result = con.store_result()
    count = 0
    foo = 0
    with transaction.commit_on_success():
        for r in result.fetch_row(0,1):
            foo += 1

            if r["poster_id"] not in users:
                print "Poster id???",r["poster_id"]
                count += 1
                continue

            if r["topic_id"] not in topics:
                print "Topic id???",r["topic_id"]
                continue

            if foo % 1000 == 0:
                print foo

            unix_timestamp = defoobar(int(r["post_time"]))
            post_time = datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=utc)
            edit_time = None
            edit_user = None
            if r["post_edit_count"] > 0 and r["post_edit_time"] > 0:
                edit_time = datetime.utcfromtimestamp(int(r["post_edit_time"])).replace(tzinfo=utc)
                #The user who made the edit doesnt appear to be stored in nuke...
                edit_user = users[r["poster_id"]]

            post, created = Post.objects.get_or_create(
                topic=topics[r["topic_id"]],
                user=users[r["poster_id"]],
                body=r["post_text"],
                created=post_time,
                updated=edit_time,
                updated_by=edit_user,
                markup="bbcode",
                #user_ip=r["poster_ip"],
            )
            if created:
                post.save()
                

    print count
    print foo

def migrate_auth(con,forums,groups):
    con.query("select * from nuke_bbauth_access")
    result = con.store_result()
    with transaction.commit_on_success():
        for r in result.fetch_row(0,1):
            if r["forum_id"] not in forums or r["group_id"] not in groups:
                print "???????????????????",r["forum_id"] in forums, r["group_id"] in groups
                continue
            forum = forums[r["forum_id"]]
            group = groups[r["group_id"]]
            if r["auth_read"] == 1 or r["auth_view"] == 1:
                assign('djangobb_forum.view_forum',group,forum)

            if r["auth_post"] == 1:
                assign('djangobb_forum.add_post',group,forum)
            
            if r["auth_delete"] == 1:
                assign('djangobb_forum.delete_post',group,forum)

            if r["auth_attachments"] == 1:
                assign('djangobb_forum.add_attachment',group,forum)

            if r["auth_download"] == 1:
                assign('djangobb_forum.download_attachment',group,forum)
           
            if r["auth_mod"] == 1: 
                assign('djangobb_forum.moderate_forum',group,forum)

            forum.save()

def update_topic_stats():
    topics = Topic.objects.all()
    total = topics.count()
    with transaction.commit_on_success():
        for i,topic in enumerate(topics):
            queryset = Post.objects.only("created","updated").filter(topic=topic)
            topic.post_count = queryset.count()
            try:
                last_post = queryset.latest("created")
            except Post.DoesNotExist:
                pass
            else:
                topic.last_post = last_post
                if last_post.updated:
                    topic.updated = last_post.updated
                else:
                    topic.updated = last_post.created
            if i % 1000 == 0:
                print "Updating topic %d" % i

            topic.save()

def update_forum_stats():
    with transaction.commit_on_success():
        for forum in Forum.objects.all():
            queryset = Post.objects.all().filter(topic__forum=forum)
            forum.post_count = queryset.count()
            try:
                forum.last_post = queryset.latest("created")
            except Post.DoesNotExist:
                pass
            queryset = Topic.objects.all().filter(forum=forum)
            forum.topic_count = queryset.count()
            forum.save()

migrate(con)
