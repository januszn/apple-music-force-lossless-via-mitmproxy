# apple-music-force-lossless-via-mitmproxy

A mitmproxy script to make sure Apple Music actually streams lossless audio.

## Problem

Apple Music uses HLS for lossless streaming and the playlists include lossy variants to handle low-bandwidth conditions.
This would be all well and good, but very often the lossy and lossless variants, or even the different quality lossless
variants - not necessarily hi-res vs "normal" lossless - I noticed this with 44100/16 and 44100/24 "not-hi-res" variants
of at least one album - don't align perfectly. Combined with the fact that the streaming often starts with the
lower-bandwidth variant and then immediately switches to the highest-bandwidth one after the first fragment, you get an
audible hiccup at the moment of the switch, either within the first two seconds or at multiplies of 15 seconds,
depending on how the given track is fragmented. This absolutely kills any enjoyment of lossless streaming, given that
you can be half-deaf, distracted and still notice the skips, yet to hear the benefits of lossless you need a good
listening environment and at least some dose of self-delusion. See https://discussions.apple.com/thread/253814684 for
proof that it's not just me, there's also FB11702976 from 2022 by me if anyone actually reads that. In any case, Apple
doesn't give the "pretty please, I can wait for buffering, just stream the one variant I want" option, and doesn't seem
to care that their variants are misaligned.

## Workaround

Apple Music doesn't use certificate pinning for the actual streams (it does for everything else), so it's possible to
MITM it and remove the unwanted lossy streams from the main m3u8 file. The script in this repository
uses https://mitmproxy.org for that purpose.

## Usage

Install mitmproxy and verify that it works - that you set the HTTPS proxy on your internet connection, installed the
certificate etc.
You won't need the proxy to remain set, we'll use mitmproxy's "local" mode to intercept only the Music app. If you use
hi-res lossless, uncomment the one relevant line in the script.

Run mitmproxy with the script:
```
/Applications/mitmproxy.app/Contents/MacOS/mitmdump --allow-hosts=aod.itunes.apple.com --mode local:Music -s ~/path/to/strip-lossy-streams.py
```

Enjoy lossless streaming.

## Notes

- I literally just read the Python tutorial to write this, don't hate me.
- This will not allow you to rip the streams in any way, they're still encrypted.
- I tried Tidal, but it doesn't have half the stuff I listen to.
- Apple folks, please fix this. It can be an option (I'll leave it to you to phrase "minimum streaming quality"/"disable
  adaptive streaming" in a way that won't confuse users), or you can re-check all your streams to confirm they align
  perfectly, or you can attempt to detect on-device if switching variants is going to cause an audible skip and don't
  switch if it does (maybe align on device too?).
