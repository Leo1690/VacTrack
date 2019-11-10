

# VacTrack

### Live Demo:

[Check the live demo here](https://vacuumatjacobs.appspot.com)
## Inspiration
Climbing six floors of stairs every week to get a vacuum cleaner from our college office always made us wonder if cleaning our room really took precedence over our comfort? Still going through all this effort just to find out about someone else already borrowing it inspired us to take this initiative.
## What it does
VacTrack is a multi-platform tracking interface that checks the availabilty of vacuum cleaners in our residential college offices, and informs the students via two different platforms: a Google Cloud-based website and an SMS-based text-and-respond system.
## How we built it
We built two devices - one connected to the vacuum, and the other located in a fixed position in the college office, both built using Raspberry Pi. As long as the vacuum is within the vicinity of the fixed 'anchor', its state will be considered available to students, and as soon as it leaves the vicinity of the college office, the time since it left will start counting. This information will be available to students over the web, and through an SMS interface, where they can text a specified phone number and get a reply of the vacuum's current state.
## Challenges we ran into
There were a handful of tasks that were time consuming; the configuration of Wifi Direct via Raspberry Pi was the first challenge we faced. Secondly, getting the real time data from the computer and uploading it to Dropbox, and then using the web interface, based in Flask, on Google Cloud to interpret those values and display them to the users. 

Last but not the least, the biggest problem was Sleep Deprivation.
## Accomplishments that we're proud of
Overcoming Google Cloud's strict storage restrictions, building a beautiful UI for the web interface, making a smart SMS system, working wire-to-wire to make the Raspberry Pi work, and most importantly, interacting and synergizing with people I never met before to build something we'll always be proud of!
## What we learned
Teamwork, confidence, smart decision making, and stumbling across new technologies!
## What's next for VacTrack
The idea is to expand the core idea of keeping check-and-balance to other applications like tracking kids, or your luggage at the airport, for example.
