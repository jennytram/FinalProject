# YardTalk: From Dream to Reality
## Overview
We wanted YardTalk to be as interactive as it could be within the given time constraints. That said, the main focus of our project was not necessarily aesthetic design or elaborating every method in 'application.py' as thoroughly as possible, but rather adding a lot of methods for different functionality in the website. Basically, we wanted YardTalk to resemble as closely as possible its real-life counterparts (or, if you would like to be overly generous to us, its competitors).

The video linked here briefly explains the functionality of our website: https://youtu.be/bhcbS8K1zZA

## The Basics
As explained in README.md, this project was implemented in Python, SQL, HTML, CSS, and JavaScript, roughly in descending order of importance for the website.

### Why Python?
Python is the foremost web programming language because it is both very high-level and, as a result, very dynamic and easy-to-use. This resulted in a focus on implementing functionality rather than parsing through hundreds of lines of code in search of a syntax error.

Flask, the library used for the execution of our project, is also unique to Python and extremely well-documented, so it was an easy choice.

### Why SQL?
SQL seemed like the obvious choice for storing the variable and distinct types of information that pass to/from YardTalk on a daily basis. Obviously it would not be viable to store every single post, like, comment, etc. as a variable instantiated at the start of every 'flask run' call (otherwise every time the serve went down, every post, like, comment, etc. would vanish with it).

SQL also makes it very easy to call information to be displayed in the HTML. Since the 'db.execute' command tends to return a dictionary, it was perfect for using a for-loop structure in Jinja to display, for example, posts on a page. In addition, the 'timestamp' type in SQL made it easy to both stamp and order every post and comment by date, as is most commonly done on websites such as Reddit and Facebook.

Most of the information seen on any given screen in YardTalk is likely to have originated in a SQL database. For example, when viewing 'All Posts,' you are really viewing a table with different attributes of a post from the table 'posts' in 'database.db' including the poster's screen name, the date it was posted, the number of likes and comments (actually implemented in separate global functions at the top of 'application.py' because of their database dependence), etc.

As a result of our reliance on SQL, you will notice that a large portion of many HTML files is either blank or filled with Jinja code which, when cross-referenced with the underlying functions in 'application.py,' can be seen to call elements of SQL tables.

### Why JavaScript?
We did not use JavaScript for many crucial functions of our website because a message board seemed to us to be a more server-oriented project, eschewing the need for a good deal fo client-side code. The majority of the JavaScript used was in the context of form validation, offering the user a more aesthetically pleasing way to remind the user to fill out the forms in an appropriate manner. Of course, to prevent malicious users from bypassing our forms, we had to implement much of this validation redundantly on the server side as well.

## User Hierarchies and the Admin Account
What is a message board without the ability to moderate it, and, in the worst-case scenario, punish bad users and moderators? We noticed that many of the social media platforms we were intending to emulate allowed for different levels of user with different levels of access to the website.

The exact nature of the user hierarchies is explained in README.md, and it offers a way to both moderate a broad base of users and to prevent wily moderators from getting out of hand via the omnipotent admin.

### Post Deletion
When a post is inappropriate or otherwise distasteful, there is generally no way to address this issue, especially with an anonymous service such as YardTalk. We decided that it only made sense to institute hierarchical checks on what users are allowed to post.

### Account Deletion
When a user repeatedly misuses his/her account to make inappropriate, harassing, or otherwise distasteful posts and comments, there is generally no action that can be taken other than deleting this user's individual posts. However, this might not deter future actions of this 'troll,' so we decided to implement account deletion by the admin so that there is one further obstacle in the way of a user getting out of hand.

In addition, what happens if moderators disagree with one another on how to do business and things get messy? The admin can delete the account of one of the moderators if this moderator is clearly behaving badly.

### Promotion/Demotion
If a moderator does something unbecoming of his/her status but a deletion is not warranted, what action is to be taken? We decided to implement account demotion by the admin to temporarily or permanently punish bad moderators.

What if a user shows him/herself to be mature and capable of diffusing situations in comments/posts? This user can be promoted to a moderator by the admin.

### Miscellaneous Admin Things
We chose to force the screen name of the admin to be 'admin' so that this user's absolute privilege would be obvious in every single post and comment, and this was the most straightforward way to do so given that we did not implement a method that displays user privileges next to every user's post.

We also did not want the admin to be able to delete his/her own account because it would defeat the purpose of placing all the administrative checks explained above on the moderators and users. For similar reasons, we did not want to grant the admin ability to demote him/herself.
