

def get_res_l10n_template(resource_name: str) -> str:
    template = '''
        import 'package:flutter/widgets.dart';
        import 'package:flutter_gen/gen_l10n/app_localizations.dart';
        import 'package:flutter_localizations/flutter_localizations.dart';
        class {RESOURCE_NAME}Localization {
          const {RESOURCE_NAME}Localization();

          List<Locale> get supportedLocales => AppLocalizations.supportedLocales;

          List<LocalizationsDelegate<Object>> get delegates {
            return [
              AppLocalizations.delegate,
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate,
              GlobalCupertinoLocalizations.delegate,
            ];
          }
        }

        extension {RESOURCE_NAME}Extension on BuildContext {
          AppLocalizations get loc => AppLocalizations.of(this);
        }
    '''

    return template.replace("{RESOURCE_NAME}", resource_name)





