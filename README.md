## Sample-rip

Sample-rip is a small python program to download free samples with.

The samples are from [musicradar](https://www.musicradar.com/news/tech/free-music-samples-royalty-free-loops-hits-and-multis-to-download) since they are all royalty-free, you may use them as you like in you DAW.


## Setup

sample-rip was tested on windows 7 using python 3.8

Before running the program, create a folder on your hard drive. This folder will contain all the sample packs downloaded. 

**WARNING:** Please make sure you have enough space on your hard drive to contain **50+ GB** of sample packs. Failing to do so could lead to unwanted situations/errors.


### Requirements

[requirements.txt](https://github.com/nortxort/sample-rip/blob/master/requirements.txt) contains a list of requirements which can be installed with `pip install -r /path/to/requirements.txt`


## Usage

Run `path/to/main.py`. When asked to enter path, enter the path to the folder you created. This will download all the sample packs from Musicradar.

When running main later on and pointing to the folder that contains samples, only samples not already downloaded will be downloaded.

Assuming a folder named `musicradar` was created, then the folder structure should be something like:

    musciradar/
        331 free '90s ambient samples/
        345 free Afrobeat samples/
        ....

After downloading the sample packs you will have to unpack them yourself, as they are all downlaoded as *.zip files.

## Todo

* Programmatically unpack zip files.

* Clean up. Delete unpacked zip files.

* Verbose?


## Author

* [nortxort](https://github.com/nortxort)


## License

The MIT License (MIT)
See [LICENSE](https://github.com/nortxort/sample-rip/blob/master/LICENSE) for more details.
