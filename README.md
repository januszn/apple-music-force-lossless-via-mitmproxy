# apple-music-force-lossless-via-mitmproxy

A mitmproxy script to make sure Apple Music actually streams lossless audio.

## Background

Apple Music uses [HLS](https://datatracker.ietf.org/doc/html/rfc8216) for lossless and Dolby Atmos streaming. This means
that instead of being streamed as a single file, each song is split into (in Apple Music's case) 15 second fragments.
Additionally, songs usually have variants, like "Hi-Res Lossless" and "Lossless" on top of that. Meaning that for a
3-minute song available in both Lossless and Hi-Res Lossless, there are 12 15-second fragments of the Lossless variant,
and another 12 15-second fragments of the Hi-Res Lossless one. In addition to the variants shown in the Apple Music UI
that you can select yourself (i.e. whether you want "just" Lossless or Hi-Res Lossless), the song playlists include
lossy variants of the song, still fragmented according to the spec, so that the player can switch variants on-the-fly
depending on the available bandwidth, or to start playback immediately with a lower-quality variant and then switch to a
higher-quality one as soon as enough of it is buffered, for a snappier experience. This is all within HLS spec - you can
probably observe it yourself by watching the "lossless" playback badge closely - it may not appear immediately after
you start playing a song.

## Problems

There are at least two problems with this approach.

First, the lossless and lossy variants of the songs are often misaligned by a fraction of a second - possibly an
artifact of the lossy encodes trimming silence from the beginning of the song. See
https://discussions.apple.com/thread/253814684 for an illustration of the problem. Combined with the fact that the
Apple Music clients often start with the lossy variant to respond immediately and then switch to the lossless one after
the first fragment (which is usually either 2 or 15 seconds long), you get an audible hiccup when playing a song that
has this problem if you just want to play it on a whim, don't have it queued up and don't wait for it to come up
(because in that case the client buffers it in advance and you don't encounter the problem). This absolutely kills any
enjoyment of lossless streaming, given that you can be hard of hearing, distracted and still notice the hiccups, yet to
hear the benefits of lossless over the "High Quality" 256 kbps AAC you need a good listening environment and at least
some dose of self-delusion.

Second, there can be multiple Lossless (not Hi-Res Lossless) variants of the same song, for example 16-bit 44100 Hz and
24-bit 44100 Hz. I don't think I've encountered any that are misaligned like the lossy ones can be, but after 3 weeks
of running the initial version of this script, which would force the client to choose only from the lossless variants
of a song, which meant Apple Music, instead of starting with the lossy variant and then switching to the lossless
variant appropriate for my bandwidth, would start with the lower-quality lossless one, I noticed audible "pops" on
lossless variant switches on my Mac Mini, which is connected via HDMI to a TV, which is then connected to an amplifier
via digital optical cable (TOSLINK). I guess Apple Music reinitializes the audio output to set the exact format to
match the stream, and my equipment in particular doesn't respond to it well. Again, good intentions but poor outcome.
The second version of the script forces Apple Music to stream only one - lossless - variant.

## Workaround

Apple Music doesn't use certificate pinning for the actual streams (it does for everything else), so it's possible to
MITM it and remove the unwanted lossy streams from the
[main m3u8 file](https://datatracker.ietf.org/doc/html/rfc8216#section-4.3.4). The script in this repository uses
[mitmproxy](https://mitmproxy.org) for that purpose.

## Usage

Install mitmproxy and verify that it works - that you set the HTTPS proxy on your internet connection, installed the
certificate etc. You won't need the proxy to remain set, we'll use mitmproxy's "local" mode to intercept only the Music
app. Because of the second problem outlined above, the script needs to know if you want Hi-Res Lossless - if you do,
uncomment the relevant line.

Run mitmproxy with the script:
```
/Applications/mitmproxy.app/Contents/MacOS/mitmdump --allow-hosts=aod.itunes.apple.com --mode local:Music -s ~/path/to/strip-lossy-streams.py
```

Enjoy lossless streaming.

## Notes

- I literally read the Python tutorial to write this, don't hate me.
- This will not allow you to rip the streams in any way, they're still encrypted.
- I tried Tidal, but it doesn't have half the stuff I listen to. Plus, it may well have similar problems.
- Apple folks, please fix this. It can be an option  - I'll leave it to you to phrase "minimum streaming
  quality"/"disable adaptive streaming" in a way that doesn't confuse users - similar to the existing option to _not_
  stream Dolby Atmos. Or you can re-check all your streams to confirm they align perfectly, or you can attempt to
  detect on-device if switching variants is going to cause an audible hiccup and don't switch if it does (maybe align
  on device too?).
- Lossy ("High Quality") streaming uses a different endpoint entirely, serving unfragmented songs in the selected
  quality.
- This works with the iOS/iPadOS versions of the Music app too. Setting up e.g. a Raspberry Pi to run the proxy and your 
  devices to use it is left as an exercise for the reader.
