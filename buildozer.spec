[app]

# (str) Title of your application
title = Chaleco Masajeador

# (str) Package name
package.name = chalfeco_masajeador

# (str) Package domain (needed for android/ios packaging)
package.domain = com.espol

# (source.dir) Source directory (where your main.py is)
source.dir = .

# (source.include_exts) Source include extensions (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (version) app version (method 1) - just for display
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy,pyjnius
requirements = python3,kivy,pyjnius,android

# (str) Supported orientation (landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (list) Permissions
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25c

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (str) Android additional libraries to add
android.add_libs_armeabi_v7a = libs/armeabi-v7a/*.so
android.add_libs_arm64_v8a = libs/arm64-v8a/*.so

# (bool) Indicate if the application should be fullscreen or not
fullscreen = False

# (str) Presplash of the application (image)
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards using * for example:
# OUYA console example fremdomain just example some statements in your api.
# android.add_src = 

# (list) Pattern to whitelist for the whole project
android.whitelist = lib-dynload/termios.so

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (int) overrides automatic versionCode generation.
# android.version_code = 1

# (list) Pattern to whitelist for the whole project
#android.whitelist = lib-dynload/termios.so

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warnings (1 = yes, 0 = no)
warn_on_root = 1
