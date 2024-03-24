import 'package:flutter/material.dart';
import 'package:poster_generator/homepage.dart';
import 'package:poster_generator/Widgets/custom_page_route.dart';

class Landingpage extends StatelessWidget {
  const Landingpage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Background image
          Image.asset(
            "assets/images/background.png",
            fit: BoxFit.cover,
            width: double.infinity,
            height: double.infinity,
          ),
          // Center the button vertically
          Align(
            alignment: Alignment.bottomCenter,
            child: Padding(
              padding: const EdgeInsets.only(bottom: 50),
              child: Directionality(
                textDirection: TextDirection.rtl,
                child: ElevatedButton.icon(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => const Homepage()),
                    );
                  },
                  label: Text("Get Started"),
                  icon: Icon(Icons.arrow_forward),
                  style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.white,
                    backgroundColor: Color(0xFFF72585),
                    minimumSize: Size(280, 50),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
