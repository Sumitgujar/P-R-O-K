import 'package:flutter/material.dart';

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});
  @override
  Widget build(BuildContext context) => const Scaffold(
    body: Center(child: Column(mainAxisSize: MainAxisSize.min, children: [
      Icon(Icons.auto_awesome, size: 48, color: Color(0xff237b70)), SizedBox(height: 16), Text('PROK'), SizedBox(height: 16), CircularProgressIndicator(),
    ])),
  );
}
