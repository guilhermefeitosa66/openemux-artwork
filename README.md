# OpenEmux Artwork

A self-hosted, size-reduced mirror of community box art for the consoles
[OpenEmux](https://github.com/guilhermefeitosa66/OpenEmux) supports. It exists
so the app has a cover-art source under the project's own control when the
upstream sources are unreachable or missing a title (OpenEmux issue
[#74](https://github.com/guilhermefeitosa66/OpenEmux/issues/74)).

## Layout

```
<System_Name>/<Game Name>.webp     # e.g. Nintendo_-_Game_Boy/Tetris (World) (Rev 1).webp
systems.json                       # OpenEmux console id -> directory name
```

- Directory names follow the upstream `libretro-thumbnails` repository names
  (spaces as underscores).
- File names keep the upstream No-Intro/Redump naming, so the same name
  normalization OpenEmux already applies to libretro URLs applies here.
- Every image is re-encoded to WebP with the longest side capped at 512 px —
  the resolution the OpenEmux grid actually renders — which keeps the whole
  set roughly an order of magnitude smaller than the source PNGs.

Fetch a cover with:

```
https://raw.githubusercontent.com/guilhermefeitosa66/openemux-artwork/main/<System_Name>/<Game Name>.webp
```

## Updating

`.github/workflows/sync.yml` re-syncs every system from upstream — on a
monthly schedule and on manual dispatch (optionally filtered to a
space-separated list of system directories). Each system job does a
blobless sparse clone of only `Named_Boxarts/`, converts, and pushes; jobs
run serially so pushes never race.

## Provenance and licensing

All artwork originates from the community-maintained
[libretro-thumbnails](https://github.com/libretro-thumbnails/libretro-thumbnails)
collection and is redistributed here in reduced resolution, unmodified
otherwise, with attribution — the same spirit in which the collection is
shared. Game cover art itself remains the property of the respective
publishers; it is reproduced at thumbnail size for identification purposes
only. If you are a rights holder and want something removed, open an issue
and it will be taken down.

No ScreenScraper media is included: their terms do not allow redistribution.
