# Photo Editor

Implementation of simple photo editor

*example of using from terminal:*

```bash
python3 img_modifier.py -p temp.jpg color_filter=sepia --rotate=45 --resize=200,300
```

**All commands list:**

-  **-p path**:  path to initial image
-  **--rotate**: rotate image to N degrees
-  **--resize**: resize image to W and H
-  **--color_filter**: apply color filter (sepia, black_white, negative)
-  **--flip_top**: flip image from top to bottom
-  **--flip_right**: flip image from left to right

Also there is a UI built with PyQt5 which works for Windows, mac os and Linux.

Use **PyInstaller** to convert it

![ScreenShot](http://i.imgur.com/ZPd2Uzi.gif)

**used libs:**
- Pillow (PIL)
- PyQt5

to install all packages use **pip3 install -r requirements.txt**

> !this application was made as a training app so it can have bugs and bad optimization.

windows version:

![ScreenShot](https://github.com/shkolovy/simple-photo-editor/blob/master/win-version.png)
