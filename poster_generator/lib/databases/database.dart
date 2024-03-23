import 'package:http/http.dart' as http;

void sendPromptToServer(String prompt) async {
  // Replace with your Flask server's URL
  final url = Uri.parse('http://127.0.0.1:5000/promt');

  try {
    final response = await http.post(
      url,
      body: {'prompt': prompt},
    );

    if (response.statusCode == 200) {
      // Handle successful response (e.g., show a success message)
      print('Prompt sent successfully!');
    } else {
      // Handle error response (e.g., show an error message)
      print('Error sending prompt: ${response.statusCode}');
    }
  } catch (error) {
    // Handle exceptions (e.g., network errors)
    print('Error sending prompt: $error');
  }
}
