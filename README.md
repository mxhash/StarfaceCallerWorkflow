# StarfaceCallWorkflow

This workflow places a call on the starface for a dedicated SIP device

![Screenshot Of Alfred With Device](doc/alfred1.png)

![Screenshot Of Alfred Without Device](doc/alfred2.png)

## Prerequisites

This workflow uses python 2.7 and xmlrpclib >= 1.0.1

## Configuration

Place a credentials file in your HOME directory ```~/.starface_credentials``` and add the following content to it:

    1. Line: URL of the starface appliance
    2. Line: Login
    3. Line: Password
    4. Line: Preferred device (optional)
 
 Finally the file looks like this:
 
 ```bash
$ cat /Users/mhein/.starface_credentials
https://mystarface.foo.bar
0123
PASSWORD
SIP/16
```

## Appendix

### call.py

The workflow contains a python script to place the call:

```bash
$ python call.py --help
usage: call.py -n +49911777-777 [ -d SIP/dev ] [ -h ]

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        Call number
  -d DEVICE, --device DEVICE
                        Place call on device, e.g. SIP/mydevice
  -c CREDENTIAL, --credential CREDENTIAL
                        Credential file
```
