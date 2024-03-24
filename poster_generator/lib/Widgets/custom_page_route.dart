import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class CustomPageRoute extends PageRouteBuilder {
  final Widget child;

  CustomPageRoute({
    required this.child,
  }) : super(
    transitionDuration: Duration(milliseconds: 500),
    pageBuilder: (
        context,
        animation,
        secondaryAnimation,
        ) =>
    child,
    transitionsBuilder: (
        context,
        animation,
        secondaryAnimation,
        child,
        ) {
      const begin = Offset(1.0, 0.0);
      const end = Offset.zero;
      const curve = Curves.easeInOut;

      var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));

      var offsetAnimation = animation.drive(tween);

      return SlideTransition(
        position: offsetAnimation,
        child: child,
      );
    },
  );
}
