import 'package:flutter/material.dart';

class AttendanceScreen extends StatelessWidget {
  const AttendanceScreen({super.key});
  @override
  Widget build(BuildContext context) => const FeatureUnavailableScreen(title: 'Attendance', icon: Icons.fact_check_outlined, description: 'Your attendance data will appear here when the attendance API is connected.');
}

class DocumentsScreen extends StatelessWidget {
  const DocumentsScreen({super.key});
  @override
  Widget build(BuildContext context) => const FeatureUnavailableScreen(title: 'Documents', icon: Icons.folder_outlined, description: 'Your document list and verification status will appear here when the document API is connected.');
}

class ScholarshipsScreen extends StatelessWidget {
  const ScholarshipsScreen({super.key});
  @override
  Widget build(BuildContext context) => const FeatureUnavailableScreen(title: 'Scholarships', icon: Icons.school_outlined, description: 'Eligible scholarships and application checklists will appear here when the scholarship API is connected.');
}

class CourseRecommendationsScreen extends StatelessWidget {
  const CourseRecommendationsScreen({super.key});
  @override
  Widget build(BuildContext context) => const FeatureUnavailableScreen(title: 'Course recommendations', icon: Icons.auto_graph_outlined, description: 'Transparent course recommendations will appear here when the recommendation API is connected.');
}

class AskProkScreen extends StatelessWidget {
  const AskProkScreen({super.key});
  @override
  Widget build(BuildContext context) => const FeatureUnavailableScreen(title: 'Ask PROK', icon: Icons.auto_awesome_outlined, description: 'The AI guide is not enabled yet. It will only provide grounded guidance from approved college information.');
}

class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({super.key});
  @override
  Widget build(BuildContext context) => const FeatureUnavailableScreen(title: 'Notifications', icon: Icons.notifications_none, description: 'You have no notifications available yet. Alerts will appear here when the notifications API is connected.');
}

class FeatureUnavailableScreen extends StatelessWidget {
  const FeatureUnavailableScreen({super.key, required this.title, required this.icon, required this.description});
  final String title;
  final IconData icon;
  final String description;
  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: Text(title)),
    body: Center(child: Padding(padding: const EdgeInsets.all(32), child: Column(mainAxisSize: MainAxisSize.min, children: [
      Icon(icon, size: 52, color: Theme.of(context).colorScheme.primary), const SizedBox(height: 16), Text(title, style: Theme.of(context).textTheme.headlineSmall), const SizedBox(height: 8), Text(description, textAlign: TextAlign.center, style: Theme.of(context).textTheme.bodyLarge),
    ]))),
  );
}
