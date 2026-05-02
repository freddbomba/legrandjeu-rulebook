#!/usr/bin/env bash
# Downloads all scenario images from legrandjeu.net and i.imgur.com
# into the assets/ subfolders of Book 1.
#
# Run once locally before the first render.
# Usage:
#   cd book1-scenarios && ./download-assets.sh
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

fetch() {
  local url="$1"
  local dest="$2"
  if [[ -f "$dest" ]]; then
    echo "  ✓ $dest (present)"
    return 0
  fi
  echo "  ↓ $dest"
  curl -fsSL --retry 3 -o "$dest" "$url"
}

# --- permacoin ------------------------------------------------------------
echo "==> permacoin"
D=assets/permacoin
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/12/Screenshot-2020-12-08-at-12.00.20.png?fit=2154%2C1474&ssl=1" "$D/hero-board-90min.png"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/12/Screenshot-2020-12-07-at-18.16.08.png" "$D/starting-set.png"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/12/2020-12-08-12.59.14.jpg" "$D/terrain-types.jpg"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/12/2020-12-08-14.33.27.jpg" "$D/in-play-occupation.jpg"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/12/blockchainCost-risc_init.jpg" "$D/blockchain-model.jpg"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/12/Screenshot-2020-12-07-at-18.16.08-2.png" "$D/master-screen.png"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/12/2020-11-11-13.54.06.jpg" "$D/resilience.jpg"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/12/Ns3y8yQ.png?fit=1109%2C619&ssl=1" "$D/game2-greencoin.png"
fetch "https://i0.wp.com/i.imgur.com/Snq7WN7.png?w=1200&ssl=1" "$D/two-continents.png"
fetch "https://i0.wp.com/i.imgur.com/JLLHlRB.png?w=1200&ssl=1" "$D/planetary-boundaries.png"
fetch "https://i0.wp.com/i.imgur.com/PNsVLJq.png?w=1200&ssl=1" "$D/round-5.png"

# --- pandemic -------------------------------------------------------------
echo "==> pandemic"
D=assets/pandemic
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/04/n37Vckr.png?fit=2338%2C1814&ssl=1" "$D/hero-board.png"

# --- downunder ------------------------------------------------------------
echo "==> downunder"
D=assets/downunder
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/04/Screenshot-2020-04-21-at-15.50.00.png?fit=1676%2C1194&ssl=1" "$D/hero-valley.png"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/04/Screenshot-2020-04-21-at-15.50.18.png" "$D/local-currency.png"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/04/Screenshot-2020-04-21-at-15.50.09.png" "$D/discussion.png"

# --- sou (Three Cities) ---------------------------------------------------
echo "==> sou"
D=assets/sou
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2024/12/photo_2021-06-26_12-49-21.webp?fit=768%2C1024&ssl=1" "$D/hero-children.webp"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2024/12/treecities.webp" "$D/three-cities.webp"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2024/12/roles-sou.webp" "$D/roles.webp"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2024/12/photo_2021-06-26_12-54-09.webp" "$D/around-table.webp"
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2024/12/photo_2021-06-26_13-02-36.webp" "$D/playing.webp"

# --- messina --------------------------------------------------------------
echo "==> messina"
D=assets/messina
fetch "https://i0.wp.com/legrandjeu.net/wp-content/uploads/2020/04/board-A.png?fit=1739%2C1586&ssl=1" "$D/hero-board.png"
fetch "https://i0.wp.com/i.imgur.com/FiyyNLD.png?w=1200&ssl=1" "$D/round-1.png"
fetch "https://i0.wp.com/i.imgur.com/EexZjjD.png?w=1200&ssl=1" "$D/assembly.png"
fetch "https://i0.wp.com/i.imgur.com/Azh9isY.png?w=1200&ssl=1" "$D/wind-boats.png"
fetch "https://i0.wp.com/i.imgur.com/SwKFMIa.png?w=1200&ssl=1" "$D/round-2.png"

echo
echo "✓ Done. Assets downloaded to $SCRIPT_DIR/assets/"
