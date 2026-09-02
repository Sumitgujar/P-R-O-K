import 'package:flutter/material.dart';

import '../models/current_user.dart';
import 'feature_screens.dart';
import 'profile_screen.dart';
import 'student_home_screen.dart';

class StudentShell extends StatefulWidget {
  const StudentShell({super.key, required this.user, required this.onLogout});
  final CurrentUser user;
  final Future<void> Function() onLogout;
  @override
  State<StudentShell> createState() => _StudentShellState();
}

class _StudentShellState extends State<StudentShell> {
  int _index = 0;
  @override
  Widget build(BuildContext context) {
    final pages = [
      StudentHomeScreen(user: widget.user),
      const AttendanceScreen(),
      const DocumentsScreen(),
      const ScholarshipsScreen(),
      ProfileScreen(user: widget.user, onLogout: widget.onLogout),
    ];
    return Scaffold(
      body: pages[_index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (value) => setState(() => _index = value),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.fact_check_outlined), selectedIcon: Icon(Icons.fact_check), label: 'Attendance'),
          NavigationDestination(icon: Icon(Icons.folder_outlined), selectedIcon: Icon(Icons.folder), label: 'Documents'),
          NavigationDestination(icon: Icon(Icons.school_outlined), selectedIcon: Icon(Icons.school), label: 'Scholarships'),
          NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}
