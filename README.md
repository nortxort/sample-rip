## Sample-rip

Sample-rip is a small python program to download sample packs from  [musicradar](https://www.musicradar.com/news/tech/free-music-samples-royalty-free-loops-hits-and-multis-to-download) with. Since all these samples are all royalty-free, you may use them as you like in your favorite DAW. The sample packs are downloaded as zip files, and will need to be unzipped once downloaded.

**NOTE:** It will take a lot of time to download all sample packs since they are about 75GB in total. (14/12/2024)

I have provided a [urls](https://github.com/nortxort/sample-rip/blob/master/urls.txt) file containing links to all the zip files.


## Setup

sample-rip was tested on windows 10 using python 3.12

Before running the program, create a folder on your hard drive, e.g `musicradar`. This folder will contain all the sample packs downloaded. 

**WARNING:** Please make sure you have enough space on your hard drive to contain **75+ GB** of sample packs. Failing to do so could lead to unwanted situations/errors.

You may want to experiment with the configuration settings found in [main.py](https://github.com/nortxort/sample-rip/blob/master/main.py#L38) to speed up the overall process. I sudgest using the default settings first. 

As default, only 5 sample pages will be processed. To processed all sample pages set **MAX\_SAMPLE\_PAGES\_URLS** to 0.


### Requirements

[requirements.txt](https://github.com/nortxort/sample-rip/blob/master/requirements.txt) contains a list of requirements which can be installed with `pip install -r /path/to/requirements.txt`


## Usage

Run `path/to/main.py`. When asked to enter path, enter the full path to the folder you created. e.g `C:\MySamples\musicradar` This will start the parsing process, once that is done you will be promted with some status information.

When running main later on and pointing to the folder that contains samples, only samples not already downloaded will be downloaded. 

**NOTE:** This is only possible, if the sample packs are not renamed/moved after downloading/unpacking them.

Assuming a folder named `musicradar` was created, then the folder structure should look something like:

    musciradar/
        musicradar-8-bit-bonanza-samples.zip
        musicradar-90s-ambient-samples.zip
        musicradar-303-style-acid-samples.zip
        musicradar-808-samples.zip
        ....

After downloading the sample packs you will have to unpack them yourself, as they are all downlaoded as *.zip files.

## Todo

* Implement database storage.

* Programmatically unpack zip files and delete the zip file.

## Author

* [nortxort](https://github.com/nortxort)


## License

The MIT License (MIT)
See [LICENSE](https://github.com/nortxort/sample-rip/blob/master/LICENSE) for more details.
