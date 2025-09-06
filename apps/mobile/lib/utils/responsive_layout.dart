import 'package:flutter/material.dart';

class ResponsiveLayout extends StatelessWidget {
  final Widget mobile;
  final Widget? tablet;
  final Widget? desktop;

  const ResponsiveLayout({
    super.key,
    required this.mobile,
    this.tablet,
    this.desktop,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth >= 1200) {
          return desktop ?? tablet ?? mobile;
        } else if (constraints.maxWidth >= 768) {
          return tablet ?? mobile;
        } else {
          return mobile;
        }
      },
    );
  }
}

class ResponsiveBreakpoints {
  static const double mobile = 768;
  static const double tablet = 1200;
  
  static bool isMobile(BuildContext context) {
    return MediaQuery.of(context).size.width < mobile;
  }
  
  static bool isTablet(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    return width >= mobile && width < tablet;
  }
  
  static bool isDesktop(BuildContext context) {
    return MediaQuery.of(context).size.width >= tablet;
  }
}

class ResponsivePadding {
  static EdgeInsets page(BuildContext context) {
    if (ResponsiveBreakpoints.isMobile(context)) {
      return const EdgeInsets.all(16);
    } else if (ResponsiveBreakpoints.isTablet(context)) {
      return const EdgeInsets.symmetric(horizontal: 32, vertical: 24);
    } else {
      return const EdgeInsets.symmetric(horizontal: 64, vertical: 32);
    }
  }
  
  static EdgeInsets card(BuildContext context) {
    if (ResponsiveBreakpoints.isMobile(context)) {
      return const EdgeInsets.all(16);
    } else {
      return const EdgeInsets.all(24);
    }
  }
}

class ResponsiveGrid {
  static int columns(BuildContext context) {
    if (ResponsiveBreakpoints.isMobile(context)) {
      return 1;
    } else if (ResponsiveBreakpoints.isTablet(context)) {
      return 2;
    } else {
      return 3;
    }
  }
  
  static double spacing(BuildContext context) {
    if (ResponsiveBreakpoints.isMobile(context)) {
      return 16;
    } else {
      return 24;
    }
  }
}

class ResponsiveWidth {
  static double content(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    
    if (ResponsiveBreakpoints.isMobile(context)) {
      return screenWidth;
    } else if (ResponsiveBreakpoints.isTablet(context)) {
      return screenWidth * 0.8;
    } else {
      return 1200;
    }
  }
  
  static Widget centered(BuildContext context, Widget child) {
    final contentWidth = content(context);
    
    return Center(
      child: Container(
        width: contentWidth,
        child: child,
      ),
    );
  }
}