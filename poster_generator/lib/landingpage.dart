import 'package:flutter/material.dart';
import 'package:poster_generator/Widgets/button_widget.dart';
import 'package:poster_generator/homepage.dart';

import 'Widgets/custom_page_route.dart';

class Landingpage extends StatelessWidget {
  const Landingpage({super.key});

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
                child: ButtonWidget(
                  onPressed: () => Navigator.pop(
                    context,
                    CustomPageRoute(child: const Homepage()),
                  ),
                  text: 'Get Started',
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
