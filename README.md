## Sample-rip

Sample-rip is a small python program to download free samples from  [musicradar](https://www.musicradar.com/news/tech/free-music-samples-royalty-free-loops-hits-and-multis-to-download) with. Since all these samples are all royalty-free, you may use them as you like in your favorite DAW.


## Setup

sample-rip was tested on windows 7/10 using python 3.8

Before running the program, create a folder on your hard drive, e.g `musicradar`. This folder will contain all the sample packs downloaded. 

**WARNING:** Please make sure you have enough space on your hard drive to contain **50+ GB** of sample packs. Failing to do so could lead to unwanted situations/errors.

You may want to experiment with the configuration settings found in [main.py](https://github.com/nortxort/sample-rip/blob/master/main.py#L36) to speed up the overall process. I sudgest using the default settings first.

### Requirements

[requirements.txt](https://github.com/nortxort/sample-rip/blob/master/requirements.txt) contains a list of requirements which can be installed with `pip install -r /path/to/requirements.txt`


## Usage

Run `path/to/main.py`. When asked to enter path, enter the path to the folder you created. This will start the parsing process, once that is done you will be promted with some status information.

When running main later on and pointing to the folder that contains samples, only samples not already downloaded will be downloaded.

Assuming a folder named `musicradar` was created, then the folder structure should look something like:

    musciradar/
        musicradar-8-bit-bonanza-samples.zip
        musicradar-90s-ambient-samples.zip
	musicradar-303-style-acid-samples.zip
	musicradar-808-samples.zip
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
