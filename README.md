This is a Instagram scraper, which extracts the UserInfo and the last 12 post information. 

Given a list of usernames defined in user_names, the script will then extract the information. Within the directory a folder called "Profiles" is part. 
Within that folder, the script creates a folder for each username (or profile), and adds two csv files; UserInfo and PostInfo. 

UserInfo: 
- Username
- Following 
- Followers 
- Number of posts 
- Story Highlights 
- Profile Pic URL

PostInformation: 
Retrieves the last 12 posts
- Caption 
- Likes 
- Comments 
- Link to post 

This uses: 
- Selenium 
- BeautifulSoup 
- OS
- Pandas
- Json 
- Time 


