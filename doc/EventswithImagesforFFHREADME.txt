----------------------------------------------------------------
======Events With Images for FFH ======
Version: 1.0
Modifier/uploader: Ostar (complaints go to him!)
Original Creator: EmperorFool (thanks go to him!)


----------------------------------------------------------------
TABLE OF CONTENTS:
1. Description
2. Installation / Removal
3. How to Use
4. Known Bugs / Compatibility
5. Usage
6. Contact
7. Credits

----------------------------------------------------------------
1. DESCRIPTION

   This small Fall from Heaven "modmod" adds an images to the standard random events 
popup window. The image is specific to that image and (hopefully) adds more interst and flavor 
to the event. No rules are changed by this mod, nor are any events altered in any way. 
Also, this mod allows modders to add images (.dds files, specifically) to the event popup 
window.  Thanks to this mod, once installed the only changes modders have to make are in the XML.

----------------------------------------------------------------
2. INSTALLATION / REMOVAL

** This mod replaces your original 'CvGameCoreDLL.dll' in your FfH folder - so back it
up first!**

INSTALLATION:
Unzip this to your Fall from Heaven game folder (usually Program Files/Firaxis Games/
Beyond the Sword/Mods/Fall from Heaven. To do it manually:
1. Place 'CvGameCoreDLL.dll' in the Assets folder of your FfH directory.
2. Place 'CIV4EventSchema.xml' and 'CivEventTriggerInfo.xml' in the Assets/XML/Events folder of your 
FfH directory.
3. Place the EventImages folder in the Assets/Art folder. All the images created for FfH events 
are already in there, and you can add your own (see "How to Mod" below).
3. Place the remaining files (EventswithImagesforFFHREADME.txt and EventTriggerInfosTEMPLATE.txt)
in any folder you like, just remember where you put them, because you may want them as a 
reference! The CvGameCoreDLL folder holds the three changed files needed to recompile the DLL.

REMOVAL:
1. Delete 'CvGameCoreDLL.dll' from the folder you placed it in.
2. Delete 'CIV4EventSchema.xml' and 'CivEventTriggerInfo.xml' from the folder you placed it in.
3. Note that if you remove this functionality from FfH for any reason by deleting
the new 'CvGameCoreDLL.dll' and 'CIV4EventSchema.xml', ALL your event entries in your
EventTriggerInfo.xml file will have to be edited; they can no longer contain the <EventArt/>
Tag (see "How to Mod" section for more details).

----------------------------------------------------------------
3. HOW TO MOD

   This mod adds a new Tag, <EventArt/>, to the EventTriggerInfos.xml file using the
CIV4EventSchema.xml file.  To use this tag, however, you will have to add it to your
EventTriggerInfos.xml file or your mod will be unable to parse that file (in other words,
it won't work).  The form of this tag is as follows:
         <EventArt>Art\EventImages\imagename.dds</EventArt>

   The included TEMPLATE file shows where this should be placed.  All events in the 
Civ4EventTriggerInfo.xml need this tag or you will have XML errors. For those events that don't need 
or shouldn't have an image, just add <EventArt></EventArt> to the proper line (below </TriggerTexts> )
and no image will show and no XML errors will occur. 
Otherwise, add the new tag with your art as shown, and your image into the Art/EventImages folder,
and your new events will have the ability to display images!
Enjoy!

----------------------------------------------------------------
4. KNOWN BUGS / COMPATIBILITY

None as of this release.

Note, however, that this mod has ONLY been compiled/tested on Fall from Heaven version M.
It will not work with any other FfH mod that changes the DLL, like Fall Further. Other mods
like TweakMod that do not change the DLL are compatabile.
Hopefully a way will be found to code this in Python so a changed DLL will not be needed in the future.

----------------------------------------------------------------
5. USAGE

You are free to use/modify this code in any mod you create freely, however, please give proper
credit to EmperorFool, the coder of this mod.  NEVER re-release this code as your own
work, as it is not.

----------------------------------------------------------------
6. CONTACT

If you have any questions, problems, comments, suggestions, or complaints, feel free to send 
me a PM on CivFanatics.com; my screenname is "Ostar".

----------------------------------------------------------------
7. CREDITS

EmperorFool - Coding the original mod
RenegadeChicken - for creating this mod for BtS 
Willem - Idea for having Images on the Event Popups
