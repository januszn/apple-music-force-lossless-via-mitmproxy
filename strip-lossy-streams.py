def strip_unwanted_streams(m3u8_bytes):
    EXT_X_MEDIA = b"#EXT-X-MEDIA:"
    EXT_X_STREAM_INF = b"#EXT-X-STREAM-INF:"
    GROUP_ID = b'GROUP-ID="'
    lines = m3u8_bytes.splitlines(keepends = True)
    output_lines = []
    wanted_streams = []
    skip_next_line = False
    for line in lines:
        if skip_next_line:
            skip_next_line = False
            continue
        if line.startswith(EXT_X_MEDIA):
            group_id_index = line.find(GROUP_ID, len(EXT_X_MEDIA));
            if group_id_index != -1:
                group_id_end_index = line.find(b'"', group_id_index + len(GROUP_ID))
                if group_id_end_index != -1:
                    group_id = line[(group_id_index + len(GROUP_ID)):group_id_end_index]
                    if group_id.startswith(b'audio-alac'):
                        wanted_streams.append(group_id)
                    else:
                        continue
        elif line.startswith(EXT_X_STREAM_INF):
            is_wanted_stream = False
            for wanted_stream in wanted_streams:
                if line.find(b'AUDIO="' + wanted_stream + b'"', len(EXT_X_STREAM_INF)) != -1:
                    is_wanted_stream = True
                    break
            if not is_wanted_stream:
                skip_next_line = True
                continue
        output_lines.append(line)
    if (output_lines):
        return b''.join(output_lines)
    return m3u8_bytes

def response(flow):
	if flow.response.headers["content-type"] == "application/vnd.apple.mpegurl":
		flow.response.content = strip_unwanted_streams(flow.response.content)
