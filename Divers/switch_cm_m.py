import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark

def state():
    return c4d.CMD_ENABLED

# Main function


def main():
    def prefs(id):
        return c4d.plugins.FindPlugin(id, c4d.PLUGINTYPE_PREFS)

    pref = prefs(465001627)

    if pref[c4d.PREF_UNITS_BASIC] == c4d.PREF_UNITS_BASIC_M :
        pref[c4d.PREF_UNITS_BASIC] = c4d.PREF_UNITS_BASIC_CM
    else :
        pref[c4d.PREF_UNITS_BASIC] = c4d.PREF_UNITS_BASIC_M


# Execute main()
if __name__=='__main__':
    main()