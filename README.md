# Time Freeze

Application that automatically capture freezing moment from wide angle then generate a panorama viewer on Facebook/Google.

## Requirements

#### Python

Python and some python dependent packages.

Install dependencies using `pip install -r requirements.txt`

#### [ExifTool by Phil Harvey](https://www.sno.phy.queensu.ca/~phil/exiftool/index.html)

ExifTool is a platform-independent Perl library plus a command-line application for reading, writing and editing meta information in a wide variety of files.

ExifTool is necessary for updating GPano metadata process. 

On Windows, you will need **Git for Windows** package and also **MinGW** compiler to make/compile the package.

##### Installation

- Install Perl.
- Download ExifTool package and extract to your place.
- Open terminal/command line at that directory.
- Run Perl command to generate makefile: `perl Makefile.PL`.
- Run make command to test: `make test` or `mingw32-make test` (on Windows).
- Run make command to compile/run: `make install` or `mingw32-make install` (on Windows).

##### Setup project
Open `image_processing.py` then change value of `_EXIFTOOL` variable to your exiftool path or just run `app.py` with environment variable `EXIFTOOL` set correspondingly.

## Run

Execute `app.py` script with environment setup.