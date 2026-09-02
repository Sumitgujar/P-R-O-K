import 'package:flutter/material.dart';

import 'models/current_user.dart';
import 'screens/login_screen.dart';
import 'screens/splash_screen.dart';
import 'screens/student_shell.dart';
import 'services/auth_api.dart';
import 'services/auth_session.dart';

void main() => runApp(const ProkApp());

class ProkApp extends StatelessWidget {
  const ProkApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'PROK',
    debugShowCheckedModeBanner: false,
    theme: ThemeData(
      colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xff237b70)),
      scaffoldBackgroundColor: const Color(0xfff6f8fb),
      useMaterial3: true,
    ),
    home: const AuthGate(),
  );
}

class AuthGate extends StatefulWidget {
  const AuthGate({super.key});
  @override
  State<AuthGate> createState() => _AuthGateState();
}

class _AuthGateState extends State<AuthGate> {
  final _api = AuthApi();
  final _session = AuthSession();
  CurrentUser? _user;
  String? _token;
  String? _error;
  bool _loading = true;

  @override
  void initState() { super.initState(); _restore(); }

  Future<void> _restore() async {
    final token = await _session.readToken();
    if (token != null) {
      try {
        _user = await _api.currentUser(token);
        _token = token;
      } on AuthException {
        await _session.clear();
      }
    }
    if (mounted) setState(() => _loading = false);
  }

  Future<void> _login(String email, String password) async {
    final token = await _api.login(email, password);
    final user = await _api.currentUser(token);
    if (user.role != 'student') throw const AuthException('This mobile app is currently available to student accounts only.');
    await _session.saveToken(token);
    if (mounted) setState(() { _token = token; _user = user; _error = null; });
  }

  Future<void> _logout() async {
    if (_token != null) { try { await _api.logout(_token!); } on AuthException {} }
    await _session.clear();
    if (mounted) setState(() { _token = null; _user = null; });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const SplashScreen();
    if (_user == null) return LoginScreen(onLogin: _login, initialError: _error);
    return StudentShell(user: _user!, onLogout: _logout);
  }
}
