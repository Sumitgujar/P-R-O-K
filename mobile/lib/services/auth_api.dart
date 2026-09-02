import '../models/current_user.dart';
import 'api_client.dart';

typedef AuthException = ApiException;

class AuthApi {
  AuthApi({ApiClient? client}) : _client = client ?? ApiClient();
  final ApiClient _client;

  Future<String> login(String email, String password) async {
    final result = await _client.request('/auth/login', method: 'POST', body: {'email': email, 'password': password});
    return result['access_token'] as String;
  }

  Future<CurrentUser> currentUser(String token) async {
    final result = await _client.request('/auth/me', token: token);
    return CurrentUser.fromJson(result);
  }

  Future<void> logout(String token) async {
    await _client.request('/auth/logout', method: 'POST', token: token);
  }
}
