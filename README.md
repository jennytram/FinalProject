# FinalProject
Message board

# Frequently Asked Questions (FAQ)

# FOR ALL
## What is YardTalk?
YardTalk is an anonymous message board intended for use by students of Harvard College. It was developed in 2018 by Thomas Brooks and Jenny Tram, and it includes many features which are described in the remainder of this FAQ.

## How does YardTalk work?
YardTalk works in the CS50 IDE, or in any Flask environment in which the necessary packages are installed (the necessary packages are those imported at the top of the 'application.py' and 'helpers.py' files). YardTalk was tested and implemented in the CS50 IDE. A simple call to 'flask run' in the command line will launch our website locally.

The functionality of YardTalk uses Javascript for some front-end form validation, HTML, CSS (mainly from Boostrap), and SQL for handling all the data that goes in and out of YardTalk.

## Are all YardTalk users the same?
While the founding fathers championed the notion that all men are created equal, all YardTalk users are certainly not. This FAQ will be separated based on what information pertains to which class of users.

The first class, 'user,' can make posts, make comments, delete their own posts, like posts, and change their account settings. All accounts created by means of the normal registration process start out as users and only change status by the decision of the admin.

The second class, 'mod,' can do everything that a user can do, plus delete any post on YardTalk.

The third and highest class, 'admin,' is unique, meaning that there is only one admin. The admin can do everything that a mod can do in addition to being able to delete users' accounts and promote/demote users/mods, respectively, with some notable exceptions. The admin cannot change its screen name, which is permanently set to be 'admin.' The admin is also incapable of changing its own permissions (so that it does not accidentally demote itself).

For ease of the grader, 'database.db' comes preset with an admin whose credentials are as follows:
screen name: admin
password: 1


# FOR USERS+
## How do I sign up?
When you first visit the website, you will be redirected to the homepage. You can then click 'Register' in the top-right corner.

You will not be able to register with the same screen name as a user who has already registered, so do not fear an error message asking you kindly to pick another screen name.

In addition, your password must contain at least one digit.

## Once signed up, how can I log in again?
From the homepage, you can either click 'Log In' in the top-right corner next to 'Register' or click 'Get Started' in the box in the middle of the page.

## How do I log out of my account?
From any page on the website, you can log out of your account by clicking the 'Log Out' button in the top-right corner.

## How do I make a post?
From any page on the website, you can click 'Create a Post' in the top-left corner to make a post.

## How do I view the posts I have already made?
From any page on the site, you can click the 'Your Posts' button in the top-left corner of the page. This will show all of your posts. Alternatively, you can navigate to 'Account Settings' at the top-right of the screen and click 'View Your Posts.'

## How do I view everyone else's posts?
You can view everyone's posts in chronological order by either clicking the YardTalk logo at the top-left corner of the screen or by clicking 'All Posts' right next to 'Your Posts' in the top-left region.

## How do I view a specific other user's posts?
Locate the user whose posts you want to see in the list of all posts. Click on the user's screen name in the 'Posted By' column. From this screen, you will also be able to view that user's account privileges as described earlier in this FAQ.

## How do I like a post?
From any page where a post is displayed in the same tabular format as on the 'All Posts' page, you can click the 'Like' button in the 'Actions' column to like a post.

When you like a post, you will also be granted the option to unlike the post at any time by merely clicking the 'Unlike' button located in the exact spot where 'Like' was beforehand.

While a like is visible to other users, precisely who liked a post is not.

## How do I comment on a post?
Click the title of the post in the 'Title' column of the table in which the posts are listed. This will show the post in full mode. You can leave a comment in the textbox and click the 'Comment' button or, alternatively, 'Cancel' if you think you will regret your comment.

## How do I view other users' comments on a post?
Click the title of the post in the 'Title' column and read the comments! It is that easy.

## How do I change my screen name?
Click on 'Account Settings' in the top-right corner of the website and click 'Change Screen Name.' Be sure to remember you screen name!

## How do I change my password?
Click on 'Account Settings' in the top-right corner of the website and click 'Change Password.' Be sure to remember you password!

## How do I delete a post?
If you have made a post, it should show up in the tabular view with an additional 'Delete' action attached to the 'Actions' column. Clicking this will delete your post.

## How do I delete my account?
Navigate to 'Account Settings' in the top-right corner of the website and click 'Delete Account' at the bottom of the page. Remember, you cannot recover a deleted account.


# FOR MODS+
## How do I delete another user's post?
You will notice that every post, not only your own, comes with a 'Delete' action attached to it. Simply click 'Delete' to delete a post.


# FOR ADMIN
## How do I delete an account?
You will notice that every post comes with a 'Delete User' action. This action will delete the account of the user who made the related post. Be careful, as it is impossible to recover a deleted account.

Note: As the admin, you cannot delete your own account.

## How do I promote/demote a user?
You will notice that every post comes with a 'Change Privileges' action. This will promote or demote a user, depending on whether that user is a user or a mod, respectively.

Note: You cannot promote a mod, and you cannot change your own privileges as admin.

## Can I change my username?
No.
