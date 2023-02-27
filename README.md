# android-SSL-unpinning

A simple Python script which patches Android APK file to bypass SSL-pinning.

## Requirements

- Python3
- Java

## How to Run

```sh
git clone https://github.com/ryanking13/android-SSL-unpinning
cd android-SSL-unpinning

python patch.py com.apk.file.to.patch.apk
```

## How it works

1. Decompile the APK file using [APKtool](https://ibotpeaches.github.io/Apktool/install/)
2. Modify `AndroidManifest.xml` and `network_security_config.xml` to trust user certificate
3. Recompile the APK file using [APKtool](https://ibotpeaches.github.io/Apktool/install/)
4. Sign the APK file using [uber-apk-signer](https://github.com/patrickfav/uber-apk-signer)

## References

- [APKtool](https://ibotpeaches.github.io/Apktool/install/)
- [uber-apk-signer](https://github.com/patrickfav/uber-apk-signer)