# General ClyphX utility commands for Ableton Live

### Summary
A few general ClyphX utility commands written for Ableton Live.


# Installation
- Have [ClyphX](http://forum.nativekontrol.com/thread/992/current-version-clyphx-live-9) installed and working in Ableton Live
- Do a `git checkout` of this repo in the folder where you installed the ClyphX scripts
(usually something like C:\ProgramData\Ableton\Live 10 Intro\Resources\MIDI Remote Scripts\ClyphX)
- Edit `MIDI Resource Scrits\ClyphX\ClyphXUserActions.py` and add the following lines to the bottom of the `__init__` method:


        import clyphx_gniputils.gniputils
        clyphx_gniputils.gniputils.register(self)
         
