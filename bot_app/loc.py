from babel import Locale

# Parsing
l = Locale.parse('de-DE', sep='-')
print("Locale name: {0}".format(l.display_name))

l = Locale.parse('und_GR', sep='_')
print("Locale name: {0}".format(l.display_name))

# Detecting
l = Locale.negotiate(['de_DE', 'en_AU'], ['de_DE', 'de_AT'])
print("Locale negociated: {0}".format(l.display_name))

print(Locale('it').english_name)
print(Locale('it').get_display_name('fr_FR'))
print(Locale('it').get_language_name('de_DE'))
print(Locale('de', 'DE').languages['zh'])

print(Locale('el', 'GR').scripts['Copt'])

# Calendar
locale = Locale('it')
month_names = locale.days['format']['wide'].items()
print(list(month_names))
