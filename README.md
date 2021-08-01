# pygame-crt

This is a small library to make simple, textmode, programs in the frame buffer, directly, using PyGame. It follows the logic of the old Turbo Pascal CRT unit, so it uses functions like write, readkey, gotoxy etc. This way, you can easily create textmode apps.

The library uses Bitmap fonts, to be able to represent 100% accurate ansi/ascii graphics, many fonts included. It also supports mouse clicks, allowing you to make use of the library in touchscreens ;)

I made it to make programs in my Raspberry Pi, with a touch screen attached to it, with out the need to have an X-Windows system installed. I hope you'll find it usefull.
