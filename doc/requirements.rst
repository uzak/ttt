Product Requirements Document
=============================

:Project:   ttt
:Author:    Martin Uzak 
:Date:      26.12.2016
:Abstract:  The purpose of a this document is to define the scope of a simple
            and minimalistic time tracking tool. There is several tools around,
            yet I feel none of those provides a simple command line utility for
            handling text file based files containing time tracking information
            for a single user.

Dictionary
----------

==== =======
Word Meaning
==== =======
ttt  time tracking tool
==== =======

Requirements
------------

General
    * time tracking
    * command line based
    * assignment to categories (=cost centers)

Input
    * storage text file (editable in normal editor)
    * storable in git (can be attached to the sources of a project)
    * per single user
    * one or more input files
    * tracking: day, from - to, (time value), project, phase, description
    * keep track of comming_to and leaving work for computing the idle time?  -> better: daily default work hours 

Multiuser
    * usable for many users, analysis still should be possible for multiple users in the same project. but the user should not be bothered with storing his ID etc. in the files. **OPTIONAL** (= to be kept in mind yet not to be implemented)

Analysis
    * output: total worked for month <- year, month (default actual). for billing
    * output: distribution to project and its phases <- from, to date (default all). for analysis. it should be possible to feed this into CVS / excel etc.
