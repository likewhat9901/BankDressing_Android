# @firebase
# Flutter 관련
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }

# Firebase
-keep class com.google.firebase.** { *; }
-dontwarn com.google.firebase.**

# HTTP 클라이언트
-dontwarn okhttp3.**
-dontwarn okio.**

# Google Play Core (deferred components)
-dontwarn com.google.android.play.core.**