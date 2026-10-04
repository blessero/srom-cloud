# skill name -> source folder (sourced by the tools)
R="/Users/michalbartosz/ARBEIT/Bima/SROM/CODE/SROM/SROM edit and trans"
SRC_srom_kanon="$R/srom-produkcja/.claude/skills/srom-kanon"
SRC_srom_produkcja="$R/srom-produkcja/.claude/skills/srom-produkcja"
SRC_srom_quant="$R/srom-produkcja/.claude/skills/srom-quant"
SRC_srom_tlumacz="$R/srom-tlumacz/.claude/skills/srom-tlumacz"
SRC_wp_acf_plugin_builder="$HOME/.claude/skills/wp-acf-plugin-builder"
SRC_wp_elementor_builder="$HOME/.claude/skills/wp-elementor-builder"
SKILLS="srom-kanon srom-produkcja srom-quant srom-tlumacz wp-acf-plugin-builder wp-elementor-builder"
EXCL="--exclude=__pycache__ --exclude=.DS_Store --exclude=*.pyc"
src_of() { eval echo "\"\$SRC_$(echo "$1" | tr - _)\""; }
