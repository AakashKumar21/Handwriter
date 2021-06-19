![](/images/logo.png)

No one loves writing assignments (except some diamonds), so I made this tool to convert text into realistic looking handwritten text.

![visitors](https://visitor-badge.glitch.me/badge?page_id=handwriter_hsakaa)

# Output

![sample](/images/sample.jpeg)

# How to Install

- Download Python 3

- Clone this repo

- Inside repo folder install python dependencies by 

  ``` python
  python3 -m pip install -r requirements.txt
  ```

# How to use

## Creating custom font

You will need custom font for your handwriting, use https://www.calligraphr.com/, But this tool is free for only 75 characters, so what you can do is pay 😶, kidding. 
Create Two font packs for **Alphabets + Numbers** and **Symbols**. 
Now using a https://fontforge.org/ you can merge that two font into one.
Paste the font in repo folder

**Note:** Every font is different so it may require some tweaking in config.py.

## Using the CLI

``` python 
python3 handwriter.py text_file1.txt text_file_2.txt ... font_file.ttf
# For example
python3 handwriter.py assignment1.txt myfont.ttf
python3 handwriter.py assignment1.txt assignment2.txt myfont.ttf
```
### Add page numbers
``` python
python3 handwriter.py text_file1.txt text_file_2.txt ... font_file.ttf page_no
```

This will generate PDF files in pdf folder with same name as text file

### Adding new page 
Add this character '↩' (without quotes) in text file where you want new page to begin.

## Configuring output generation

For now you can change variables in config.py to suit your needs. Each handwriting may require different configuration.


## Todo
- [ ] Add GUI (WebApp or App)
- [ ] Background Transparency
- [ ] Add page resolution selection
- [ ] Add Background noise color option
- [ ] Add text color option
- [ ] Add fallback font option

# Need Contribution 

For making this tool more robust, adding GUI and making a good readme :).