import 'dart:convert';

import 'package:http/http.dart' as http;

List<String> imageUrls = [];
Future<void> fetchImageUrls(String promt) async {
  final response = await http.post(
    Uri.parse(
        'http://10.0.2.2:5000/promt'), // Replace with your Flask server URL
    body: {'prompt': promt}, // Replace with your prompt
  );

  if (response.statusCode == 200) {
    final data = json.decode(response.body);
    print(data);
    // imageUrls = List<String>.from(data['images']);
  } else if (response.statusCode == 404) {
    print('Error 404 occured');
  } else {
    throw Exception('Failed to load image URLs');
  }
}
