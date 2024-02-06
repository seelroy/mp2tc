
# mp2tc

A Python script to convert MakePlace furniture lists into importable Teamcraft URLs. URL is printed to terminal and exported to a text file.





## Installation/Setup

To get started ensure that you have Python 3.12 installed: https://www.python.org/downloads/

Your mileage may vary with older versions of Python.

* Download the files in the repository
* Extract them
* Open a terminal/command prompt in the directory
* Run `pip install -r requirements.txt`

Next head over to https://xivapi.com/

* Login via Discord
* Once back to xivapi, click "Dev Account"
* Grab your api key under "API Access"
* Open `mp2tc.py` in your text editor of choice
* Find `client = pyxivapi.XIVAPIClient(api_key="key")`, which should be about line 12
* Replace "key" with your api key
    
## Usage & Example

Run `py mp2tc.py` and enter the filename of the furniture list.

![mp2tc example](/img/example.gif)

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

