class CurrentUser {
  const CurrentUser({required this.id, required this.email, required this.displayName, required this.role});

  final String id;
  final String email;
  final String displayName;
  final String role;

  factory CurrentUser.fromJson(Map<String, dynamic> json) => CurrentUser(
    id: json['id'] as String,
    email: json['email'] as String,
    displayName: json['display_name'] as String,
    role: json['role'] as String,
  );
}
