import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:poster_generator/databases/database.dart';

class Homepage extends StatelessWidget {
  const Homepage({super.key});

  @override
  Widget build(BuildContext context) {
    String _promt = "";
    TextEditingController promt = new TextEditingController();
    String image = "";
    var isLoaded = false;

    return Scaffold(
      backgroundColor: Color(0xFFF1F8FF),
      drawer: const Drawer(
        backgroundColor: Color(0xFFF1F8FF),
      ),
      appBar: AppBar(
        elevation: 10,
        toolbarHeight: 100,
        title: const Text(
          'PosterGenieAI',
          style:
              TextStyle(color: Color(0xFF7209B7), fontWeight: FontWeight.bold),
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Image.asset('assets/images/notification.png'),
          )
        ],
        centerTitle: true,
        backgroundColor: const Color(0xFFF1F8FF),
      ),
      body: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            SizedBox(
              height: 10,
            ),
            SingleChildScrollView(
                scrollDirection: Axis.vertical,
                child: isLoaded
                    ? Image.network(image)
                    : Image.asset('assets/animations/loader.gif')),
            Padding(
              padding: EdgeInsets.only(left: 16, top: 10),
              child: Text(
                'Input Prompt',
                style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.w700,
                    fontFamily: 'Jakarta'),
              ),
            ),
            SizedBox(
              height: 10,
            ),
            Padding(
              padding: const EdgeInsets.all(20),
              child: TextField(
                controller: promt,
                decoration: InputDecoration(
                    enabledBorder: const OutlineInputBorder(
                        borderSide:
                            BorderSide(color: Color(0xFF7209B7), width: 2)),
                    focusedBorder: const OutlineInputBorder(
                        borderSide:
                            BorderSide(color: Color(0xFF7209B7), width: 2)),
                    hintText: 'Describe about event',
                    suffixIcon: IconButton(
                        onPressed: () {
                          promt.clear();
                        },
                        icon: Icon(
                          Icons.clear,
                          color: Color(0xFF7209B7),
                        ))),
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(left: 100, bottom: 20),
              child: Directionality(
                textDirection: TextDirection.rtl,
                child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                        minimumSize: Size(280, 50),
                        primary: Color(0xFF7209B7),
                        onPrimary: Colors.white),
                    onPressed: () async {
                      await fetchImageUrls(promt.text);
                    },
                    icon: Icon(Icons.arrow_back_rounded),
                    label: Text(
                      'Next',
                      style: TextStyle(fontSize: 20),
                    )),
              ),
            )
          ]),
    );
  }
}
