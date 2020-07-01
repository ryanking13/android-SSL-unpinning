# Android-SSL-unpinning

Simple python script which patches Android APK file to bypass SSL-pinning.

## Requirements

- Python3
- Java

## How to Run

```sh
python patch.py com.apk.file.to.patch.apk
# Patched APK file: com.apk.file.to.path.s.apk will be generated
```

## References

- [APKtool](https://ibotpeaches.github.io/Apktool/install/)
- [appium/sign](https://github.com/appium/sign)