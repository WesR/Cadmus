# Cadmus
Making CUPS networked printers accessable through discord. 
Mainly for printing to a networked recipt printer with a max character width of 18.
Any text sent through the print command will be at max 18 characters long.

## Commands
The trigger is @botName. Ownership is determined by the userID specified in the .json.

**Open to anyone**
+ print <any length text>
+ print-doc <any document/image>
+ get printers
+ get default printer
+ get job queue
+ clear job queue
------------------------------
**Requires Permission:**
+ print-doc printer <printer-name> <any document/image>
------------------------------
**Admin Commands:**
+ clear printer queue <printer>
+ set default printer <name>
+ yes to auth prints to other printers

---------
defaultsAndKeys.json should look like:

```
{
    "discord": "yeahsomthinglong.yepp.morehashshouldbehere",
    "ownerid":  "9465198416516ish",
    "default-printer": "your-printer-name-locally"
}

```
