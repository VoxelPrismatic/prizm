print("""
All the info is at https://discordapp.com/developers/applications/
CREATE A BOT -------------
  1. Navigate to the above URL
  2. Click on `New Application` or similar in upper right
  3. Enter the name
  4. Add a PFP
  5. Go to `Bot` in the left panel
  6. Click on `Create bot` or similar

GET THE TOKEN -----------
  1. Navigate to the above URL
  2. Click on your bot
  3. Go to `Bot` in the left panel
  4. Click on `Copy` under the bot's name

""")
token = input("[discord] Bot token ] ")

print("""
All the info is at https://old.reddit.com/prefs/apps/
CREATE A BOT -------------
  1. Navigate to the above URL
  2. Click on `create another app...` or similat on the bottom of the page
  3. Enter the name of the app
  4. Click on `script`, so you don't get screwed
  5. Put anything in the description
  6. Leave the `about url` blank
  7. Put any random but valid format website for `redirect uri`
     Example: `https://thiswebsitedoesnotexist.xyz`
  8. Click on `create app` on the bottom of the page

GET THE TOKEN AND STUFF --
  1. Navigate to the above URL
  2. Find your bot and click on `edit`
  3. The bot ID will be under the name
  4. The bot secret will be labeled as such
  5. The bot name will be big and blue
""")
name = input("[reddit] Bot name ] ")
rid = input("[reddit] Bot ID ] ")
secret = input("[reddit] Bot secret ] ")
u_ = "/u/" + input("[reddit] Your reddit name ] /u/")
print("\n\nSaving data...")
path = open("loc.txt").read()
if path[-1] != "/":
    path += "/"
open(path + "secrets.txt", "w+").write(token)
lines = open(path + "util/praw_util.py").read().split("\n")
lines[8] = f"        client_id = '{rid}',"
lines[9] = f"        client_secret = '{secret}',"
lines[10] = f"        user_agent = '{name} by {u_}'"
open(path + "util/praw_util.py", "w").write("\n".join(lines))
