import 'dart:convert';
import 'dart:io';

import '../core/config/app_config.dart';

class ApiException implements Exception {
  const ApiException(this.message, {this.statusCode});
  final String message;
  final int? statusCode;
}

class UnauthorizedException extends ApiException {
  const UnauthorizedException() : super('Your session has expired. Please sign in again.', statusCode: 401);
}

class ApiClient {
  Future<Map<String, dynamic>> request(
    String path, {
    String method = 'GET',
    Map<String, dynamic>? body,
    String? token,
  }) async {
    final client = HttpClient();
    try {
      final request = await client.openUrl(method, Uri.parse('${AppConfig.apiBaseUrl}$path'));
      request.headers.contentType = ContentType.json;
      if (token != null) request.headers.set(HttpHeaders.authorizationHeader, 'Bearer $token');
      if (body != null) request.write(jsonEncode(body));
      final response = await request.close();
      final content = await utf8.decodeStream(response);
      final parsed = content.isEmpty ? <String, dynamic>{} : jsonDecode(content) as Map<String, dynamic>;
      if (response.statusCode == 401) throw const UnauthorizedException();
      if (response.statusCode < 200 || response.statusCode >= 300) {
        throw ApiException(parsed['detail'] as String? ?? 'Request failed', statusCode: response.statusCode);
      }
      return parsed;
    } on SocketException {
      throw const ApiException('Unable to reach the PROK API. Check your connection and try again.');
    } finally {
      client.close(force: true);
    }
  }
}
