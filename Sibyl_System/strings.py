on_string = """
Connected to seed!
Welcome {manager} {name}
Your validity is successfully verified.
"""

# Make sure not to change these too much
# If you still wanna change it change the regex too
scan_request_string = """
$BLOCKREQUEST
Block request to block this person!
**Spma Block manager:** {manager} 
**User blocked:** {spammer}
**Reason:** `{reason}`
**Block Source:** {chat}
**Target Message:** `{message}`
"""
forced_scan_string = """
$FORCED
**GENERAL:** {dev}
**Target:** {spammer}
**Reason:** `{reason}`
**Block Source:** {chat}
**Target Message:** `{message}`
"""

reject_string = """
$REJECTED
**Crime Coefficient:** `Under 100`
Not a target for enforcement action. 
The trigger will be locked.
"""

proof_string = """
**Case file for** - {proof_id} :
┣━**Reason**: {reason}
┗━**Message**
         ┣━[Nekobin]({paste})
         ┗━[DelDog]({url})"""

scan_approved_string = """
#LethalEliminator
**Target User:** {scam}
**Crime Coefficient:** `Over 300`
**Reason:** `{reason}`
**Manager:** `{manager}`
**Case Number:** `{proof_id}`
"""

bot_gban_string = """
#DestroyDecomposer
**Spam Block Manager:** `{manager}`
**Target User:** {scam}
**Reason:** `{reason}`
"""

# https://psychopass.fandom.com/wiki/Crime_Coefficient_(Index)
# https://psychopass.fandom.com/wiki/The_Dominator
