# TwitterClone
This is a scaled down version of the micro-blogging site formerly known as Twitter. This website will feature signup, login, posting, replying to posts and different feeds of posts.

# Features
- **Signup**
Ask the user for their Email, UserName and Password. If their Email is already in use, show an error. The email should have an @ and a . the UserName and Password can not be blank If everything is OK, save their information to a database and automatically log them in.

- **Login**
Ask for their Email (or UserName) and Password. If something is wrong, show an error. If everything is OK log them into the system and redirect them to the Profile page.

- **Profile**
Pick a URL to show someone’s profile. This could be /profile/username or /@username or /u/username (whatever you’d like). Show the user’s photo, UserName and only their posts. If they haven’t uploaded a photo, show some generic photo. If someone is looking at their own profile, let them upload a photo to the system. Also, when looking at your own profile, a textbox and a button to write a new post.

- **Feed**
Show the recent 10 posts of everyone in the system. More recent should be on top. You should show the user’s photo next to the posts. Clicking on someone’s name should take you to their profile page.
 
- **Post View**
When a user clicks on the comments/reply button for a post, display the post with replies below it. Have a textbox and button to reply to the post.
