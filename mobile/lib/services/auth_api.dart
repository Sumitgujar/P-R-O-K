import 'dart:convert';
import 'dart:io';

import '../core/config/app_config.dart';
import '../models/current_user.dart';

class AuthException implements Exception {
  const AuthException(this.message);
  final String message;
}

class AuthApi {
  Future<String> login(String email, String password) async {
    final result = await _request('/auth/login', method: 'POST', body: {'email': email, 'password': password});
    return result['access_token'] as String;
  }

  Future<CurrentUser> currentUser(String token) async {
    final result = await _request('/auth/me', token: token);
    return CurrentUser.fromJson(result);
  }

  Future<void> logout(String token) async {
    await _request('/auth/logout', method: 'POST', token: token);
  }

  Future<Map<String, dynamic>> _request(String path, {String method = 'GET', Map<String, dynamic>? body, String? token}) async {
    final client = HttpClient();
    try {
      final request = await client.openUrl(method, Uri.parse('${AppConfig.apiBaseUrl}$path'));
      request.headers.contentType = ContentType.json;
      if (token != null) request.headers.set(HttpHeaders.authorizationHeader, 'Bearer $token');
      if (body != null) request.write(jsonEncode(body));
      final response = await request.close();
      final content = await utf8.decodeStream(response);
      final parsed = content.isEmpty ? <String, dynamic>{} : jsonDecode(content) as Map<String, dynamic>;
      if (response.statusCode < 200 || response.statusCode >= 300) throw AuthException(parsed['detail'] as String? ?? 'Request failed');
      return parsed;
    } on SocketException {
      throw const AuthException('Unable to reach the PROK API.');
    } finally {
      client.close(force: true);
    }
  }
}
