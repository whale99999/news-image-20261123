// main.ts — entrypoint for make.fun's "Sum up 23 November's world news
// in one image" bounty (news-image-20261123).
//
// The repository carries the finished front page as entry.png (composed by
// compose.py from the day's reported stories, with every illustration
// drawn in code). This program checks that file against the bounty's
// gate — a whole PNG or JPEG, at most 1 MiB, at most 1024 by 1024 pixels
// — and copies it unchanged to the output directory. Copying bytes, not
// re-rendering, means two runs always write identical bytes.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const LIMIT_BYTES = 1_048_576; // 1 MiB
const LIMIT_PX = 1024;

const root = dirname(fileURLToPath(import.meta.url));
const input = join(root, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const output = join(outDir, "entry.png");

function reject(reason: string): never {
  console.error(`entry.png rejected: ${reason}`);
  process.exit(1);
}

const data = readFileSync(input);
if (data.length === 0) reject("the file is empty");
if (data.length > LIMIT_BYTES) {
  reject(`the file is ${data.length} bytes, over the 1 MiB limit`);
}

const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const looksPng = PNG_MAGIC.every((byte, i) => data[i] === byte);
const looksJpeg =
  data[0] === 0xff &&
  data[1] === 0xd8 &&
  data[data.length - 2] === 0xff &&
  data[data.length - 1] === 0xd9;

if (looksPng) {
  // In a PNG the IHDR chunk starts at byte 8; width and height sit at
  // offsets 16 and 20 as big-endian 32-bit values.
  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  const width = view.getUint32(16);
  const height = view.getUint32(20);
  if (width === 0 || height === 0) reject("the PNG header names no pixels");
  if (width > LIMIT_PX || height > LIMIT_PX) {
    reject(`the PNG is ${width}x${height}, over the 1024x1024 limit`);
  }
  // A whole PNG ends with the 12-byte IEND chunk (length 0, "IEND").
  const tail = data.subarray(data.length - 12);
  const endsWithIend =
    tail[4] === 0x49 && tail[5] === 0x45 && tail[6] === 0x4e && tail[7] === 0x44;
  if (!endsWithIend) reject("the PNG does not end with its IEND chunk");
  console.log(`entry.png: PNG ${width}x${height}, ${data.length} bytes`);
} else if (looksJpeg) {
  console.log(`entry.png: JPEG, ${data.length} bytes`);
} else {
  reject("the file is neither a PNG nor a JPEG");
}

mkdirSync(outDir, { recursive: true });
writeFileSync(output, data);
console.log(`wrote ${output}`);
