import 'package:flutter/material.dart';

import 'models/current_user.dart';
import 'services/auth_api.dart';
import 'services/auth_session.dart';

void main() => runApp(const ProkApp());

class ProkApp extends StatelessWidget {
  const ProkApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'PROK',
    debugShowCheckedModeBanner: false,
    theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xff237b70)), useMaterial3: true),
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
  bool _loading = true;

  @override
  void initState() { super.initState(); _restore(); }

  Future<void> _restore() async {
    final token = await _session.readToken();
    if (token != null) {
      try { _user = await _api.currentUser(token); _token = token; } on AuthException { await _session.clear(); }
    }
    if (mounted) setState(() => _loading = false);
  }

  Future<void> _signIn(String email, String password) async {
    final token = await _api.login(email, password);
    final user = await _api.currentUser(token);
    await _session.saveToken(token);
    if (mounted) setState(() { _token = token; _user = user; });
  }

  Future<void> _logout() async {
    if (_token != null) { try { await _api.logout(_token!); } on AuthException {} }
    await _session.clear();
    if (mounted) setState(() { _token = null; _user = null; });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    return _user == null ? LoginScreen(onLogin: _signIn) : Scaffold(
      appBar: AppBar(title: const Text('PROK'), actions: [IconButton(onPressed: _logout, icon: const Icon(Icons.logout), tooltip: 'Sign out')]),
      body: Padding(padding: const EdgeInsets.all(24), child: Text('Signed in as ${_user!.displayName}\nRole confirmed by API: ${_user!.role}', style: Theme.of(context).textTheme.titleLarge)),
    );
  }
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key, required this.onLogin});
  final Future<void> Function(String email, String password) onLogin;
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _email = TextEditingController(text: 'student.one@prok.example');
  final _password = TextEditingController();
  String? _error;
  bool _submitting = false;
  @override
  void dispose() { _email.dispose(); _password.dispose(); super.dispose(); }
  Future<void> _submit() async {
    setState(() { _submitting = true; _error = null; });
    try { await widget.onLogin(_email.text, _password.text); } on AuthException catch (error) { if (mounted) setState(() => _error = error.message); } finally { if (mounted) setState(() => _submitting = false); }
  }
  @override
  Widget build(BuildContext context) => Scaffold(body: Center(child: ConstrainedBox(constraints: const BoxConstraints(maxWidth: 420), child: Padding(padding: const EdgeInsets.all(24), child: Column(mainAxisSize: MainAxisSize.min, crossAxisAlignment: CrossAxisAlignment.stretch, children: [
    Text('PROK', style: Theme.of(context).textTheme.displaySmall), const SizedBox(height: 8), const Text('Secure sign in'), const SizedBox(height: 16),
    TextField(controller: _email, keyboardType: TextInputType.emailAddress, decoration: const InputDecoration(labelText: 'Email')), TextField(controller: _password, obscureText: true, decoration: const InputDecoration(labelText: 'Password')), if (_error != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error))), const SizedBox(height: 16), FilledButton(onPressed: _submitting ? null : _submit, child: Text(_submitting ? 'Signing in…' : 'Sign in')),
  ])))));
}
