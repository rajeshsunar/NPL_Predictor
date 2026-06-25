All Men's Nepal Premier League match data in CSV format
=======================================================

The background
--------------

As an experiment, after being asked by a user of the site, I started
converting the IPL data from YAML into this CSV format. This then expanded
to include international T20s, for both women and men, before, finally,
expanding again to cover all matches we provide.

This particular zip folder contains the CSV data for...
  All Men's Nepal Premier League matches
...for which we have data, and is loosely based on the format that Retrosheet
uses for baseball, with some suitable hacks built in.

How you can help
----------------

Providing feedback on the data would be the most helpful. Tell me what you
like and what you don't. Is there anything that is in the JSON data that
you'd like to be included in the CSV? Could something be included in a better
format? General views and comments help, as well as incredibly detailed
feedback. All information is of use to me at this stage. I can only improve
the data if people tell me what does works and what doesn't. I'd like to make
the data as useful as possible but I need your help to do it. Also, which of
the 2 CSV formats do you prefer, this one or the newer "Ashwin" format?
Ideally I'd like to settle on a single CSV format so what should be kept
from each?

Finally, any feedback as to the licence the data should be released under
would be greatly appreciated. Licensing is a strange little world and I'd
like to choose the "right" licence. My basic criteria may be that:

  * the data should be free,
  * corrections are encouraged/required to be reported to the project,
  * derivative works are allowed,
  * you can't just take data and sell it.

Feedback, pointers, comments, etc on licensing are welcome.

The format of the data
----------------------

Full documentation of this CSV format can be found at:
  https://cricsheet.org/format/csv_original/
but the following is a brief summary of the details...

Each file has a 'version', multiple 'info' lines, and multiple 'ball' lines.
'version' is just 1.6.0, or 1.7.0 for now, and will change as I make changes.
The 'info' entries should be fairly self-explanatory but feel free to ask on
Mastodon (@cricsheet@deeden.co.uk) if you're unsure. If you look carefully
you may see some slight hints as to some data we'll be including in the full
data files in the future.

Each 'ball' line has the following fields:

  * The word 'ball' to identify it as such
  * Innings number, starting from 1
  * Over and ball
  * Batting team name
  * Batsman
  * Non-striker
  * Bowler
  * Runs-off-bat
  * Extras
  * Wides
  * No-balls
  * Byes
  * Leg-byes
  * Penalty
  * Kind of wicket, if any
  * Dismissed played, if there was a wicket

Matches included in this archive
--------------------------------

2025-12-13 - club - NPL - male - 1511008 - Sudur Paschim Royals vs Lumbini Lions
2025-12-11 - club - NPL - male - 1511007 - Lumbini Lions vs Biratnagar Kings
2025-12-10 - club - NPL - male - 1511006 - Kathmandu Gorkhas vs Lumbini Lions
2025-12-09 - club - NPL - male - 1511005 - Sudur Paschim Royals vs Biratnagar Kings
2025-12-07 - club - NPL - male - 1511004 - Karnali Yaks vs Janakpur Bolts
2025-12-06 - club - NPL - male - 1511003 - Chitwan Rhinos vs Pokhara Avengers
2025-12-06 - club - NPL - male - 1511002 - Sudur Paschim Royals vs Biratnagar Kings
2025-12-05 - club - NPL - male - 1511001 - Janakpur Bolts vs Lumbini Lions
2025-12-04 - club - NPL - male - 1511000 - Sudur Paschim Royals vs Chitwan Rhinos
2025-12-04 - club - NPL - male - 1510999 - Kathmandu Gorkhas vs Pokhara Avengers
2025-12-03 - club - NPL - male - 1510998 - Biratnagar Kings vs Lumbini Lions
2025-12-02 - club - NPL - male - 1510997 - Pokhara Avengers vs Karnali Yaks
2025-12-02 - club - NPL - male - 1510996 - Chitwan Rhinos vs Janakpur Bolts
2025-11-30 - club - NPL - male - 1510995 - Karnali Yaks vs Kathmandu Gorkhas
2025-11-29 - club - NPL - male - 1510994 - Janakpur Bolts vs Sudur Paschim Royals
2025-11-29 - club - NPL - male - 1510993 - Pokhara Avengers vs Lumbini Lions
2025-11-28 - club - NPL - male - 1510992 - Karnali Yaks vs Biratnagar Kings
2025-11-28 - club - NPL - male - 1510991 - Kathmandu Gorkhas vs Chitwan Rhinos
2025-11-27 - club - NPL - male - 1510990 - Pokhara Avengers vs Janakpur Bolts
2025-11-27 - club - NPL - male - 1510989 - Lumbini Lions vs Sudur Paschim Royals
2025-11-26 - club - NPL - male - 1510988 - Chitwan Rhinos vs Biratnagar Kings
2025-11-25 - club - NPL - male - 1510987 - Kathmandu Gorkhas vs Lumbini Lions
2025-11-24 - club - NPL - male - 1510986 - Sudur Paschim Royals vs Karnali Yaks
2025-11-24 - club - NPL - male - 1510985 - Biratnagar Kings vs Janakpur Bolts
2025-11-22 - club - NPL - male - 1510984 - Kathmandu Gorkhas vs Biratnagar Kings
2025-11-22 - club - NPL - male - 1510983 - Lumbini Lions vs Karnali Yaks
2025-11-21 - club - NPL - male - 1510982 - Sudur Paschim Royals vs Pokhara Avengers
2025-11-20 - club - NPL - male - 1510981 - Chitwan Rhinos vs Lumbini Lions
2025-11-19 - club - NPL - male - 1510980 - Sudur Paschim Royals vs Kathmandu Gorkhas
2025-11-18 - club - NPL - male - 1510979 - Biratnagar Kings vs Pokhara Avengers
2025-11-18 - club - NPL - male - 1510978 - Karnali Yaks vs Chitwan Rhinos
2025-11-17 - club - NPL - male - 1510977 - Janakpur Bolts vs Kathmandu Gorkhas
2024-12-21 - club - NPL - male - 1462670 - Sudur Paschim Royals vs Janakpur Bolts
2024-12-19 - club - NPL - male - 1462669 - Karnali Yaks vs Janakpur Bolts
2024-12-18 - club - NPL - male - 1462668 - Janakpur Bolts vs Sudur Paschim Royals
2024-12-18 - club - NPL - male - 1462667 - Karnali Yaks vs Chitwan Rhinos
2024-12-16 - club - NPL - male - 1462666 - Karnali Yaks vs Sudur Paschim Royals
2024-12-15 - club - NPL - male - 1462665 - Sudur Paschim Royals vs Pokhara Avengers
2024-12-15 - club - NPL - male - 1462664 - Biratnagar Kings vs Kathmandu Gurkhas
2024-12-14 - club - NPL - male - 1462663 - Chitwan Rhinos vs Janakpur Bolts
2024-12-14 - club - NPL - male - 1462662 - Pokhara Avengers vs Kathmandu Gurkhas
2024-12-13 - club - NPL - male - 1462661 - Biratnagar Kings vs Chitwan Rhinos
2024-12-13 - club - NPL - male - 1462660 - Karnali Yaks vs Lumbini Lions
2024-12-12 - club - NPL - male - 1462659 - Kathmandu Gurkhas vs Janakpur Bolts
2024-12-12 - club - NPL - male - 1462658 - Biratnagar Kings vs Pokhara Avengers
2024-12-11 - club - NPL - male - 1462657 - Kathmandu Gurkhas vs Lumbini Lions
2024-12-11 - club - NPL - male - 1462656 - Sudur Paschim Royals vs Janakpur Bolts
2024-12-10 - club - NPL - male - 1462655 - Pokhara Avengers vs Karnali Yaks
2024-12-10 - club - NPL - male - 1462654 - Lumbini Lions vs Chitwan Rhinos
2024-12-08 - club - NPL - male - 1462653 - Chitwan Rhinos vs Sudur Paschim Royals
2024-12-08 - club - NPL - male - 1462652 - Janakpur Bolts vs Lumbini Lions
2024-12-07 - club - NPL - male - 1462651 - Karnali Yaks vs Biratnagar Kings
2024-12-07 - club - NPL - male - 1462650 - Sudur Paschim Royals vs Lumbini Lions
2024-12-06 - club - NPL - male - 1462649 - Lumbini Lions vs Pokhara Avengers
2024-12-06 - club - NPL - male - 1462648 - Chitwan Rhinos vs Karnali Yaks
2024-12-05 - club - NPL - male - 1462647 - Sudur Paschim Royals vs Kathmandu Gurkhas
2024-12-05 - club - NPL - male - 1462646 - Pokhara Avengers vs Janakpur Bolts
2024-12-04 - club - NPL - male - 1462645 - Lumbini Lions vs Biratnagar Kings
2024-12-04 - club - NPL - male - 1462644 - Karnali Yaks vs Kathmandu Gurkhas
2024-12-03 - club - NPL - male - 1462643 - Chitwan Rhinos vs Pokhara Avengers
2024-12-03 - club - NPL - male - 1462642 - Sudur Paschim Royals vs Biratnagar Kings
2024-12-02 - club - NPL - male - 1462641 - Karnali Yaks vs Janakpur Bolts
2024-12-02 - club - NPL - male - 1462640 - Kathmandu Gurkhas vs Chitwan Rhinos
2024-11-30 - club - NPL - male - 1462596 - Biratnagar Kings vs Janakpur Bolts

Further information
-------------------

You can find all of our currently available data at https://cricsheet.org/

You can contact me via the following methods:
  Email   : stephen@cricsheet.org
  Mastodon: @cricsheet@deeden.co.uk
