import 'package:flutter/material.dart';

import '../services/auth_api.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key, required this.onLogin, this.initialError});
  final Future<void> Function(String email, String password) onLogin;
  final String? initialError;
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _email = TextEditingController();
  final _password = TextEditingController();
  String? _error;
  bool _submitting = false;
  @override
  void initState() { super.initState(); _error = widget.initialError; }
  @override
  void dispose() { _email.dispose(); _password.dispose(); super.dispose(); }
  Future<void> _submit() async {
    setState(() { _submitting = true; _error = null; });
    try { await widget.onLogin(_email.text, _password.text); } on AuthException catch (error) { if (mounted) setState(() => _error = error.message); } finally { if (mounted) setState(() => _submitting = false); }
  }
  @override
  Widget build(BuildContext context) => Scaffold(body: SafeArea(child: Center(child: SingleChildScrollView(child: ConstrainedBox(constraints: const BoxConstraints(maxWidth: 420), child: Padding(padding: const EdgeInsets.all(24), child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
    Text('PROK', style: Theme.of(context).textTheme.displaySmall), const SizedBox(height: 8), Text('Your college personal guide', style: Theme.of(context).textTheme.titleMedium), const SizedBox(height: 32),
    TextField(controller: _email, keyboardType: TextInputType.emailAddress, autofillHints: const [AutofillHints.username], decoration: const InputDecoration(labelText: 'Email')), const SizedBox(height: 12), TextField(controller: _password, obscureText: true, autofillHints: const [AutofillHints.password], onSubmitted: (_) => _submit(), decoration: const InputDecoration(labelText: 'Password')), if (_error != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error))), const SizedBox(height: 20), FilledButton(onPressed: _submitting ? null : _submit, child: Text(_submitting ? 'Signing in…' : 'Sign in')),
  ]))))));
}
