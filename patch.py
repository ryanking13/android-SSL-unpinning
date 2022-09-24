import os
import sys
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET
import subprocess as sp


def usage():
    print("Usage: python {} <APK file to patch>".format(sys.argv[0]))


def die(msg):
    print(msg)
    exit(1)


def patch_manifest_file(manifest_file):
    tree = ET.parse(manifest_file)
    root = tree.getroot()

    application = root.find("application")
    network_security_config = application.get(
        "{http://schemas.android.com/apk/res/android}networkSecurityConfig"
    )

    # if network security config attribute not exists, inject it
    if network_security_config is None:
        application.set(
            "{http://schemas.android.com/apk/res/android}networkSecurityConfig",
            "@xml/network_security_config",
        )

    with open(manifest_file, "w", encoding="utf-8") as f:
        f.write(ET.tostring(root, encoding="utf-8").decode())


def patch_network_security_config(config_file):
    cfg = """<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <debug-overrides>
        <trust-anchors>
            <certificates src="user" />
        </trust-anchors>
    </debug-overrides>
    <base-config cleartextTrafficPermitted="true">
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
        </trust-anchors>
    </base-config>
</network-security-config>
"""
    with open(config_file, "w") as f:
        f.write(cfg)


def main():

    shutil.which("java") or die("Java is not installed")

    if len(sys.argv) < 2:
        usage()
        exit(1)

    apktool = "apktool.jar"
    sign = "sign.jar"
    target_apk = sys.argv[1]

    if not target_apk.endswith(".apk"):
        print(
            "The extension of `{}` is not .apk, is it really a APK file?".format(
                target_apk
            )
        )
        exit(1)

    target_apk_unpacked = os.path.splitext(target_apk)[0]
    target_apk_repacked = target_apk_unpacked + ".repack.apk"

    # Unpacking
    sp.run(["java", "-jar", apktool, "d", target_apk])

    # Patch security config of APK to trust user rook certificate
    manifest_file = Path(target_apk_unpacked) / "AndroidManifest.xml"
    patch_manifest_file(str(manifest_file))
    config_file = (
        Path(target_apk_unpacked) / "res" / "xml" / "network_security_config.xml"
    )
    patch_network_security_config(str(config_file))

    # Repacking
    sp.run(
        ["java", "-jar", apktool, "b", target_apk_unpacked, "-o", target_apk_repacked]
    )

    # Signing
    sp.run(["java", "-jar", sign, "-a", target_apk_repacked])

    # Clean up
    shutil.rmtree(target_apk_unpacked)
    os.remove(target_apk_repacked)


if __name__ == "__main__":
    main()
