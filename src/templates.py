from src.case_util import snake_to_pascal


def res_export_template(project_name: str):
    template = """
export './src/{0}_localization.dart';
export './src/{0}_theme.dart';
    """

    result = template.format(project_name)
    return result


# from case_util import snake_to_pascal
def get_res_l10n_template(project_name: str) -> str:

    pascal_case = snake_to_pascal(project_name)

    template = """
import 'package:flutter/widgets.dart';
import '../l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
class {0}Localization {{
  const {0}Localization();

  List<Locale> get supportedLocales => AppLocalizations.supportedLocales;

  List<LocalizationsDelegate<Object>> get delegates {{
    return [
      AppLocalizations.delegate,
      GlobalMaterialLocalizations.delegate,
      GlobalWidgetsLocalizations.delegate,
      GlobalCupertinoLocalizations.delegate,
    ];
  }}
}}

extension {0}Extension on BuildContext {{
  AppLocalizations get loc => AppLocalizations.of(this);
}}
    """
    res = template.format(pascal_case)

    return res


def apps_main_template(app_name: str, project_name: str):
    app_pascal = snake_to_pascal(app_name)
    project_pascal = snake_to_pascal(project_name)
    template = """
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
// import 'package:{1}/config/route/router.dart';
import 'package:{2}/core/providers/locale_provider.dart';
import 'package:{2}_resources/{1}_resources.dart';

class {0} extends StatelessWidget  {{
  const {0}({{super.key}});

  @override
  Widget build(BuildContext context) {{
    //final selectedString = ref.watch(languageProvider);

    const localization = {1}Localization();

    return {1}Theme(
        themeMode: ThemeMode.dark,
        builder: (config) {{
          return MaterialApp.router(
              localizationsDelegates: localization.delegates, supportedLocales: localization.supportedLocales,
              locale: const Locale('ne'),
//              routerConfig: AppRouter.router,
              debugShowCheckedModeBanner: false,
              theme: config.dark,
              darkTheme: config.dark);
        }});
  }}
}}
    """

    result = template.format(app_pascal, project_pascal, project_name)
    return result


def get_theme_template(project_name: str):

    pascal = snake_to_pascal(project_name)
    template = """
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class {0}Theme extends StatefulWidget {{
  const {0}Theme({{required this.builder, required this.themeMode, super.key}});

  final Widget Function({0}ThemeConfig) builder;
  final ThemeMode themeMode;

  @override
  State<{0}Theme> createState() => _{0}ThemeState();

  static {0}ThemeConfig of(BuildContext context) {{
    final result =
        context.dependOnInheritedWidgetOfExactType<_{0}ThemeScope>();
    assert(result != null, 'No {0}Theme found in context');
    return result!.config;
  }}
}}

class _{0}ThemeState extends State<{0}Theme> {{
  late final {0}ThemeConfig _config;

  @override
  void initState() {{
    super.initState();
    _config = {0}ThemeConfig(
      mode: widget.themeMode,
    );
  }}

  @override
  Widget build(BuildContext context) {{
    return _{0}ThemeScope(config: _config, child: widget.builder(_config));
  }}
}}

class _{0}ThemeScope extends InheritedWidget {{
  const _{0}ThemeScope({{required this.config, required super.child}});

  final {0}ThemeConfig config;

  @override
  bool updateShouldNotify(_{0}ThemeScope oldWidget) =>
      oldWidget.config != config;
}}

class {0}ThemeConfig {{
  {0}ThemeConfig({{required this.mode}}) {{
    // Define the text theme based on the typography image
    final TextTheme customTextTheme = TextTheme(
      displayLarge: GoogleFonts.roboto(
        fontSize: 57,
        fontWeight: FontWeight.w400,
        letterSpacing: -0.25,
      ),
      displayMedium: GoogleFonts.roboto(
        fontSize: 45,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
      ),
      displaySmall: GoogleFonts.roboto(
        fontSize: 36,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
      ),
      headlineLarge: GoogleFonts.roboto(
        fontSize: 32,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
      ),
      headlineMedium: GoogleFonts.roboto(
        fontSize: 28,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
      ),
      headlineSmall: GoogleFonts.roboto(
        fontSize: 24,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
      ),
      titleLarge: GoogleFonts.roboto(
        fontSize: 22,
        fontWeight: FontWeight.w400,
        letterSpacing: 0,
      ),
      titleMedium: GoogleFonts.roboto(
        fontSize: 16,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.15,
      ),
      titleSmall: GoogleFonts.roboto(
        fontSize: 14,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.1,
      ),
      labelLarge: GoogleFonts.roboto(
        fontSize: 14,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.1,
      ),
      labelMedium: GoogleFonts.roboto(
        fontSize: 12,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.5,
      ),
      labelSmall: GoogleFonts.roboto(
        fontSize: 11,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.5,
      ),
      bodyLarge: GoogleFonts.roboto(
        fontSize: 16,
        fontWeight: FontWeight.w400,
        letterSpacing: 0.15,
      ),
      bodyMedium: GoogleFonts.roboto(
        fontSize: 14,
        fontWeight: FontWeight.w400,
        letterSpacing: 0.25,
      ),
      bodySmall: GoogleFonts.roboto(
        fontSize: 12,
        fontWeight: FontWeight.w400,
        letterSpacing: 0.4,
      ),
    );

    light = ThemeData(
      colorScheme: _lightColorScheme,
      textTheme: customTextTheme,
      useMaterial3: true,
    );

    dark = ThemeData(
      colorScheme: _darkColorScheme,
      textTheme: customTextTheme,
      useMaterial3: true,
    );
  }}

  final ThemeMode mode;

  late final ThemeData light;
  late final ThemeData dark;
}}

ColorScheme _lightColorScheme = const ColorScheme.light(
  primary: Color(0xFF00376B),
  onPrimary: Color(0xFFFFFFFF),
  primaryContainer: Color(0xFFCEE5FF),
  onPrimaryContainer: Color(0xFF001E42),
  secondary: Color(0xFF4C626B),
  onSecondary: Color(0xFFFFFFFF),
  secondaryContainer: Color(0xFFCFE6F1),
  onSecondaryContainer: Color(0xFF071F26),
  tertiary: Color(0xFF006875),
  onTertiary: Color(0xFFFFFFFF),
  tertiaryContainer: Color(0xFFAFEBF3),
  onTertiaryContainer: Color(0xFF001F24),
  error: Color(0xFFB3261E),
  onError: Color(0xFFFFFFFF),
  errorContainer: Color(0xFFF9DEDC),
  onErrorContainer: Color(0xFF410E0B),
  surface: Color(0xFFFBFCFD),
  onSurface: Color(0xFF1C1B1F),
  outline: Color(0xFF72777D),
);

ColorScheme _darkColorScheme = const ColorScheme.dark(
  primary: Color(0xFF84CFFF),
  onPrimary: Color(0xFF003354),
  primaryContainer: Color(0xFF004B76),
  onPrimaryContainer: Color(0xFFCFE5FF),
  secondary: Color(0xFFB2CBD3),
  onSecondary: Color(0xFF1C333B),
  secondaryContainer: Color(0xFF334B53),
  onSecondaryContainer: Color(0xFFCFE6F1),
  tertiary: Color(0xFF6FD5E0),
  onTertiary: Color(0xFF00363F),
  tertiaryContainer: Color(0xFF004F5A),
  onTertiaryContainer: Color(0xFFAFEBF3),
  error: Color(0xFFF2B8B5),
  onError: Color(0xFF601410),
  errorContainer: Color(0xFF8C1D18),
  onErrorContainer: Color(0xFFF9DEDC),
  surface: Color(0xFF1C1B1F),
  onSurface: Color(0xFFE6E1E5),
  outline: Color(0xFF8C9196),
);
    """
    res = template.format(pascal)
    return res
