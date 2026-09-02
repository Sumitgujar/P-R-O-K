import 'package:flutter/material.dart';

import '../models/current_user.dart';
import 'feature_screens.dart';

class StudentHomeScreen extends StatelessWidget {
  const StudentHomeScreen({super.key, required this.user});
  final CurrentUser user;

  void _open(BuildContext context, Widget screen) => Navigator.of(context).push(MaterialPageRoute<void>(builder: (_) => screen));

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: const Text('PROK'),
      actions: [IconButton(onPressed: () => _open(context, const NotificationsScreen()), icon: const Icon(Icons.notifications_none), tooltip: 'Notifications')],
    ),
    body: ListView(padding: const EdgeInsets.all(20), children: [
      Text('Good morning, ${user.displayName.split(' ').first} 👋', style: Theme.of(context).textTheme.headlineSmall), const SizedBox(height: 6), Text('Your college journey, in one place.', style: Theme.of(context).textTheme.bodyLarge), const SizedBox(height: 22),
      GridView.count(crossAxisCount: 2, shrinkWrap: true, physics: const NeverScrollableScrollPhysics(), mainAxisSpacing: 12, crossAxisSpacing: 12, childAspectRatio: 1.35, children: [
        _SummaryCard(label: 'Attendance', value: 'Not connected', icon: Icons.fact_check_outlined, onTap: () => _open(context, const AttendanceScreen())),
        _SummaryCard(label: 'Documents', value: 'Not connected', icon: Icons.folder_outlined, onTap: () => _open(context, const DocumentsScreen())),
        _SummaryCard(label: 'Scholarships', value: 'Not connected', icon: Icons.school_outlined, onTap: () => _open(context, const ScholarshipsScreen())),
        _SummaryCard(label: 'Recommendations', value: 'Not connected', icon: Icons.auto_graph_outlined, onTap: () => _open(context, const CourseRecommendationsScreen())),
      ]), const SizedBox(height: 20),
      FilledButton.icon(onPressed: () => _open(context, const AskProkScreen()), icon: const Icon(Icons.auto_awesome_outlined), label: const Text('Ask PROK')), const SizedBox(height: 24),
      Text('Recent alerts', style: Theme.of(context).textTheme.titleLarge), const SizedBox(height: 8), const Card(child: Padding(padding: EdgeInsets.all(16), child: Text('No alerts are available yet. When backend alert services are connected, current attendance, document, and recommendation alerts will be shown here.')),
    ]),
  );
}

class _SummaryCard extends StatelessWidget {
  const _SummaryCard({required this.label, required this.value, required this.icon, required this.onTap});
  final String label;
  final String value;
  final IconData icon;
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) => Card(child: InkWell(borderRadius: BorderRadius.circular(12), onTap: onTap, child: Padding(padding: const EdgeInsets.all(14), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Icon(icon, color: Theme.of(context).colorScheme.primary), const Spacer(), Text(label, style: Theme.of(context).textTheme.labelLarge), Text(value, style: Theme.of(context).textTheme.bodySmall)]))));
}
