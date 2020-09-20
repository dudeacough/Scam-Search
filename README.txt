Rental Scam Search


Have you ever been renting out a place and get contacted by someone who saw "your" listing on a site you didn't
post at asking if you would honor the cheaper advertisement they saw.  Usually this is followed by a reply notifying them the listing was a scam.

The intent of this program is to input a URL listing of a rental property from Zillow, copy the pictures and zip code.
Then perform a search on craiglist for rentals in the same zip code.  Then open up each of the search results on
craiglist and compare the images to the zillow URL.

There are easier ways to look for duplicate lisitng, for example an address search, but the intended purpose is a personal challenge to use image comparison.

The program will return a file containing the URLs of the craiglist sites that contain photos that are simliar to the
photos copied from the provided Zillow URL.

This project is intended for personal growth in coding with Python.

Instructions for Running Program:
Before running the program copy the URL of a rental listing on the Zillow website to your clipboard.  Note currently the rental listing must be located in the
Inland Empire, CA area because of the Craiglist website used for comparison.  Alternatively the zillow URL can be passed as a system argument when running.
The program will check for sys arguments, otherwise the clipboard contents will be used.

Future ideas for project:
- Add other comparison methods such as address or street number
- Optimize search on Craiglist for number of bedrooms and bathrroms
- Add multithreading and/or multiprocessing capabilities for image downloading and image comparison
- Provide support for areas outside the Inland Empire Craiglist areas
