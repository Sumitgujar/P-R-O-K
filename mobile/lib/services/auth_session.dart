import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class AuthSession {
  static const _key = 'prok_access_token';
  static const _storage = FlutterSecureStorage();

  Future<String?> readToken() => _storage.read(key: _key);
  Future<void> saveToken(String token) => _storage.write(key: _key, value: token);
  Future<void> clear() => _storage.delete(key: _key);
}
