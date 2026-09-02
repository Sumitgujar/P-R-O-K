import 'package:flutter/material.dart';

import '../models/current_user.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key, required this.user, required this.onLogout});
  final CurrentUser user;
  final Future<void> Function() onLogout;
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Profile')),
    body: ListView(padding: const EdgeInsets.all(20), children: [
      CircleAvatar(radius: 34, child: Text(user.displayName.substring(0, 1).toUpperCase(), style: Theme.of(context).textTheme.headlineMedium)), const SizedBox(height: 16), Center(child: Text(user.displayName, style: Theme.of(context).textTheme.headlineSmall)), Center(child: Text(user.email)), const SizedBox(height: 24),
      Card(child: ListTile(leading: const Icon(Icons.verified_user_outlined), title: const Text('Account role'), subtitle: Text('Student · confirmed by PROK API'))), const SizedBox(height: 16),
      OutlinedButton.icon(onPressed: onLogout, icon: const Icon(Icons.logout), label: const Text('Sign out')),
    ]),
  );
}
