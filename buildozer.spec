[app]
title = Chaleco Masajeador
package.name = chaleco_masajeador
package.domain = com.espol
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0.0
requirements = python3,kivy,pyjnius,android
orientation = portrait
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25c
android.private_storage = True
android.theme = "@android:style/Theme.NoTitleBar"
android.copy_libs = 1
android.archs = arm64-v8a
android.enable_androidx = True
fullscreen = False

[buildozer]
log_level = 2
warn_on_root = 1
