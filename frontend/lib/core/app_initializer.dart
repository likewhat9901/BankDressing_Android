import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';

import 'notification/fcm_service.dart';
import 'logger/logger_service.dart';

class AppInitializer {
  static Future<void> init() async {
    try {
      await Firebase.initializeApp();
      FirebaseMessaging.onBackgroundMessage(
        FCMService.backgroundHandler,
      );
      await FCMService().init();
      LoggerService.info('Firebase', 'Firebase 초기화 완료');
    } catch (e) {
      LoggerService.error('Firebase', 'Firebase 초기화 실패: $e', e);
    }
  }
}
