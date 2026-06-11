def print_help(args, COLLECTION_FLAGS):
    print(
        """
OmniGlyph
Fast Emoji and Unicode Symbol Picker for Linux

USAGE
  omniglyph [OPTION]

OPTIONS
  -h, --help
      Show this help message and exit.

COLLECTIONS
  --emoji
      Load emoji characters.

  --emoticons
      Load text emoticons and kaomoji.

  --arrows
      Load arrow and directional symbols.

  --math
      Load mathematical operators and symbols.

  --currency
      Load currency symbols.

  --special
      Load miscellaneous Unicode symbols.

  --hieroglyphs
      Load Egyptian hieroglyph characters.

EXAMPLES
  omniglyph
      Start OmniGlyph with the default emoji collection.

  omniglyph --math
      Start OmniGlyph with mathematical symbols selected.

  omniglyph --currency
      Start OmniGlyph with currency symbols selected.

  omniglyph --hieroglyphs
      Start OmniGlyph with Egyptian hieroglyphs selected.

DEFAULT
  If no collection is specified, OmniGlyph starts with:

      --emoji
"""
    )
